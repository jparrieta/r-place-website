"""Open the published E2b workspace and original conversation from r-place Git.

No checkpoint archive or saved-state supplement is downloaded. This is the
published workspace, not the full original local filesystem. New interviews
are native Claude forks and never overwrite the saved conversation.
"""
import argparse
import datetime
import fcntl
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import types
import uuid

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / 'E2b-PUBLISHED-GIT.json').read_text())
package = types.ModuleType('handoff_runtime')
package.__path__ = [str(ROOT / 'code')]
sys.modules[package.__name__] = package
native = importlib.import_module('handoff_runtime.native')
originals = importlib.import_module('handoff_runtime.originals')


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT='0', GIT_LFS_SKIP_SMUDGE='1')
    return subprocess.check_output(
        ['git', '-c', 'core.hooksPath=' + os.devnull,
         '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false',
         '-c', 'gc.auto=0', '-C', str(repo), *args], env=env)


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()


def verify_checkout(repo):
    if git(repo, 'rev-parse', 'HEAD').decode().strip() != SPEC['commit']:
        raise ValueError('Existing checkout has another commit. Nothing was overwritten.')
    if git(repo, 'remote', 'get-url', 'origin').decode().strip() != 'https://github.com/' + SPEC['repository'] + '.git':
        raise ValueError('Existing checkout has another origin. Nothing was overwritten.')
    workspace = repo / SPEC['workspace_prefix']
    if workspace.is_symlink() or not workspace.resolve().is_relative_to(repo.resolve()):
        raise ValueError('Published workspace is outside the checkout.')
    rows = git(repo, 'ls-tree', '-rz', SPEC['commit'], '--', SPEC['workspace_prefix'])
    count = size = 0
    expected = set()
    for row in rows.split(b'\0'):
        if not row:
            continue
        header, raw_name = row.split(b'\t', 1)
        mode, kind, oid = header.decode().split()
        name = raw_name.decode()
        path = repo / name
        expected.add(path.relative_to(workspace).as_posix())
        if kind != 'blob' or not path.parent.resolve().is_relative_to(workspace.resolve()):
            raise ValueError('Unsupported Git member: ' + name)
        if mode == '120000':
            if not path.is_symlink():
                raise ValueError('Missing published link: ' + name)
            data = os.readlink(path).encode()
            if not path.resolve().is_relative_to(workspace.resolve()):
                raise ValueError('Published link escapes the workspace: ' + name)
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        elif mode in ('100644', '100755'):
            if path.is_symlink() or not path.is_file():
                raise ValueError('Missing published file: ' + name)
            n = path.stat().st_size
            h = hashlib.sha1(b'blob ' + str(n).encode() + b'\0')
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(4 * 1024**2), b''):
                    h.update(block)
            actual = h.hexdigest()
            if bool(path.stat().st_mode & 0o111) != (mode == '100755'):
                raise ValueError('Published executable mode changed: ' + name)
            size += n
        else:
            raise ValueError('Unsupported Git mode: ' + name)
        if actual != oid:
            raise ValueError('Published Git object differs: ' + name)
        count += 1
    actual = {p.relative_to(workspace).as_posix() for p in workspace.rglob('*')
              if p.is_symlink() or p.is_file()}
    if actual != expected:
        raise ValueError('Unlisted or missing files in the published workspace.')
    transcript = repo / SPEC['transcript']['path']
    if transcript.stat().st_size != SPEC['transcript']['size'] or sha256(transcript) != SPEC['transcript']['sha256']:
        raise ValueError('The E2b conversation differs from the validated original.')
    found = False
    with transcript.open() as stream:
        for line in stream:
            if line.strip() and json.loads(line).get('sessionId') == SPEC['session_id']:
                found = True
    if not found:
        raise ValueError('The E2b session identity is absent.')
    return workspace, transcript, {'tracked_members': count, 'regular_file_bytes': size,
                                 'all_git_objects_verified': True, 'transcript_sha256': sha256(transcript)}


