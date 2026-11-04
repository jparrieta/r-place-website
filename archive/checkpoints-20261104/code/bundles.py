"""Portable interview bundles. All extraction is manual and fails closed.

No archive member is executed. Archive links, devices, duplicate paths, unlisted
files, credentials and path traversal are refused. Saved relative directory links
are described in the manifest and created only after regular files are verified.
The SHA comes from the catalogue,
not from a sidecar downloaded with an untrusted bundle.
"""
import hashlib
import json
import os
import posixpath
import re
import shutil
import tarfile
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath

FORMAT = 'rplace-interview-v1'
LINKS_FORMAT = 'rplace-interview-v2'
MAX_MANIFEST = 16*1024*1024
RESERVE = 2*1024**3


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def safe_name(value):
    if not isinstance(value,str) or not value or '\\' in value or '\x00' in value:
        raise ValueError('Invalid bundle path')
    p=PurePosixPath(value)
    if p.is_absolute() or any(x in ('..','.') for x in value.split('/')) or str(p)!=value:
        raise ValueError('Unsafe or noncanonical bundle path: '+value)
    return value


def credential_name(name):
    return any(part.lower() in {'auth.json','.credentials.json','credentials.json','.env','id_rsa','id_ed25519','cookies.sqlite','login.keychain-db'}
               or part.lower().endswith(('.keychain','.p12','.pfx')) for part in PurePosixPath(name).parts)


def validate_links(files, directories, links):
    """Only direct links to an archived directory in the same workspace."""
    if not isinstance(links,dict):raise ValueError('Invalid link inventory')
    names=set(files)|set(directories)|set(links)
    if len(names)!=len(files)+len(directories)+len(links):raise ValueError('Overlapping member kinds')
    for name in names:
        safe_name(name)
        if any(str(parent) in files or str(parent) in links for parent in PurePosixPath(name).parents):
            raise ValueError('Member descends through a file or link')
    for name,entry in links.items():
        target=entry.get('target')
        mode=entry.get('mode')
        if not name.startswith('workspace/') or credential_name(name):raise ValueError('Link outside workspace')
        if (not isinstance(target,str) or not target or '\\' in target or '\x00' in target
                or PurePosixPath(target).is_absolute() or type(mode) is not int or mode&~0o777):
            raise ValueError('Invalid saved link')
        resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),target))
        safe_name(resolved)
        if (resolved.split('/')[0]!='workspace' or resolved not in directories
                or any(str(parent) in links for parent in PurePosixPath(resolved).parents)):
            raise ValueError('Link target is not a direct archived workspace directory')


def restore_links(root, links):
    for name,entry in links.items():
        path=Path(root)/name
        path.parent.mkdir(parents=True,exist_ok=True)
        os.symlink(entry['target'],path)
        # Linux fixes link modes at 0777. The target and ordinary file modes are
        # still exact; this platform limit is carried in the admission receipt.
        if os.chmod in os.supports_follow_symlinks:
            os.chmod(path,entry['mode'],follow_symlinks=False)


