"""Known-value checks and import contracts for the biological table compositors."""
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bioinformatics',ROOT/'skills/scientific-figure-making/scripts/bioinformatics.py')
bio=importlib.util.module_from_spec(spec);spec.loader.exec_module(bio)
ASSETS=ROOT/'skills/scientific-figure-making/assets/bioinformatics'

@pytest.mark.parametrize('kind',list(bio.SCHEMAS))
def test_exported_browser_fixtures_read_in_python(kind):
    rows=bio.read_table(ASSETS/f'{kind}.csv',kind)
    assert len(rows)>10
    assert bio.validate(rows,kind) is rows


def test_onco_missingness_and_cohort_identity():
    rows=[['P1','G1','WT','A'],['P1','G2','NA','A'],['P2','G1','missense','B'],['P2','G2','deletion','B']]
    bio.validate(rows,'oncoprint')
    with pytest.raises(ValueError):bio.validate(rows+[['P1','G2','missense','A']],'oncoprint')
    with pytest.raises(ValueError):bio.validate(rows[:-1],'oncoprint')
    bad=[r[:] for r in rows];bad[1][3]='B'
    with pytest.raises(ValueError):bio.validate(bad,'oncoprint')


def test_known_tree_distances_and_cycle():
    rows=[['r','','',0,'',None],['x','r','',.4,'',None],['a','r','Leaf A',.1,'A',1],['b','x','B',.2,'B',2],['c','x','C',.3,'B',3]]
    bio.validate(rows,'phylogeny');nodes,leaves=bio.tree_structure(rows)
    assert len(leaves)==3 and nodes['c']['distance']==pytest.approx(.7)
    rows[1][1]='b'
    with pytest.raises(ValueError):bio.validate(rows,'phylogeny')


def test_genomic_interval_limits_and_overlap():
    rows=[['chromosome','chr1',0,100,0,'',0,0,''],['chromosome','chr2',0,200,0,'',0,0,''],['gc','chr1',0,50,.4,'',0,0,'']]
    bio.validate(rows,'circos')
    with pytest.raises(ValueError):bio.validate(rows+[['gc','chr1',40,60,.5,'',0,0,'']],'circos')
    with pytest.raises(ValueError):bio.validate(rows+[['link','chr1',0,10,1,'chr2',0,201,'']],'circos')


def test_sashimi_explicit_counts_and_nonoverlapping_coverage():
    rows=[['exon','G',0,10,0,'E1'],['exon','G',20,30,0,'E2'],['coverage','S',0,10,3,''],['junction','S',10,20,4,'J']]
    bio.validate(rows,'sashimi')
    with pytest.raises(ValueError):bio.validate(rows+[['coverage','S',5,15,4,'']],'sashimi')
    with pytest.raises(ValueError):bio.validate(rows+[['coverage','T',0,10,4,'']],'sashimi')


def test_csv_preserves_quoted_and_unicode_names(tmp_path):
    path=tmp_path/'spots.csv';path.write_text('spot,x,y,cell_type,expression\n"细胞, A",0,1,Immune,2\nB,2,3,Stromal,0\n')
    rows=bio.read_table(path,'spatial')
    assert rows[0][0]=='细胞, A'
