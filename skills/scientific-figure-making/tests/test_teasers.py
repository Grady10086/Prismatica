"""Exercise the gallery CLI with an exported palette, without user color registries."""
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / 'examples/teaser_gallery.py'


def test_exported_palette_and_editable_svg(tmp_path):
    tokens = tmp_path / 'tokens.json'
    tokens.write_text(json.dumps({'theme':'synthetic', 'hues':{
        'ours':{'anchor':'#245678'}, 'base1':{'anchor':'#AB5678'}}}))
    output = tmp_path / 'gallery'
    result = subprocess.run([sys.executable,str(SCRIPT),'--out',str(output),
                             '--tokens',str(tokens)],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
    files = list(output.glob('*.svg'))
    assert len(files) == 3
    for path in files:
        root = ET.parse(path).getroot()
        assert root.attrib['viewBox'] == '0 0 1600 660'
        assert root.attrib['width'] == '183mm'
        assert list(root.iter('{http://www.w3.org/2000/svg}text'))
        assert list(root.iter('{http://www.w3.org/2000/svg}desc'))
        assert '#245678' in path.read_text()
        assert not list(root.iter('{http://www.w3.org/2000/svg}image'))
    provenance = json.loads((output/'provenance.json').read_text())
    assert provenance['palette'] == 'paper-colors theme: synthetic'


def test_bad_palette_fails_before_writing_gallery(tmp_path):
    tokens = tmp_path / 'bad.json'
    tokens.write_text(json.dumps({'theme':'invalid','hues':{
        'ours':{'anchor':'red'},'base1':{'anchor':'#123456'}}}))
    output = tmp_path / 'gallery'
    result = subprocess.run([sys.executable,str(SCRIPT),'--out',str(output),
                             '--tokens',str(tokens)],capture_output=True,text=True)
    assert result.returncode != 0
    assert not output.exists()
