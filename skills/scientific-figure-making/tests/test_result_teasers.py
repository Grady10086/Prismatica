"""Check image preservation, crop isolation, and required provenance."""
import base64
import importlib.util
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest

SCRIPT = Path(__file__).parents[1] / 'examples' / 'result_teasers.py'
spec = importlib.util.spec_from_file_location('result_teasers', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKhQAAAAASUVORK5CYII=')


def test_embedded_pixels_and_independent_crops(tmp_path):
    image = tmp_path / 'pixel.png'
    image.write_bytes(PNG)
    board = module.Board('Input < Output')
    asset = {'path': image, 'size': [1, 1]}
    board.image(asset, 0, 0, 200, 100)
    board.image(asset, 200, 0, 100, 200, [0, 0, .5, 1])
    svg = board.finish('Author & source', 'PROJECT RESULTS')
    root = ET.fromstring(svg)
    ns = {'s': 'http://www.w3.org/2000/svg'}
    images = root.findall('.//s:image', ns)
    clips = root.findall('.//s:clipPath', ns)
    assert len({c.attrib['id'] for c in clips}) == 2
    for image, clip in zip(images, clips):
        assert base64.b64decode(image.attrib['href'].split(',')[1]) == PNG
        assert image.attrib['clip-path'] == f"url(#{clip.attrib['id']})"
    assert root.find('s:title', ns).text == 'Input < Output'
    assert root.findall('.//s:text', ns)[0].text == 'Author & source'


@pytest.mark.parametrize('crop', [[-1, 0, 1, 1], [0, 0, 2, 1], [0, 0, 0, 1]])
def test_reject_out_of_bounds_crop(tmp_path, crop):
    image = tmp_path / 'pixel.png'
    image.write_bytes(PNG)
    with pytest.raises(ValueError, match='Crop outside image'):
        module.Board('Test').image({'path': image, 'size': [1, 1]}, 0, 0, 20, 20, crop)


def test_cli_requires_explicit_result_origin(tmp_path, monkeypatch):
    manifest = tmp_path / 'input.json'
    manifest.write_text('{"layout": "editing-atlas", "kind": "unspecified"}')
    out = tmp_path / 'output'
    monkeypatch.setattr('sys.argv', ['result_teasers.py', str(manifest), '--out', str(out)])
    with pytest.raises(ValueError, match='Declare whether'):
        module.main()
    assert not out.exists()
