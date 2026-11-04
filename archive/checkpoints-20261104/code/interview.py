"""Private checkpoint interviews. Uses separate state and has no research endpoints."""
import argparse
import hmac
from datetime import datetime, timezone
import json
import os
import re
import secrets
import shutil
import subprocess
import threading
import time
import urllib.parse
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import bundles, native, originals

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_HOME=Path.home()/'.rplace-interviews'


def private_home(path):
    home=Path(path).expanduser().resolve()
    if home.is_relative_to(ROOT) or any((parent/'.git').exists() for parent in (home,*home.parents)):
        raise ValueError('Interview state and login must be outside every Git checkout')
    return home


class Manager:
    def __init__(self,home,catalog,local_bundles=None,explicit=None,max_sessions=1,idle_seconds=1800):
        self.home=private_home(home)
        if self.home.exists() and not (self.home/'INTERVIEW-HOME.json').exists():
            allowed={'sessions','cache','login','staging','access-token'}
            if any(p.name not in allowed for p in self.home.iterdir()):raise ValueError('Use a new, dedicated interview home')
        self.home.mkdir(parents=True,exist_ok=True,mode=0o700);self.home.chmod(0o700)
        (self.home/'INTERVIEW-HOME.json').write_text('{"purpose":"rplace-checkpoint-interviews"}\n')
        self.sessions={};self.guard=threading.RLock();self.explicit=explicit
        self.max_sessions=max_sessions;self.idle_seconds=idle_seconds;self.local=local_bundles or {}
        self.restore_slot=threading.Lock()
        self.entries={c['id']:c for c in catalog['checkpoints'] if c.get('availability')=='ready' and c.get('bundle')}
        (self.home/'sessions').mkdir(exist_ok=True,mode=0o700);(self.home/'cache').mkdir(exist_ok=True,mode=0o700)

    def create(self,checkpoint):
        with self.guard:
            if checkpoint not in self.entries:raise ValueError('Checkpoint is not admitted')
            if len(self.sessions)>=self.max_sessions:raise ValueError('All interview slots are in use. Close an open interview before starting another.')
            sid=uuid.uuid4().hex;path=self.home/'sessions'/sid
            path.mkdir(mode=0o700);(path/'OWNER.json').write_text(json.dumps({'id':sid,'purpose':'checkpoint-interview'}))
            s={'id':sid,'checkpoint':checkpoint,'status':'restoring','messages':[],'events':[],'error':None,
               'native':None,'path':path,'last':time.monotonic(),'cancel':False,'worker':None,
               'phase':'waiting_restore','created_utc':datetime.now(timezone.utc).isoformat()}
            self.sessions[sid]=s
            def restore():
                try:
                    with self.restore_slot:
                        if s['cancel']:return
                        entry=self.entries[checkpoint];bundle=entry['bundle'];archive=self.local.get(checkpoint)
                        if entry.get('original_source') and not archive:
                            s['phase']='restoring_originals';self.save(s)
                            m=originals.restore(originals.load(entry),path/'restored',self.home/'cache')
                            s['restoration']=json.loads((path/'original-source-receipt.json').read_text())
                            s['restoration']['route']='original-github'
                        else:
                            if not archive:
                                s['phase']='downloading';self.save(s)
                                archive=bundles.download(bundle['url'],self.home/'cache'/(bundle['sha256']+'.tar.gz'),bundle['sha256'],bundle['bytes'])
                            s['phase']='unpacking_verifying';self.save(s)
                            m=bundles.verify(archive,bundle['sha256'],checkpoint,path/'restored',max_bytes=bundle['unpacked_bytes'])
                            s['restoration']={'route':'explicit-bundle' if self.local.get(checkpoint) else 'published-bundle',
                                              'bundle_sha256':bundle['sha256']}
                        s['phase']='checking_identity';self.save(s)
                        # Check provenance independently of the user-facing label.
                        for k in ('backend','session_id','model','effort'):
                            if entry.get(k) and entry[k]!=m[k]:raise ValueError('Catalogue and bundle disagree on '+k)
                        if s['cancel']:return
                        s['manifest']=m;s['status']='ready';s['phase']='files_ready';self.save(s)
                except Exception as e:s['status']='error';s['phase']='error';s['error']=str(e);self.save(s)
                finally:
                    if s['cancel']:self.remove(s)
            s['worker']=threading.Thread(target=restore,daemon=True);s['worker'].start()
            return sid

    def save(self,s):
        if s['path'].exists():
            data={k:s[k] for k in ('id','checkpoint','status','phase','created_utc','messages','events','error')}
            data['restoration']=s.get('restoration')
            (s['path']/'interview.json').write_text(json.dumps(data,indent=2)+'\n')

    def snapshot(self,sid):
        with self.guard:
            s=self.sessions.get(sid)
            if not s:raise ValueError('Interview has ended or expired')
            s['last']=time.monotonic()
            return {k:s[k] for k in ('id','checkpoint','status','phase','created_utc','messages','events','error')}

    def listing(self, ids=None, touch=False):
        with self.guard:
            result=[]
            for sid,s in self.sessions.items():
                if ids is not None and sid not in ids:continue
                if s['cancel']:continue
                if touch:s['last']=time.monotonic()
                row={k:s[k] for k in ('id','checkpoint','status','phase','created_utc')}
                row['title']=self.entries[s['checkpoint']].get('title',s['checkpoint'])
                result.append(row)
            return {'interviews':result,'capacity':self.max_sessions,'idle_seconds':self.idle_seconds}

    def ask(self,sid,text):
        if not isinstance(text,str) or not text.strip() or len(text)>20000:raise ValueError('Send a question of 1 to 20,000 characters')
        with self.guard:
            s=self.sessions.get(sid)
            if not s or s['status']!='ready' or s['cancel']:raise ValueError('Interview is not ready for a question')
            s['status']='working';s['phase']='opening_conversation' if not s['native'] else 'answering';s['last']=time.monotonic();s['messages'].append({'role':'user','text':text})
            self.save(s)
            def work():
                try:
                    if not s['native']:
                        proof=self.entries[s['checkpoint']]['bundle'].get('proof',{})
                        if proof and proof.get('bundle_sha256')!=self.entries[s['checkpoint']]['bundle']['sha256']:
                            raise ValueError('Runtime proof belongs to another bundle')
                        s['native']=native.open_native(s['path'],s['manifest'],self.home/'login'/s['manifest']['backend'],self.explicit,
                            lambda event:s['events'].append(event) if len(s['events'])<500 else None,runtime_proof=proof)
                    if s['cancel']:return
                    self.save(s)
                    response=s['native'].ask(text)
                    s['messages'].append({'role':'assistant','label':'New checkpoint interview response','text':response})
                    s['status']='ready';s['phase']='ready';self.save(s)
                except Exception as e:s['status']='error';s['phase']='error';s['error']=str(e);self.save(s)
                finally:
                    if s['cancel']:self.remove(s)
            s['worker']=threading.Thread(target=work,daemon=True);s['worker'].start()

    def export(self,sid):
        snap=self.snapshot(sid);entry=self.entries[snap['checkpoint']]
        state=self.sessions[sid];m=state.get('manifest',{});actor=state.get('native')
        return {'format':'rplace-checkpoint-interview-export-v1','notice':'New responses, not the original research record.',
                'bundle_sha256':entry['bundle']['sha256'],'backend':m.get('backend'),'model':m.get('model'),'effort':m.get('effort'),
                'historical_cli_version':m.get('cli_version'),
                'restoration':state.get('restoration'),
                'interview_cli_version':getattr(actor,'runtime_version',None),
                'parent_session_id':m.get('session_id'),'interview_session_id':getattr(actor,'thread',None),**snap}

    def remove(self,s):
        if s.get('native'):s['native'].close();s['native']=None
        path=s['path'];owner=path/'OWNER.json'
        if path.parent!=self.home/'sessions' or not owner.is_file() or json.loads(owner.read_text()).get('id')!=s['id']:
            raise ValueError('Refusing to clean an unowned path')
        shutil.rmtree(path)
        with self.guard:self.sessions.pop(s['id'],None)

    def end(self,sid):
        with self.guard:
            s=self.sessions.get(sid)
            if not s:return
            s['cancel']=True
            actor=s.get('native');worker=s.get('worker')
            if actor:actor.close()
            if not worker or not worker.is_alive():self.remove(s)

    def expire(self):
        with self.guard:ids=[sid for sid,s in self.sessions.items() if time.monotonic()-s['last']>self.idle_seconds]
        for sid in ids:self.end(sid)