def validate_manifest(m):
    required=('checkpoint_id','backend','session_id','model','effort','cli_version','transcript','files','provenance')
    if m.get('format') not in (FORMAT,LINKS_FORMAT) or any(not m.get(k) for k in required):
        raise ValueError('Incomplete interview manifest')
    if m['backend'] not in ('codex','claude') or not re.fullmatch(r'[A-Za-z0-9_.-]+',m['checkpoint_id']):
        raise ValueError('Unknown backend or invalid checkpoint ID')
    if not re.fullmatch(r'[0-9a-fA-F-]{36}',m['session_id']):raise ValueError('Invalid native session ID')
    if not isinstance(m['files'],dict) or len(m['files'])>200000:raise ValueError('Invalid file inventory')
    for name,entry in m['files'].items():
        safe_name(name)
        if not (name.startswith('workspace/') or name.startswith('native/') or name.startswith('evidence/')) or credential_name(name):
            raise ValueError('Forbidden bundle member: '+name)
        if not re.fullmatch('[0-9a-f]{64}',entry.get('sha256','')) or type(entry.get('size')) is not int or entry['size']<0:
            raise ValueError('Invalid manifest entry: '+name)
        if type(entry.get('mode',0o600)) is not int or entry.get('mode',0o600)&~0o777:raise ValueError('Invalid mode')
    if m['transcript'] not in m['files'] or not m['transcript'].startswith('native/'):
        raise ValueError('Native transcript is absent')
    if not any(k.startswith('workspace/') for k in m['files']):raise ValueError('Historical workspace is absent')
    for name,mode in m.get('directories',{}).items():
        safe_name(name)
        if name in m['files'] or name.split('/')[0] not in ('workspace','native','evidence') or type(mode) is not int or mode&~0o777:
            raise ValueError('Invalid directory manifest')
    if m.get('links') and m['format']!=LINKS_FORMAT:raise ValueError('Links require the version 2 loader')
    validate_links(m['files'],m.get('directories',{}),m.get('links',{}))
    cwd=m.get('workspace_cwd','.')
    if cwd!='.':safe_name(cwd)
    if m['provenance'].get('completed_boundary') is not True or not re.fullmatch('[0-9a-f]{64}',m['provenance'].get('source_sha256','')):
        raise ValueError('A verified completed boundary and source hash are required')
    return m


def inventory(root):
    out={}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():continue
        if p.is_dir():continue
        if not p.is_file():raise ValueError('Special file in bundle')
        rel=p.relative_to(root).as_posix()
        if rel=='manifest.json':continue
        if credential_name(rel):raise ValueError('Credential file: '+rel)
        with p.open('rb') as f:
            # A heuristic is not a substitute for the required release review.
            head=f.read(16384)
        if b'PRIVATE KEY-----' in head:raise ValueError('Private key in '+rel)
        out[rel]={'sha256':digest(p),'size':p.stat().st_size,'mode':p.stat().st_mode&0o777}
    return out


def pack(root, target, metadata, compresslevel=9):
    root=Path(root).resolve();target=Path(target).resolve()
    if target.is_relative_to(root):raise ValueError('Write bundle outside the prepared tree')
    if target.exists():raise ValueError('Refusing to replace an existing bundle')
    m={**metadata,'format':FORMAT,'files':inventory(root),
       'links':{p.relative_to(root).as_posix():{'target':os.readlink(p),'mode':p.lstat().st_mode&0o777}
                for p in root.rglob('*') if p.is_symlink()},
       'directories':{p.relative_to(root).as_posix():p.stat().st_mode&0o777 for p in root.rglob('*') if p.is_dir() and not p.is_symlink()}}
    if m['links']:m['format']=LINKS_FORMAT
    validate_manifest(m)
    import io
    raw=json.dumps(m,sort_keys=True,indent=2).encode()+b'\n'
    target.parent.mkdir(parents=True,exist_ok=True)
    tmp=target.with_name(target.name+'.partial')
    if tmp.exists():raise ValueError('A partial bundle exists; inspect it first')
    try:
        with tarfile.open(tmp,'w:gz',dereference=False,compresslevel=compresslevel) as t:
            info=tarfile.TarInfo('manifest.json');info.size=len(raw);info.mode=0o600
            t.addfile(info,io.BytesIO(raw))
            for rel in sorted(m['files']):t.add(root/rel,arcname=rel,recursive=False)
        sha=digest(tmp)
        verify(tmp,sha,m['checkpoint_id'])
        os.replace(tmp,target)
    except BaseException:
        # Preserve failed output for inspection; it is never admitted.
        raise
    return {'sha256':sha,'bytes':target.stat().st_size,'unpacked_bytes':sum(x['size'] for x in m['files'].values()),'manifest':m}


