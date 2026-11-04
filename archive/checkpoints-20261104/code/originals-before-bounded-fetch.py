"""Restore original GitHub objects, with explicit saved-state supplements.

The recipe is pinned by the catalogue. GitHub supplies the research bytes from
an immutable commit. Supplements come from the previously published checkpoint,
and can fill only the exact paths declared by the recipe, never failed Git reads.
"""
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tarfile
import zipfile
import urllib.parse
from pathlib import Path

from . import bundles

SOURCE = Path(__file__).resolve().parent
FORMAT = 'rplace-original-github-map-v1'


def load(entry, source=SOURCE):
    declaration = entry['original_source']
    name = bundles.safe_name(declaration['recipe'])
    if not name.startswith('original-sources/'):
        raise ValueError('Original-source recipe is outside its declared folder')
    path = Path(source) / name
    if path.is_symlink() or path.stat().st_size > 32 * 1024**2 or not path.resolve().is_relative_to(Path(source).resolve()):
        raise ValueError('Invalid original-source recipe file')
    if bundles.digest(path) != declaration['sha256']:
        raise ValueError('Original-source recipe hash mismatch')
    recipe = validate(json.loads(path.read_text()), entry['id'])
    if recipe['tested_bundle_sha256'] != entry['bundle']['sha256']:
        raise ValueError('Original-source recipe and accepted checkpoint differ')
    return recipe


def validate(recipe, checkpoint):
    if recipe.get('format') != FORMAT or recipe.get('checkpoint_id') != checkpoint:
        raise ValueError('Wrong original-source recipe')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', recipe.get('repository', '')):
        raise ValueError('Invalid GitHub repository')
    if not re.fullmatch(r'[0-9a-f]{40}', recipe.get('commit', '')):
        raise ValueError('An immutable Git commit is required')
    if not re.fullmatch(r'[0-9a-f]{64}', recipe.get('tested_bundle_sha256', '')):
        raise ValueError('Missing accepted-checkpoint binding')
    manifest = bundles.validate_manifest(recipe['manifest'])
    if manifest['checkpoint_id'] != checkpoint:
        raise ValueError('Original manifest has another checkpoint identity')
    git_files, extras = recipe['git_files'], recipe['supplement_files']
    if set(git_files) & set(extras) or set(git_files) | set(extras) != set(manifest['files']):
        raise ValueError('Original source and supplement must partition the saved files')
    native_source = recipe.get('primary_transcript_source', 'git')
    if native_source not in ('git', 'supplement') or manifest['transcript'] not in (git_files if native_source == 'git' else extras):
        raise ValueError('The declared original analyst transcript source is absent')
    prefix = bundles.safe_name(recipe['workspace_prefix'].rstrip('/')) + '/'
    for destination, item in git_files.items():
        bundles.safe_name(destination)
        source = bundles.safe_name(item['path'])
        if not source.startswith(prefix) or not re.fullmatch(r'[0-9a-f]{40}', item.get('blob', '')):
            raise ValueError('Git source escapes the recorded checkpoint')
        if 'member' in item:
            bundles.safe_name(item['member'])
            if item.get('format') != 'tar-zstd':
                raise ValueError('Unknown original Git archive format')
    for name, item in extras.items():
        if {key: item[key] for key in ('sha256', 'size', 'mode')} != manifest['files'][name]:
            raise ValueError('Supplement differs from the saved manifest')
        if not item.get('reason'):
            raise ValueError('Every supplement needs an explicit reason')
    supplement = recipe['supplement']
    if supplement['format'] not in ('claude-snapshot-zip', 'interview-tar'):
        raise ValueError('Unknown saved-state supplement format')
    if not re.fullmatch(r'[0-9a-f]{64}', supplement.get('sha256', '')):
        raise ValueError('Missing supplement checksum')
    if type(supplement.get('bytes')) is not int or supplement['bytes'] <= 0:
        raise ValueError('Missing supplement size')
    parsed = urllib.parse.urlsplit(supplement['url'])
    if (parsed.scheme != 'https' or parsed.netloc != 'github.com' or parsed.query or parsed.fragment
            or not parsed.path.startswith('/' + recipe['repository'] + '/releases/download/')
            or len(parsed.path.split('/')) != 7):
        raise ValueError('Supplement must name its published GitHub release')
    return recipe


