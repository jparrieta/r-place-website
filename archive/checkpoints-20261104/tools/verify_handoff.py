"""Verify the small handoff, without fetching data or running model calls."""
import hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
expected={}
for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
    sha,name=line.split('  ',1)
    p=pathlib.PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and str(p)==name
    assert name!='MANIFEST.sha256' and name not in expected
    expected[name]=sha
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256' and '__pycache__' not in p.parts}
assert actual==set(expected), 'Unexpected or missing handoff files'
for name,sha in expected.items():
    path=ROOT/name
    assert not path.is_symlink() and hashlib.sha256(path.read_bytes()).hexdigest()==sha, name
print('Verified',len(expected),'handoff files. No network or model calls were made.')
