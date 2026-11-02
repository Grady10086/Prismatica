"""CLI checks for domain templates and portable local-image embedding."""
import base64
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

SCRIPT=Path(__file__).resolve().parents[1]/'examples/domain_teasers.py'
SVG='{http://www.w3.org/2000/svg}'
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j3YQAAAAASUVORK5CYII=')


def run(tmp_path, assets=None):
    palette=tmp_path/'palette.json'
    palette.write_text(json.dumps({'theme':'synthetic','hues':{
        'ours':{'anchor':'#245678'},'base1':{'anchor':'#AB5678'}}}))
    args=[sys.executable,str(SCRIPT),'--out',str(tmp_path/'out'),'--tokens',str(palette)]
    if assets is not None:
        manifest=tmp_path/'assets.json';manifest.write_text(json.dumps(assets))
        args+=['--assets',str(manifest)]
    return subprocess.run(args,capture_output=True,text=True)


def test_four_distinct_editable_templates(tmp_path):
    result=run(tmp_path)
    assert result.returncode==0,result.stderr
    paths=list((tmp_path/'out').glob('*.svg'))
    assert {p.stem for p in paths}=={'multimodal-grounding','conditional-generation',
                                    'controlled-generation','robot-action-loop'}
    for path in paths:
        root=ET.parse(path).getroot()
        assert root.attrib['width']=='183mm'
        assert list(root.iter(SVG+'text'))
        assert '#245678' in path.read_text()
    assert len({ET.parse(p).getroot().find(SVG+'title').text for p in paths})==4


def test_relative_local_images_are_embedded_without_distortion(tmp_path):
    (tmp_path/'observation.png').write_bytes(PNG)
    result=run(tmp_path,{'robot_observation':'observation.png','multimodal_output':'observation.png'})
    assert result.returncode==0,result.stderr
    root=ET.parse(tmp_path/'out/robot-action-loop.svg').getroot()
    images=list(root.iter(SVG+'image'))
    assert len(images)==1
    data=images[0].attrib['href']
    assert data.startswith('data:image/png;base64,')
    assert base64.b64decode(data.split(',',1)[1])==PNG
    assert images[0].attrib['preserveAspectRatio']=='xMidYMid meet'
    mm=(tmp_path/'out/multimodal-grounding.svg').read_text()
    assert 'The cup is left of the bowl.' not in mm
    provenance=json.loads((tmp_path/'out/provenance.json').read_text())
    assert provenance['supplied_image_slots']==['multimodal_output','robot_observation']


def test_unsupported_slot_does_not_write_outputs(tmp_path):
    result=run(tmp_path,{'unknown':'missing.png'})
    assert result.returncode!=0
    assert not (tmp_path/'out').exists()


def test_invalid_image_does_not_write_outputs(tmp_path):
    (tmp_path/'not-an-image.png').write_text('not a raster image')
    result=run(tmp_path,{'robot_observation':'not-an-image.png'})
    assert result.returncode!=0
    assert not (tmp_path/'out').exists()
