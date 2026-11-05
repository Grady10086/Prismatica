"""Independent set arithmetic and import validation."""
import importlib.util
from pathlib import Path

import pytest

SCRIPT=Path(__file__).resolve().parents[1]/'skills/scientific-figure-making/scripts/set_overlap.py'
spec=importlib.util.spec_from_file_location('set_overlap', SCRIPT)
sets=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sets)


def test_exact_masks_marginals_and_inclusive_pairs():
    data=sets.summarize(['a','b','c','d'], [[1,0,0],[0,1,0],[1,1,0],[1,1,1]], ['A','B','C'])
    assert data['union']==4 and data['core']==1
    assert data['totals']==[3,3,1]
    assert data['unique']==[1,1,0]
    assert data['degree']==[2,1,1]
    assert dict(data['intersections'])=={1:1,2:1,3:1,7:1}
    assert data['shared'][0][1]==2
    assert data['jaccard'][0][1]==.5
    assert data['jaccard'][0][2]==pytest.approx(1/3)


def test_duplicate_or_empty_items_rejected():
    with pytest.raises(ValueError):
        sets.summarize(['x','x'], [[1,0],[0,1]], ['A','B'])
    with pytest.raises(ValueError):
        sets.summarize(['x'], [[0,0]], ['A','B'])
    with pytest.raises(ValueError):
        sets.summarize(['x'], [[1,.5]], ['A','B'])


def test_string_ids_and_empty_sets(tmp_path):
    path=tmp_path/'genes.csv'
    path.write_text('item,Model X,Model Y,Model Z\ngene-α,1,0,0\ngene-β,1,0,0\n')
    ids,membership,names=sets.read_memberships(path)
    data=sets.summarize(ids,membership,names)
    assert ids==['gene-α','gene-β']
    assert data['totals']==[2,0,0]
    assert data['jaccard'][0][1]==0
    assert str(data['jaccard'][1][2])=='nan'


def test_demo_conservation():
    ids,membership,names=sets.demo_memberships()
    data=sets.summarize(ids,membership,names)
    assert sum(data['degree'])==data['union']==400
    assert sum(v for _,v in data['intersections'])==400
    assert sum(data['totals'])==sum((i+1)*v for i,v in enumerate(data['degree']))


def test_all_63_membership_patterns():
    rows=[[(mask>>j)&1 for j in range(6)] for mask in range(1,64)]
    data=sets.summarize(list(range(1,64)), rows, list('ABCDEF'))
    assert data['totals']==[32]*6
    assert data['unique']==[1]*6
    assert data['degree']==[6,15,20,15,6,1]
    assert data['core']==1
    assert data['jaccard'][0][1]==pytest.approx(1/3)
