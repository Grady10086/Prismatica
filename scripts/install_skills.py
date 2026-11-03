"""Install the complete Prismatica skill suite, preserving existing installations."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import tempfile
import uuid
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def install(destination: Path, *, replace: bool = False, root: Path = ROOT) -> dict:
    names = json.loads((root / 'skills.json').read_text())['skills']
    if not names or len(set(names)) != len(names):
        raise ValueError('Invalid skill manifest')
    for name in names:
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError('Invalid skill directory name')
        if not (root / 'skills' / name / 'SKILL.md').is_file():
            raise ValueError(f'Missing entrypoint: {name}')
    destination = destination.expanduser().resolve()
    conflicts = [name for name in names if (destination / name).exists() or (destination / name).is_symlink()]
    if conflicts and not replace:
        raise FileExistsError('Existing skills: ' + ', '.join(conflicts) + '. Use --replace to preserve backups and replace them.')
    # Refuse to replace the checkout's own skill folders.
    if any((root / 'skills' / name).resolve() == (destination / name).resolve() for name in names):
        raise ValueError('Destination must not be the source skills directory')
    destination.mkdir(parents=True, exist_ok=True)
    backup = destination / '.prismatica-backups' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8])
    installed, moved = [], []
    with tempfile.TemporaryDirectory(prefix='.prismatica-stage-', dir=destination) as staging:
        stage = Path(staging)
        for name in names:
            shutil.copytree(root / 'skills' / name, stage / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.pytest_cache', '.DS_Store'))
        try:
            for name in names:
                target = destination / name
                if target.exists() or target.is_symlink():
                    backup.mkdir(parents=True, exist_ok=True)
                    target.rename(backup / name)
                    moved.append(name)
                (stage / name).rename(target)
                installed.append(name)
        except Exception:
            for name in reversed(installed):
                shutil.rmtree(destination / name)
            for name in reversed(moved):
                (backup / name).rename(destination / name)
            raise
    return {'destination': str(destination), 'installed': installed,
            'backup': str(backup) if moved else None}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path.home() / '.codex' / 'skills')
    parser.add_argument('--replace', action='store_true', help='Preserve existing skill directories as backups before replacing')
    args = parser.parse_args()
    try:
        result = install(args.dest, replace=args.replace)
    except (ValueError, FileExistsError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
