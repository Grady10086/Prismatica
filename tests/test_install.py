import importlib.util
import json
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prismatica_install', ROOT / 'scripts/install_skills.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

def test_complete_suite_with_sibling_references(tmp_path):
    result = installer.install(tmp_path / 'skills')
    names = json.loads((ROOT / 'skills.json').read_text())['skills']
    assert result['installed'] == names
    for name in names:
        assert (tmp_path / 'skills' / name / 'SKILL.md').read_bytes() == (ROOT / 'skills' / name / 'SKILL.md').read_bytes()
    assert (tmp_path / 'skills/prismatica/assets/logo.svg').is_file()
    assert result['backup'] is None

def test_conflict_does_not_partially_install(tmp_path):
    dest = tmp_path / 'skills'
    (dest / 'paper-colors').mkdir(parents=True)
    sentinel = dest / 'paper-colors/my-data.txt'
    sentinel.write_text('keep')
    with pytest.raises(FileExistsError):
        installer.install(dest)
    assert sentinel.read_text() == 'keep'
    assert not (dest / 'prismatica').exists()

def test_replace_preserves_user_files_in_backup(tmp_path):
    dest = tmp_path / 'skills'
    installer.install(dest)
    (dest / 'paper-colors/custom.txt').write_text('user content')
    result = installer.install(dest, replace=True)
    assert (Path(result['backup']) / 'paper-colors/custom.txt').read_text() == 'user content'
    assert not (dest / 'paper-colors/custom.txt').exists()

def test_source_destination_rejected():
    with pytest.raises((ValueError, FileExistsError)):
        installer.install(ROOT / 'skills', replace=True)
