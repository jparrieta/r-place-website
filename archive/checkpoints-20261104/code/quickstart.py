"""Prepare a reader's local interview, without starting a model turn."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from . import interview, native, originals


def ensure_login(backend, executable, home):
    login = home/'login'/backend
    if backend == 'claude':
        try:
            native.claude_environment(login, login)
            return
        except ValueError:
            pass
    else:
        status = subprocess.run([executable, 'login', 'status'],
                                env=native.environment(login, backend),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        if status.returncode == 0:
            return
    print('Sign in to '+backend+' for checkpoint interviews. Your research login is separate.', flush=True)
    subprocess.run([sys.executable, '-m', 'website.interview', '--home', str(home),
                    'login', backend, '--executable', executable], check=True)


def prepare(entry, home, explicit=None, offline=False):
    if entry.get('availability') != 'ready' or not entry.get('bundle'):
        raise ValueError('This checkpoint is not admitted for an interview.')
    backend = entry['backend']
    executable = native.executable(backend, explicit)
    proof = entry['bundle'].get('proof', {})
    if proof and proof.get('bundle_sha256') != entry['bundle']['sha256']:
        raise ValueError('Runtime proof belongs to another bundle.')
    native.validate_runtime(executable, entry['cli_version'], proof)
    if entry.get('original_source') and not offline:
        recipe = originals.load(entry)
        for tool in ('git', 'gh'):
            if not shutil.which(tool):
                raise ValueError('Install '+tool+' first, then run the same command again. See the full setup instructions.')
        if any(item.get('format') == 'tar-zstd' for item in recipe['git_files'].values()):
            try:
                import zstandard  # noqa: F401
            except ImportError:
                if sys.prefix == sys.base_prefix:
                    raise ValueError('Use the website setup command to install the archive reader in a private Python environment.')
                print('Installing the archive reader in the private launcher environment.', flush=True)
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'zstandard'], check=True)
        access = subprocess.run(['gh', 'api', 'repos/'+recipe['repository'], '--silent'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        if access.returncode:
            signed_in = subprocess.run(['gh', 'auth', 'status', '--hostname', 'github.com'],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            if signed_in.returncode:
                print('Sign in to GitHub for the original checkpoint files.', flush=True)
                subprocess.run(['gh', 'auth', 'login', '--hostname', 'github.com', '--web', '--git-protocol', 'https'], check=True)
            access = subprocess.run(['gh', 'api', 'repos/'+recipe['repository'], '--silent'],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            if access.returncode:
                raise ValueError('GitHub access to '+recipe['repository']+' failed. Check your access and connection, then run the same command again.')
    ensure_login(backend, executable, home)
    return executable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint')
    parser.add_argument('--home', type=Path, default=interview.DEFAULT_HOME)
    parser.add_argument('--executable')
    parser.add_argument('--bundle', type=Path)
    args = parser.parse_args()
    catalog = json.loads((Path(__file__).parent/'catalog.json').read_text())
    entry = next((row for row in catalog['checkpoints'] if row['id'] == args.checkpoint), None)
    if entry is None:
        parser.error('Unknown checkpoint. Copy the command from its Chat Locally page.')
    try:
        home = interview.private_home(args.home)
        executable = prepare(entry, home, args.executable, offline=bool(args.bundle))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error)+'\nNo interview was started.\n')
    command = [sys.executable, '-m', 'website.interview', '--home', str(home),
               'launch', args.checkpoint, '--executable', executable]
    if args.bundle:
        command += ['--bundle', str(args.bundle.expanduser().resolve())]
    print('Opening the private interview page. No model turn begins until you ask a question.', flush=True)
    os.execv(sys.executable, command)


if __name__ == '__main__':
    main()