class Service(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,manager,token,origin=None):
        super().__init__(address,Handler);self.manager=manager;self.token=token
        self.origin=origin or f'http://127.0.0.1:{self.server_address[1]}'
        self.host=urllib.parse.urlsplit(self.origin).netloc


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def reply(self,status,data,kind='application/json'):
        raw=data if isinstance(data,bytes) else json.dumps(data).encode() if kind=='application/json' else data.encode()
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.end_headers();self.wfile.write(raw)

    def allowed(self):
        if self.headers.get('Host')!=self.server.host:return False
        origin=self.headers.get('Origin')
        if origin and origin!=self.server.origin:return False
        supplied=self.headers.get('Authorization','')
        return hmac.compare_digest(supplied,'Bearer '+self.server.token)

    def do_GET(self):
        path=urllib.parse.urlsplit(self.path).path
        if self.headers.get('Host')!=self.server.host:self.reply(403,{'error':'Host not allowed'});return
        assets={'/':('interview.html','text/html'),'/assets/site.css':('site.css','text/css'),
                '/assets/site.js':('site.js','text/javascript'),'/assets/interview.js':('interview.js','text/javascript')}
        for folder in ('fonts', 'type'):
            for font in (ROOT/'website/assets'/folder).glob('*'):
                if font.is_file() and not font.is_symlink() and font.suffix in ('.css','.woff2'):
                    assets['/assets/'+folder+'/'+font.name]=(folder+'/'+font.name,'text/css' if font.suffix=='.css' else 'font/woff2')
        if path in assets:
            name,kind=assets[path];self.reply(200,(ROOT/'website/assets'/name).read_bytes(),kind);return
        if not self.allowed():self.reply(401,{'error':'Enter the private interview access token'});return
        try:
            if path=='/api/checkpoints':
                self.reply(200,[{'id':c['id'],'title':(c.get('entity','')+' · '+c.get('title',c['id'])).strip(' ·')} for c in self.server.manager.entries.values()]);return
            if path=='/api/interviews':
                q=urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                ids=q.get('ids',[''])[0].split(',') if 'ids' in q else None
                if ids is not None and any(not re.fullmatch(r'[0-9a-f]{32}',x) for x in ids):raise ValueError('Invalid interview reference')
                self.reply(200,self.server.manager.listing(ids,touch=q.get('touch')==['1']));return
            m=re.fullmatch(r'/api/interviews/([0-9a-f]{32})(/export)?',path)
            if m:
                result=self.server.manager.export(m[1]) if m[2] else self.server.manager.snapshot(m[1])
                self.reply(200,result);return
            self.reply(404,{'error':'No such interview endpoint'})
        except ValueError as e:self.reply(400,{'error':str(e)})

    def do_POST(self):
        if not self.allowed():self.reply(403,{'error':'Private access or origin check failed'});return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=100000 or self.headers.get_content_type()!='application/json':raise ValueError('Send a bounded JSON request')
            data=json.loads(self.rfile.read(n));path=urllib.parse.urlsplit(self.path).path
            if path=='/api/interviews':
                sid=self.server.manager.create(data['checkpoint']);self.reply(202,{'id':sid});return
            m=re.fullmatch(r'/api/interviews/([0-9a-f]{32})/(message|end)',path)
            if not m:self.reply(404,{'error':'No such interview endpoint'});return
            if m[2]=='message':self.server.manager.ask(m[1],data['text'])
            else:self.server.manager.end(m[1])
            self.reply(202,{'accepted':True})
        except (ValueError,KeyError,TypeError) as e:self.reply(400,{'error':str(e)})


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--home',type=Path,default=DEFAULT_HOME)
    sub=p.add_subparsers(dest='command',required=True)
    login=sub.add_parser('login');login.add_argument('backend',choices=['codex','claude']);login.add_argument('--executable')
    for name in ('serve','launch'):
        cmd=sub.add_parser(name)
        if name=='launch':
            cmd.add_argument('checkpoint')
            cmd.add_argument('--bundle',type=Path,help='An already downloaded bundle; catalogue checks still apply')
        cmd.add_argument('--catalog',type=Path,default=ROOT/'website/catalog.json');cmd.add_argument('--bundle-map',type=Path)
        cmd.add_argument('--port',type=int,default=0 if name=='launch' else 8776);cmd.add_argument('--origin')
        cmd.add_argument('--executable');cmd.add_argument('--no-browser',action='store_true')
    pack=sub.add_parser('pack');pack.add_argument('prepared',type=Path);pack.add_argument('metadata',type=Path);pack.add_argument('output',type=Path)
    check=sub.add_parser('verify');check.add_argument('bundle',type=Path);check.add_argument('--sha256',required=True)
    args=p.parse_args();home=args.home.expanduser().resolve()
    if args.command=='pack':
        result=bundles.pack(args.prepared,args.output,json.loads(args.metadata.read_text()))
        print(json.dumps({k:v for k,v in result.items() if k!='manifest'},indent=2));return
    if args.command=='verify':
        m=bundles.verify(args.bundle,args.sha256);print('Verified complete bundle: '+m['checkpoint_id']);return
    if args.command=='login':
        home=private_home(home)
        dest=home/'login'/args.backend;dest.mkdir(parents=True,exist_ok=True,mode=0o700)
        command=[native.executable(args.backend,args.executable)]+(['login'] if args.backend=='codex' else ['auth','login'])
        raise SystemExit(subprocess.call(command,env=native.environment(dest,args.backend)))
    catalog=json.loads(args.catalog.read_text())
    if args.command=='launch':catalog['checkpoints']=[c for c in catalog['checkpoints'] if c['id']==args.checkpoint]
    mapping=json.loads(args.bundle_map.read_text()) if args.bundle_map else {}
    if args.command=='launch' and args.bundle:
        if mapping:raise SystemExit('Use --bundle or --bundle-map, not both.')
        mapping={args.checkpoint:str(args.bundle.expanduser().resolve())}
    manager=Manager(home,catalog,mapping,args.executable)
    if not manager.entries:raise SystemExit('No verified bundle is admitted for this selection. Read its record on the website.')
    token=secrets.token_urlsafe(32);tokenfile=home/'access-token';tokenfile.write_text(token);tokenfile.chmod(0o600)
    server=Service(('127.0.0.1',args.port),manager,token,args.origin)
    selection='?checkpoint='+urllib.parse.quote(args.checkpoint,safe='') if args.command=='launch' else ''
    url=server.origin+'/'+selection+'#token='+token
    print(f'Private interview service: {server.origin}/\nAccess token saved outside Git: {tokenfile}\nPress Ctrl-C to end the service. Research controllers are not connected.')
    if not args.no_browser:webbrowser.open(url)
    def reap():
        while True:
            time.sleep(30);manager.expire()
    threading.Thread(target=reap,daemon=True).start()
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        server.server_close()
        for sid in list(manager.sessions):manager.end(sid)
        # Give active cancellation a bounded chance to remove its owned workspace.
        for s in list(manager.sessions.values()):
            if s.get('worker'):s['worker'].join(timeout=10)


if __name__=='__main__':main()
