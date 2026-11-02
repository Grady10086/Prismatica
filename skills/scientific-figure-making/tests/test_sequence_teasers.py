"""Evidence-preservation checks for the six image-dense layouts."""
import base64
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import pytest

EXAMPLES = Path(__file__).parents[1] / 'examples'
sys.path.insert(0, str(EXAMPLES))
spec = importlib.util.spec_from_file_location('sequence_teasers', EXAMPLES / 'sequence_teasers.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKhQAAAAASUVORK5CYII=')
REF = {'asset': 'image'}


def fixture_manifest(layout):
    m = dict(layout=layout, title='Results < & >', category='TEST', kind='PROJECT RESULTS',
             source_label='Verified source', source_url='https://example.org/experiment',
             assets={'image': {'file': 'pixel.png', 'size': [1, 1]}})
    if layout == 'video-cinema': m.update(input=REF, detail=REF, frames=[REF]*4)
    elif layout == 'video-proofsheet': m['rows'] = [dict(label=str(i), frames=[REF]*4) for i in range(3)]
    elif layout == 'object-stage': m.update(input=REF, geometry=REF, hero=REF, normals=[REF]*2, colors=[REF]*2, gallery=[REF]*4)
    elif layout == 'geometry-comparison': m.update(columns=list('ABCDE'), objects=[dict(label=str(i), images=[REF]*5) for i in range(3)])
    else: m['tasks'] = [dict(label=str(i), frames=[REF]*5) for i in range(2 if layout == 'robot-diptych' else 4)]
    return m


@pytest.mark.parametrize('layout,count', [('video-cinema',7),('video-proofsheet',12),
    ('object-stage',11),('geometry-comparison',15),('robot-diptych',10),('task-mosaic',8)])
def test_render_keeps_pixels_and_crop_isolation(tmp_path,monkeypatch,layout,count):
    m = fixture_manifest(layout)
    (tmp_path/'pixel.png').write_bytes(PNG)
    src = tmp_path/'input.json';src.write_text(json.dumps(m))
    out = tmp_path/'output'
    monkeypatch.setattr(sys,'argv',['sequence_teasers.py',str(src),'--out',str(out)])
    mod.main()
    root = ET.parse(out/(layout+'.svg')).getroot()
    ns = {'s':'http://www.w3.org/2000/svg'}
    images = root.findall('.//s:image',ns)
    clips = root.findall('.//s:clipPath',ns)
    assert len(images) == 1
    uses = root.findall('.//s:use',ns)
    assert len(uses) == count
    assert len({c.attrib['id'] for c in clips}) == count
    assert base64.b64decode(images[0].attrib['href'].split(',')[1]) == PNG
    for use,c in zip(uses,clips):
        assert use.attrib['href'] == '#' + images[0].attrib['id']
        assert use.attrib['clip-path'] == f"url(#{c.attrib['id']})"
    assert root.find('s:title',ns).text == m['title']
    provenance = json.loads((out/(layout+'-provenance.json')).read_text())
    assert provenance['source_url'] == m['source_url']
    assert len(provenance['assets']['image']['sha256']) == 64
    if 'frames' in m: assert provenance['frames'] == m['frames']


@pytest.mark.parametrize('crop', [[0,0,2,1],[0,0,float('nan'),1],[0,0,-1,1]])
def test_bad_crop_never_creates_output(tmp_path,monkeypatch,crop):
    m = fixture_manifest('video-cinema');m['detail']={'asset':'image','crop':crop}
    (tmp_path/'pixel.png').write_bytes(PNG)
    src=tmp_path/'input.json';src.write_text(json.dumps(m));out=tmp_path/'output'
    monkeypatch.setattr(sys,'argv',['sequence_teasers.py',str(src),'--out',str(out)])
    with pytest.raises(ValueError,match='Crop'):mod.main()
    assert not out.exists()


def test_incomplete_sequence_is_rejected():
    m=fixture_manifest('video-cinema');m['frames']=[REF]*3
    with pytest.raises(ValueError,match='four ordered samples'):mod.validate_refs(m)


def test_intact_overview_keeps_source_sheet_unsplit(tmp_path, monkeypatch):
    m = fixture_manifest('geometry-comparison')
    del m['objects']
    m.update(overview=REF,column_centers=[.07,.25,.47,.68,.9])
    (tmp_path/'pixel.png').write_bytes(PNG)
    src=tmp_path/'input.json';src.write_text(json.dumps(m));out=tmp_path/'output'
    monkeypatch.setattr(sys,'argv',['sequence_teasers.py',str(src),'--out',str(out)])
    mod.main()
    root=ET.parse(out/'geometry-comparison.svg').getroot()
    ns={'s':'http://www.w3.org/2000/svg'}
    assert len(root.findall('.//s:use',ns))==1
    audit=json.loads((out/'geometry-comparison-provenance.json').read_text())
    assert audit['overview']==m['overview']