def download(recipe, cache):
    """Use the reader's existing gh login for a private release, never copy it."""
    spec = recipe['supplement']
    target = Path(cache) / spec['sha256']
    if target.exists():
        if target.stat().st_size != spec['bytes'] or bundles.digest(target) != spec['sha256']:
            raise ValueError('Cached supplement differs from its published checksum')
        return target
    gh = shutil.which('gh')
    if not gh or subprocess.run([gh, 'auth', 'status', '--hostname', 'github.com'],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30).returncode:
        return bundles.download(spec['url'], target, spec['sha256'], spec['bytes'])
    parts = urllib.parse.urlsplit(spec['url']).path.split('/')
    tag, asset = map(urllib.parse.unquote, parts[-2:])
    partial = target.with_suffix('.partial')
    target.parent.mkdir(parents=True, exist_ok=True)
    if partial.exists():
        raise ValueError('A partial supplement remains; inspect it before retrying')
    result = subprocess.run([gh, 'release', 'download', tag, '--repo', recipe['repository'],
                             '--pattern', asset, '--output', str(partial)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    if result.returncode:
        raise ValueError('Cannot download the saved-state supplement. Check GitHub access; any partial is retained.')
    if partial.stat().st_size != spec['bytes'] or bundles.digest(partial) != spec['sha256']:
        raise ValueError('Downloaded supplement differs from its published checksum')
    os.replace(partial, target)
    return target


def verify_identity(root, manifest):
    found = False
    with (root / manifest['transcript']).open('rb') as source:
        while line := source.readline(bundles.MAX_MANIFEST + 1):
            if len(line) > bundles.MAX_MANIFEST:
                raise ValueError('Native transcript line is too large')
            if not line.strip():
                continue
            row = json.loads(line)
            if manifest['backend'] == 'codex' and row.get('type') == 'session_meta':
                if row.get('payload', {}).get('id') != manifest['session_id']:
                    raise ValueError('Native transcript identity differs from manifest')
                found = True
            elif manifest['backend'] == 'claude' and row.get('sessionId') == manifest['session_id']:
                found = True
    if not found:
        raise ValueError('No matching native session in the transcript')


def checkout(recipe, destination):
    """Fetch one commit and the saved workspace, with no hooks or user filters."""
    root = Path(destination)
    root.mkdir(mode=0o700)
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update(GIT_TERMINAL_PROMPT='0', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_LFS_SKIP_SMUDGE='1')
    command = ['git', '-c', 'core.hooksPath=' + os.devnull, '-c', 'core.fsmonitor=false',
               '-c', 'core.autocrlf=false', '-c', 'credential.interactive=false']
    gh = shutil.which('gh')
    if gh:
        command += ['-c', 'credential.helper=!' + shlex.quote(gh) + ' auth git-credential']
    log = root.parent / 'original-git.log'

    def run(*args, text=None):
        with log.open('ab') as output:
            result = subprocess.run(command + list(args), cwd=root, env=env,
                                    input=text.encode() if text is not None else None,
                                    stdout=output, stderr=output, timeout=1800)
        if result.returncode:
            raise ValueError('Original GitHub fetch failed. No archive fallback was used; inspect original-git.log.')

    run('init', '--quiet')
    run('remote', 'add', 'origin', 'https://github.com/' + recipe['repository'] + '.git')
    run('fetch', '--depth=1', '--filter=blob:none', 'origin', recipe['commit'])
    run('sparse-checkout', 'init', '--cone')
    run('sparse-checkout', 'set', '--stdin', text=recipe['workspace_prefix'].rstrip('/') + '\n')
    run('checkout', '--detach', recipe['commit'])
    actual = subprocess.check_output(command + ['rev-parse', 'HEAD'], cwd=root, env=env, text=True).strip()
    if actual != recipe['commit']:
        raise ValueError('Fetched Git commit differs from the recipe')
    raw = subprocess.check_output(command + ['ls-tree', '-rz', actual, '--',
                                  recipe['workspace_prefix']], cwd=root, env=env)
    objects = {}
    for line in raw.split(b'\0'):
        if line:
            header, name = line.split(b'\t', 1)
            mode, kind, oid = header.decode().split()
            if kind == 'blob' and mode in ('100644', '100755'):
                objects[name.decode()] = oid
    for item in recipe['git_files'].values():
        if objects.get(item['path']) != item['blob']:
            raise ValueError('Original Git tree does not contain the declared file')
    return root


def put(stream, destination, expected):
    destination.parent.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    count = 0
    with destination.open('xb') as out:
        while data := stream.read(1024**2):
            count += len(data)
            if count > expected['size']:
                raise ValueError('Source file exceeds its saved size')
            h.update(data)
            out.write(data)
    if count != expected['size'] or h.hexdigest() != expected['sha256']:
        raise ValueError('Original file differs from its saved checkpoint: ' + destination.name)
    destination.chmod(expected['mode'])


def git_archive_files(recipe, original, destination):
    """Read selected members of unchanged archives at their original Git paths."""
    groups = {}
    for name, item in recipe['git_files'].items():
        if 'member' in item:
            groups.setdefault(item['path'], {}).setdefault(item['member'], []).append(name)
    if not groups:
        return
    try:
        import zstandard
    except ImportError as error:
        raise ValueError('Original community archives need zstandard: python3 -m pip install zstandard') from error
    for source_path, wanted in groups.items():
        path = original / source_path
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(original.resolve()):
            raise ValueError('Original Git archive is not a regular file')
        seen = set()
        with path.open('rb') as raw, zstandard.ZstdDecompressor().stream_reader(raw) as stream:
            with tarfile.open(fileobj=stream, mode='r|') as archive:
                for member in archive:
                    if member.name not in wanted:
                        continue
                    if member.name in seen or not member.isfile():
                        raise ValueError('Duplicate or invalid original archive member')
                    names = wanted[member.name]
                    expected = recipe['manifest']['files'][names[0]]
                    if member.size != expected['size']:
                        raise ValueError('Original archive member has the wrong size')
                    with archive.extractfile(member) as source:
                        put(source, destination / names[0], expected)
                    for name in names[1:]:
                        with (destination / names[0]).open('rb') as source:
                            put(source, destination / name, recipe['manifest']['files'][name])
                    seen.add(member.name)
        if seen != set(wanted):
            raise ValueError('Original Git archive is missing a declared member')


def supplements(recipe, archive, destination):
    """Read only declared exceptions from the original published checkpoint."""
    wanted = recipe['supplement_files']
    seen = set()

    def read_tar(stream, prefix=None, namespace=None):
        with tarfile.open(fileobj=stream, mode='r|gz') as inner:
            for member in inner:
                name = member.name.rstrip('/')
                bundles.safe_name(name)
                if prefix is not None:
                    if name == prefix:
                        continue
                    if not name.startswith(prefix + '/'):
                        raise ValueError('Unexpected snapshot archive root')
                    name = namespace + '/' + name[len(prefix) + 1:]
                if name not in wanted:
                    continue
                if name in seen or not member.isfile() or member.size != wanted[name]['size']:
                    raise ValueError('Duplicate or invalid saved-state supplement')
                with inner.extractfile(member) as source:
                    put(source, destination / name, wanted[name])
                seen.add(name)

    if recipe['supplement']['format'] == 'interview-tar':
        with Path(archive).open('rb') as stream:
            read_tar(stream)
    else:
        with zipfile.ZipFile(archive) as source:
            if len(source.namelist()) != len(set(source.namelist())):
                raise ValueError('Duplicate checkpoint ZIP member')
            for archive_name, prefix, namespace in [('fs.tar.gz', '00_GIVE-THE-AGENT', 'workspace'),
                                                      ('agent.tar.gz', '.cc', 'native')]:
                if any(name.startswith(namespace + '/') for name in wanted):
                    with source.open(archive_name) as stream:
                        read_tar(stream, prefix, namespace)
            for name, expected in wanted.items():
                if name.startswith('evidence/'):
                    with source.open(name[len('evidence/'):]) as stream:
                        put(stream, destination / name, expected)
                    seen.add(name)
    if seen != set(wanted):
        raise ValueError('Saved-state supplement is incomplete')


def restore(recipe, destination, cache, local_supplement=None):
    validate(recipe, recipe['checkpoint_id'])
    dest = Path(destination).resolve()
    if dest.exists():
        raise ValueError('Original-source restore requires a new destination')
    manifest = recipe['manifest']
    if any('member' in item for item in recipe['git_files'].values()):
        try:
            import zstandard
        except ImportError as error:
            raise ValueError('Original community archives need zstandard: python3 -m pip install zstandard') from error
    total = sum(item['size'] for item in manifest['files'].values())
    # One sparse checkout, one restored world and the compressed supplement.
    if shutil.disk_usage(dest.parent).free < 2 * total + recipe['supplement']['bytes'] + bundles.RESERVE:
        raise ValueError('Insufficient space for original-source restore plus reserve')
    original = checkout(recipe, dest.parent / 'original-git')
    dest.mkdir(mode=0o700)
    for name in sorted(manifest.get('directories', {})):
        (dest / name).mkdir(parents=True, exist_ok=True)
    for name, item in recipe['git_files'].items():
        if 'member' in item:
            continue
        source = original / item['path']
        if source.is_symlink() or not source.is_file() or not source.resolve().is_relative_to(original.resolve()):
            raise ValueError('Original Git source is not a regular file')
        with source.open('rb') as stream:
            put(stream, dest / name, manifest['files'][name])
    git_archive_files(recipe, original, dest)
    spec = recipe['supplement']
    if local_supplement:
        archive = Path(local_supplement)
        if archive.stat().st_size != spec['bytes'] or bundles.digest(archive) != spec['sha256']:
            raise ValueError('Local saved-state supplement differs from its published checksum')
    else:
        archive = download(recipe, cache)
    supplements(recipe, archive, dest)
    if bundles.inventory(dest) != manifest['files']:
        raise ValueError('Restored original-source files differ from the accepted checkpoint')
    verify_identity(dest, manifest)
    bundles.restore_links(dest, manifest.get('links', {}))
    for name, mode in sorted(manifest.get('directories', {}).items(), reverse=True):
        (dest / name).chmod(mode)
    if not (dest / 'workspace' / manifest.get('workspace_cwd', '.')).is_dir():
        raise ValueError('Original saved working directory is absent')
    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    receipt = {key: recipe[key] for key in ('repository', 'commit', 'checkpoint_id', 'tested_bundle_sha256')}
    receipt.update(git_files=len(recipe['git_files']), supplemental_files=len(recipe['supplement_files']),
                   primary_transcript_source=recipe.get('primary_transcript_source', 'git'),
                   supplement_url=spec['url'], supplement_sha256=spec['sha256'],
                   original_files_url='https://github.com/' + recipe['repository'] + '/tree/' + recipe['commit']
                                      + '/' + recipe['workspace_prefix'].rstrip('/'),
                   all_saved_files_hashes_and_modes_match=True, no_archive_fallback=True)
    (dest.parent / 'original-source-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    # This checkout was created by this restore, after its exact files verified.
    shutil.rmtree(original)
    return manifest
