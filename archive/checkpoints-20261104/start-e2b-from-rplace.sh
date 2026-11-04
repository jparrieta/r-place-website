#!/usr/bin/env bash
set -euo pipefail
for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -I -c 'import sys; sys.exit(sys.version_info < (3,11))' 2>/dev/null; then
    exec "$candidate" -I -c 'import hashlib,io,os,pathlib,shutil,stat,sys,tempfile,urllib.parse,urllib.request,zipfile
DIGEST='"'"'a69ca259600deda9a1d87d971797c2065245ebca48e86de4479617d6b080198f'"'"'
SIZE=21264
if len(sys.argv)<2:raise SystemExit('"'"'Pass the immutable handoff folder URL.'"'"')
base=sys.argv[1].rstrip('"'"'/'"'"')
u=urllib.parse.urlsplit(base)
if u.scheme!='"'"'https'"'"' or u.hostname!='"'"'raw.githubusercontent.com'"'"' or u.query or u.fragment:
    raise SystemExit('"'"'Use the pinned GitHub handoff URL.'"'"')
storage=pathlib.Path.home()/'"'"'.local/share/rplace-e2b-launchers'"'"'
if any((p/'"'"'.git'"'"').exists() for p in (storage,*storage.parents)):
    raise SystemExit('"'"'Launcher storage must be outside Git.'"'"')
storage.mkdir(parents=True,exist_ok=True,mode=0o700)
dest=storage/DIGEST
if dest.exists():
    raw=(dest/'"'"'launcher.zip'"'"').read_bytes()
else:
    print('"'"'Downloading the small E2b launcher. Research comes directly from r-place Git.'"'"',flush=True)
    with urllib.request.urlopen(base+'"'"'/launchers/e2b-git-launcher.zip'"'"',timeout=120) as response:raw=response.read(SIZE+1)
if len(raw)!=SIZE or hashlib.sha256(raw).hexdigest()!=DIGEST:raise SystemExit('"'"'Launcher checksum failed; nothing executed.'"'"')
files={}
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    for i in z.infolist():
        p=pathlib.PurePosixPath(i.filename)
        if p.is_absolute() or '"'"'..'"'"' in p.parts or not p.parts or p.parts[0]!='"'"'rplace-e2b-git'"'"' or i.is_dir() or stat.S_IFMT(i.external_attr>>16) not in (0,stat.S_IFREG):
            raise SystemExit('"'"'Unsafe launcher member.'"'"')
        n='"'"'/'"'"'.join(p.parts[1:])
        if not n or n in files or i.file_size>2*1024**2:raise SystemExit('"'"'Invalid launcher member.'"'"')
        files[n]=z.read(i)
expected={}
for line in files['"'"'FILES.sha256'"'"'].decode().splitlines():
    h,n=line.split('"'"'  '"'"',1)
    if n in expected:raise SystemExit('"'"'Repeated launcher member.'"'"')
    expected[n]=h
if set(expected)!=set(files)-{'"'"'FILES.sha256'"'"'}:raise SystemExit('"'"'Incomplete launcher manifest.'"'"')
if any(hashlib.sha256(files[n]).hexdigest()!=h for n,h in expected.items()):raise SystemExit('"'"'Launcher member checksum failed.'"'"')
if dest.exists():
    for n,b in files.items():
        p=dest/'"'"'rplace-e2b-git'"'"'/n
        if p.is_symlink() or not p.is_file() or p.read_bytes()!=b:raise SystemExit('"'"'Cached launcher changed; nothing executed.'"'"')
else:
    temp=pathlib.Path(tempfile.mkdtemp(prefix='"'"'.install-'"'"',dir=storage))
    (temp/'"'"'launcher.zip'"'"').write_bytes(raw)
    for n,b in files.items():
        p=temp/'"'"'rplace-e2b-git'"'"'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    temp.rename(dest)
env={k:v for k,v in os.environ.items() if not k.startswith('"'"'PYTHON'"'"')}
env['"'"'PYTHONDONTWRITEBYTECODE'"'"']='"'"'1'"'"'
os.execve(sys.executable,[sys.executable,'"'"'-B'"'"',str(dest/'"'"'rplace-e2b-git/tools/e2b_from_rplace.py'"'"'),*sys.argv[2:]],env)
' "$@"
  fi
done
printf '%s\n' 'Install Python 3.11 or newer, then run this command again.' >&2
exit 1
