"""Download exact draft assets. Read-only GitHub access; no publication operations."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=json.loads((ROOT/'release-metadata/ASSETS.json').read_text())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only',choices=['launcher','supplements','all'],default='launcher')
parser.add_argument('--destination',type=pathlib.Path,default=pathlib.Path.home()/'rplace-checkpoint-handoff-downloads')
parser.add_argument('--list',action='store_true',help='List the selected assets without downloading or logging in')
args=parser.parse_args()
rows=[a for a in SPEC['assets'] if args.only=='all' or
      (args.only=='launcher' and a['name']=='rplace-interviews.zip') or
      (args.only=='supplements' and a['name'].endswith('.supplement.tar.gz'))]
if args.list:
    for row in rows:print(row['name'],row['bytes'],row['sha256'])
    raise SystemExit(0)
if not shutil.which('gh'):raise SystemExit('Install GitHub CLI first. No files were downloaded.')
destination=args.destination.expanduser().resolve()
if any((p/'.git').exists() for p in (destination,*destination.parents)):
    raise SystemExit('Choose a download directory outside Git repositories.')
destination.mkdir(parents=True,exist_ok=True,mode=0o700)
try:
    release=json.loads(subprocess.check_output(['gh','api',f'repos/{SPEC["repository"]}/releases/{SPEC["release_id"]}']))
except subprocess.CalledProcessError:
    raise SystemExit('Draft access failed. Use an authorized gh login; do not publish the release to gain access.')
remote={a['id']:a for a in release['assets']}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(4*1024**2),b''):h.update(b)
    return h.hexdigest()

for row in rows:
    name=row['name']; target=destination/name
    if pathlib.Path(name).name!=name:raise SystemExit('Unsafe asset filename')
    asset=remote.get(row['id'])
    if not asset or asset['name']!=name or asset['size']!=row['bytes'] or asset['digest']!='sha256:'+row['sha256']:
        raise SystemExit('The draft asset differs from the reviewed manifest: '+name)
    if target.exists():
        if target.is_symlink() or target.stat().st_size!=row['bytes'] or digest(target)!=row['sha256']:
            raise SystemExit('Existing file differs; it was not overwritten: '+str(target))
        print('Already verified:',target,flush=True);continue
    partial=destination/(name+'.partial')
    if partial.exists():raise SystemExit('Inspect the retained partial before retrying: '+str(partial))
    if shutil.disk_usage(destination).free < row['bytes']+2*1024**3:
        raise SystemExit('Insufficient space for this asset plus a 2 GiB reserve.')
    process=subprocess.Popen(['gh','api','-H','Accept: application/octet-stream',
        f'repos/{SPEC["repository"]}/releases/assets/{row["id"]}'],stdout=subprocess.PIPE)
    h=hashlib.sha256();count=0
    with partial.open('xb') as out:
        for block in iter(lambda:process.stdout.read(4*1024**2),b''):
            count+=len(block)
            if count>row['bytes']:
                process.terminate();process.wait();raise SystemExit('Asset exceeded its recorded size. Partial retained.')
            h.update(block);out.write(block)
    if process.wait()!=0 or count!=row['bytes'] or h.hexdigest()!=row['sha256']:
        raise SystemExit('Asset verification failed. Partial retained: '+str(partial))
    partial.replace(target);print('Verified:',target,flush=True)