def verify(archive, expected_sha, checkpoint_id=None, destination=None, max_bytes=50*1024**3):
    if not re.fullmatch('[0-9a-f]{64}',expected_sha or '') or digest(archive)!=expected_sha:
        raise ValueError('Bundle SHA-256 mismatch')
    dest=Path(destination).resolve() if destination else None
    if dest and dest.exists():raise ValueError('Restore destination must be new')
    seen=set();m=None
    try:
        with tarfile.open(archive,'r|gz') as t:
            first=t.next()
            if first is None or first.name!='manifest.json' or not first.isfile() or first.size>MAX_MANIFEST:
                raise ValueError('Manifest must be the first regular member')
            m=validate_manifest(json.load(t.extractfile(first)))
            if checkpoint_id and m['checkpoint_id']!=checkpoint_id:raise ValueError('Wrong checkpoint bundle')
            total=sum(e['size'] for e in m['files'].values())
            if total>max_bytes:raise ValueError('Bundle exceeds restore size limit')
            if dest:
                if shutil.disk_usage(dest.parent).free<total+RESERVE:raise ValueError('Insufficient restore space plus reserve')
                dest.mkdir(mode=0o700)
                for name,mode in sorted(m.get('directories',{}).items()):
                    (dest/name).mkdir(parents=True,exist_ok=True)
            for member in t:
                # Stream iteration may include the member already returned by next().
                if member is first:continue
                name=safe_name(member.name)
                if name in seen or name not in m['files'] or not member.isfile():raise ValueError('Unlisted, duplicate or non-regular member: '+name)
                seen.add(name);expected=m['files'][name]
                if member.size!=expected['size']:raise ValueError('Member size mismatch: '+name)
                output=None
                if dest:
                    p=dest/name;p.parent.mkdir(parents=True,exist_ok=True)
                    output=p.open('xb')
                h=hashlib.sha256()
                native_buffer=b'';native_identity=False
                def native_line(line):
                    nonlocal native_identity
                    if not line.strip():return
                    row=json.loads(line)
                    if m['backend']=='codex' and row.get('type')=='session_meta':
                        if row.get('payload',{}).get('id')!=m['session_id']:raise ValueError('Native transcript identity differs from manifest')
                        native_identity=True
                    elif m['backend']=='claude' and row.get('sessionId')==m['session_id']:
                        native_identity=True
                try:
                    with t.extractfile(member) as f:
                        for b in iter(lambda:f.read(1024*1024),b''):
                            h.update(b)
                            if output:output.write(b)
                            if name==m['transcript']:
                                native_buffer+=b
                                lines=native_buffer.split(b'\n');native_buffer=lines.pop()
                                for line in lines:native_line(line)
                                if len(native_buffer)>MAX_MANIFEST:raise ValueError('Native transcript line is too large')
                finally:
                    if output:output.close()
                if name==m['transcript']:
                    native_line(native_buffer)
                    if not native_identity:raise ValueError('No matching native session in the transcript')
                if h.hexdigest()!=expected['sha256']:raise ValueError('Member hash mismatch: '+name)
                if dest:(dest/name).chmod(expected.get('mode',0o600)&0o777)
            if seen!=set(m['files']):raise ValueError('Bundle has missing members')
        if dest:
            restore_links(dest,m.get('links',{}))
            for name,mode in sorted(m.get('directories',{}).items(),reverse=True):(dest/name).chmod(mode)
            if not (dest/'workspace'/m.get('workspace_cwd','.')).is_dir():raise ValueError('Saved working directory is absent')
            (dest/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
        return m
    except BaseException:
        if dest and dest.exists():shutil.rmtree(dest)
        raise


def download(url, target, expected_sha, max_bytes=20*1024**3):
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme!='https' or parsed.username or parsed.password:raise ValueError('Only HTTPS bundle URLs are admitted')
    target=Path(target)
    if target.exists():
        if digest(target)==expected_sha:return target
        raise ValueError('Cached bundle differs from catalogue')
    tmp=target.with_suffix('.partial');target.parent.mkdir(parents=True,exist_ok=True)
    request=urllib.request.Request(url,headers={'User-Agent':'rplace-checkpoint-interview/1'})
    with urllib.request.urlopen(request,timeout=60) as response, tmp.open('xb') as f:
        if urllib.parse.urlsplit(response.url).scheme!='https':raise ValueError('Insecure redirect')
        n=0
        for b in iter(lambda:response.read(1024*1024),b''):
            n+=len(b)
            if n>max_bytes:raise ValueError('Download exceeds catalogue limit')
            f.write(b)
    if digest(tmp)!=expected_sha:raise ValueError('Downloaded bundle hash mismatch; partial retained')
    os.replace(tmp,target);return target
