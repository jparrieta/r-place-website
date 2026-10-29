#!/usr/bin/env bash
set -euo pipefail
for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -I -c 'import sys; sys.exit(sys.version_info < (3,11))' 2>/dev/null; then
    exec "$candidate" -I -c '"""Generate a one-command bootstrap for the exact launcher from this build."""
import argparse
import fcntl
import hashlib
import io
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import venv
import zipfile


def members(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        files = {}
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            if (not path.parts or path.parts[0] != '"'"'rplace-interviews'"'"' or path.is_absolute()
                    or '"'"'..'"'"' in path.parts or '"'"'\\'"'"' in info.filename or info.is_dir()
                    or stat.S_IFMT(info.external_attr >> 16) not in (0, stat.S_IFREG)):
                raise ValueError('"'"'Unsafe launcher member.'"'"')
            name = str(PurePosixPath(*path.parts[1:]))
            if name in files or name == '"'"'.'"'"':
                raise ValueError('"'"'Duplicate or empty launcher member.'"'"')
            if info.file_size > 32*1024**2 or sum(len(b) for b in files.values())+info.file_size > 256*1024**2:
                raise ValueError('"'"'Launcher exceeds its size limit.'"'"')
            files[name] = archive.read(info)
    manifest = files.get('"'"'FILES.sha256'"'"', b'"'"''"'"').decode().splitlines()
    expected = {}
    for line in manifest:
        digest, name = line.split('"'"'  '"'"', 1)
        if name in expected or not re.fullmatch('"'"'[0-9a-f]{64}'"'"', digest):
            raise ValueError('"'"'Invalid launcher manifest.'"'"')
        expected[name] = digest
    if set(expected) != set(files)-{'"'"'FILES.sha256'"'"'}:
        raise ValueError('"'"'Launcher manifest does not cover every file.'"'"')
    for name, digest in expected.items():
        if hashlib.sha256(files[name]).hexdigest() != digest:
            raise ValueError('"'"'Launcher file checksum failed: '"'"'+name)
    return files


def install(base, digest, size, storage):
    url = base.rstrip('"'"'/'"'"')+'"'"'/rplace-interviews.zip'"'"'
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != '"'"'https'"'"' and not (parsed.scheme == '"'"'http'"'"' and parsed.hostname in ('"'"'localhost'"'"', '"'"'127.0.0.1'"'"', '"'"'::1'"'"'))
            or parsed.username or parsed.password or parsed.query or parsed.fragment):
        raise ValueError('"'"'Use an HTTPS website, or this computer\'"'"'s loopback preview.'"'"')
    storage = Path(storage).expanduser().resolve()
    if any((parent/'"'"'.git'"'"').exists() for parent in (storage, *storage.parents)):
        raise ValueError('"'"'The launcher must be installed outside Git checkouts.'"'"')
    storage.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (storage/'"'"'install.lock'"'"').open('"'"'a'"'"') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        destination = storage/digest
        archive = destination/'"'"'launcher.zip'"'"'
        if destination.exists():
            if not archive.is_file() or archive.is_symlink():
                raise ValueError('"'"'Incomplete cached launcher. Keep it for review; no files were replaced.'"'"')
            raw = archive.read_bytes()
        else:
            print('"'"'Downloading the interview launcher.'"'"', flush=True)
            with urllib.request.urlopen(url, timeout=60) as response:
                redirected = urllib.parse.urlsplit(response.url)
                if redirected.scheme != '"'"'https'"'"' and not (redirected.scheme == '"'"'http'"'"' and redirected.hostname in ('"'"'localhost'"'"','"'"'127.0.0.1'"'"','"'"'::1'"'"')):
                    raise ValueError('"'"'Launcher download redirected to an insecure URL.'"'"')
                raw = response.read(size+1)
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('"'"'Launcher download checksum failed. Nothing was executed.'"'"')
        files = members(raw)
        if destination.exists():
            for name, data in files.items():
                target = destination/'"'"'rplace-interviews'"'"'/name
                if target.is_symlink() or not target.is_file() or target.read_bytes() != data:
                    raise ValueError('"'"'Cached launcher changed: '"'"'+name+'"'"'. Nothing was executed.'"'"')
        else:
            temporary = Path(tempfile.mkdtemp(prefix='"'"'.install-'"'"', dir=storage))
            try:
                (temporary/'"'"'launcher.zip'"'"').write_bytes(raw)
                for name, data in files.items():
                    target = temporary/'"'"'rplace-interviews'"'"'/name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                temporary.rename(destination)
            finally:
                if temporary.exists():
                    shutil.rmtree(temporary)
        environment = destination/'"'"'venv'"'"'
        if not (environment/'"'"'bin/python'"'"').is_file():
            print('"'"'Preparing a private Python environment.'"'"', flush=True)
            venv.EnvBuilder(with_pip=True).create(environment)
        print('"'"'Launcher verified. Checking account and runtime requirements.'"'"', flush=True)
        return destination/'"'"'rplace-interviews'"'"', environment/'"'"'bin/python'"'"'


def main(digest, size):
    parser = argparse.ArgumentParser(description='"'"'Download, verify and open a checkpoint interview.'"'"')
    parser.add_argument('"'"'checkpoint'"'"')
    parser.add_argument('"'"'downloads_url'"'"')
    args, extra = parser.parse_known_args()
    if not re.fullmatch(r'"'"'[A-Za-z0-9][A-Za-z0-9_.-]*'"'"', args.checkpoint):
        parser.error('"'"'Invalid checkpoint ID.'"'"')
    try:
        root, python = install(args.downloads_url, digest, size, Path.home()/'"'"'.local/share/rplace-interview-launchers'"'"')
    except (ValueError, OSError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        parser.exit(1, str(error)+'"'"'\nNo interview was started.\n'"'"')
    os.chdir(root)
    # Leave research environment overrides and startup modules out of the launcher.
    env = {key:value for key,value in os.environ.items() if not key.startswith('"'"'PYTHON'"'"')}
    env['"'"'PYTHONDONTWRITEBYTECODE'"'"'] = '"'"'1'"'"'
    os.execve(str(python), [str(python), '"'"'-m'"'"', '"'"'website.quickstart'"'"', args.checkpoint, *extra], env)


main('"'"'ab14b2546ab706de39ce0d19ff90b708b49cb656a94811691196eef380395626'"'"', 43590667)
' "$@"
  fi
done
printf '%s\n' 'Python 3.11 or newer is required. Install it, then paste the same command again.' >&2
exit 1
