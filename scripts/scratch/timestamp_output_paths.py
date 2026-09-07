"""Timestamp completed run paths, retaining original raw provenance. -- Codex/GPT-6"""

import argparse
import json
import re
import shlex
import subprocess
from datetime import datetime
from pathlib import Path


def main(apply: bool) -> None:
    root = Path.cwd()
    tasks = json.loads(subprocess.check_output(['pueue', 'status', '--json']))['tasks']
    starts = {}
    active = set()
    for task in tasks.values():
        if task['path'] != str(root):
            continue
        argv = shlex.split(task['command'])
        if '--output-dir' not in argv:
            continue
        path = Path(argv[argv.index('--output-dir') + 1])
        status = task['status']
        if 'Done' in status:
            starts[path] = status['Done']['start']
        else:
            active.add(path)
    mapping = []
    for old in sorted(Path('out').iterdir()):
        match = re.fullmatch(r'(\d{4}-\d{2}-\d{2})_(?!\d{6}(?:_|$))(.+)', old.name)
        if not old.is_dir() or not match or old in active:
            continue
        if old in starts:
            stamp = datetime.fromisoformat(starts[old])
            evidence = 'pueue job start'
        else:
            stamp = datetime.fromtimestamp(old.stat().st_mtime).astimezone()
            evidence = 'directory mtime estimate, not measured start'
        new = old.with_name(f'{stamp:%Y-%m-%d_%H%M%S}_{match[2]}')
        assert not new.exists(), new
        mapping.append({'old': str(old), 'new': str(new), 'timestamp_source': evidence})
    print(json.dumps(mapping, indent=2))
    if not apply:
        return
    for item in mapping:
        Path(item['old']).rename(item['new'])
    replacements = {item['old']: item['new'] for item in mapping}
    pattern = re.compile('|'.join(re.escape(key) for key in sorted(replacements, key=len, reverse=True)) + r'(?=[/\s\x22\x27`)\]]|$)') if replacements else None
    if pattern:
        files = subprocess.check_output(['rg', '--files', '--hidden', '-g', '!.git', '-g', '*.md', '-g', '*.py', '-g', 'justfile']).decode().splitlines()
        files += [str(path) for path in Path('out').glob('*/**/*.md')]
        for name in set(files):
            path = Path(name)
            if not path.exists() or 'human' in name.lower():
                continue
            original = path.read_text()
            updated = pattern.sub(lambda match: replacements[match[0]], original)
            if updated != original:
                path.write_text(updated)
    manifest = Path('slop/output-path-migration.json')
    manifest.write_text(json.dumps(mapping, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