def prepare(storage):
    if any((p / '.git').exists() for p in (storage, *storage.parents)):
        raise ValueError('Choose storage outside a Git checkout.')
    storage.mkdir(parents=True, exist_ok=True, mode=0o700)
    repo = storage / 'original-git'
    with (storage / 'prepare.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Another E2b preparation is running. No competing download started.') from None
        if not repo.exists():
            if shutil.disk_usage(storage).free < SPEC['minimum_free_bytes']:
                raise ValueError('Allow 22 GiB free for the checkout and reserve.')
            print('Downloading E2b directly from the pinned r-place Git commit.', flush=True)
            recipe = {**SPEC, 'git_files': {'selected-transcript': SPEC['transcript']}}
            originals.checkout(recipe, repo)
        print('Verifying every published Git file and the saved E2b conversation.', flush=True)
        workspace, transcript, checks = verify_checkout(repo)
        receipt = {
            'status': 'pass', 'source': 'published-git-workspace',
            'repository': SPEC['repository'], 'commit': SPEC['commit'],
            'session_id': SPEC['session_id'], **checks,
            'supplements_downloaded': 0, 'full_snapshot_equivalent': False,
            'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        (storage / 'PREPARED.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return workspace, transcript, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--storage', type=Path, default=Path.home() / 'rplace-checkpoint-interviews' / 'E2b-f275665')
    parser.add_argument('--login-home', type=Path, default=Path.home() / '.rplace-interviews' / 'login' / 'claude')
    parser.add_argument('--executable')
    parser.add_argument('--prepare-only', action='store_true', help='Verify files without login or a model call')
    args = parser.parse_args()
    if not shutil.which('git'):
        parser.error('Install Git first.')
    exe = None
    if not args.prepare_only:
        exe = native.executable('claude', args.executable)
        native.validate_runtime(exe, SPEC['cli_version'])
        help_text = subprocess.check_output([exe, '--help'], text=True)
        if any(flag not in help_text for flag in ('--restricted', '--safe-mode', '--system-prompt-snapshot')):
            raise ValueError('The recorded Claude isolation options are unavailable.')
    storage = args.storage.expanduser().resolve()
    workspace, transcript, receipt = prepare(storage)
    print(json.dumps(receipt, indent=2), flush=True)
    if args.prepare_only:
        print('Files ready. No login or model call was made.', flush=True)
        return
    login = args.login_home.expanduser().resolve()
    login.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        native.claude_environment(login, login)
    except ValueError:
        print('Sign in to Claude using the separate interview login.', flush=True)
        login_env = native.environment(login, 'claude')
        login_env['DISABLE_AUTOUPDATER'] = '1'
        subprocess.run([exe, 'auth', 'login'], env=login_env, check=True)
    fork = str(uuid.uuid4())
    private = storage / 'interviews' / fork
    home = private / 'home'
    home.mkdir(parents=True, mode=0o700)
    notice = native.NOTICE + (
        ' This interview uses the published E2b Git workspace. It is not the full '
        'original local filesystem. Older unpublished chats, local settings and '
        'bookkeeping are absent; RUN.json is its published version. State these '
        'limits when they affect an answer.')
    command = [exe, '--restricted', '--safe-mode', '--system-prompt-snapshot', 'off',
        '--tools', 'Read,Glob,Grep', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
        '--disable-slash-commands', '--settings', '{"disableAllHooks":true}',
        '--model', SPEC['model'], '--effort', SPEC['effort'],
        '--append-system-prompt', notice, '--permission-mode', 'plan',
        '--resume', str(transcript), '--fork-session', '--session-id', fork]
    (private / 'SESSION.json').write_text(json.dumps({
        'source_commit': SPEC['commit'], 'source_session': SPEC['session_id'],
        'fork_session': fork, 'source_transcript_sha256': SPEC['transcript']['sha256'],
        'source_kind': 'published-git-workspace', 'full_snapshot_equivalent': False,
    }, indent=2) + '\n')
    print('Opening E2b in Claude CLI. Ask your question when the prompt appears.', flush=True)
    env = native.claude_environment(home, login)
    env['DISABLE_AUTOUPDATER'] = '1'
    try:
        result = subprocess.run(command, cwd=workspace, env=env)
    finally:
        verify_checkout(storage / 'original-git')
    if result.returncode:
        raise ValueError('Claude exited unsuccessfully. The attempt was kept; no retry was made.')


try:
    main()
except (ValueError, OSError, subprocess.SubprocessError) as error:
    raise SystemExit(str(error) + '\nNo automatic retry was made.')
