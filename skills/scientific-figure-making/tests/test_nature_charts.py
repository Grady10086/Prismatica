"""Check statistical meanings, missing observations and Pareto dominance."""
import importlib.util
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pytest

spec=importlib.util.spec_from_file_location('nature_charts',Path(__file__).parents[1]/'scripts/nature_charts.py')
charts=importlib.util.module_from_spec(spec);spec.loader.exec_module(charts)


@pytest.fixture
def ax():
    fig,axis=plt.subplots();yield axis;plt.close(fig)


def test_summary_is_sample_sd_not_sem():
    s=charts.summarize([1,2,3])
    assert s=={'n':3,'mean':2.,'sd':1.}


@pytest.mark.parametrize('bad',[[1],[1,np.nan],[1,np.inf],[[1,2],[3,4]]])
def test_invalid_observations_rejected(bad):
    with pytest.raises(ValueError):charts.summarize(bad)


def test_training_summary_uses_unsmoothed_shared_time_points(ax):
    raw=np.array([[0,10,2],[2,6,8]])
    s=charts.training(ax,[1,2,3],{'A':raw},{'A':{'color':'black'}})['A']
    np.testing.assert_array_equal(s['mean'],[1,8,5])
    np.testing.assert_allclose(s['sd'],raw.std(axis=0,ddof=1))
    assert s['n']==2


def test_training_does_not_guess_misaligned_steps(ax):
    with pytest.raises(ValueError,match='strictly increasing'):
        charts.training(ax,[1,3,2],{'A':[[1,2,3],[2,3,4]]},{'A':{'color':'black'}})


def test_missing_ablation_is_not_a_zero(ax):
    im,s=charts.ablation(ax,np.array([[[1,-1],[np.nan,np.nan]]]),['A'],['X','Y'],cmap='coolwarm',vlim=2)
    assert s['mean'][0][0]==0
    assert np.isnan(s['mean'][0][1])
    assert s['n']==[[2,0]]
    assert np.ma.getmaskarray(im.get_array()).tolist()==[[False,True]]


def test_ablation_cannot_silently_saturate_color_scale(ax):
    with pytest.raises(ValueError,match='hide measured means'):
        charts.ablation(ax,[[[3,5]]],['A'],['X'],cmap='coolwarm',vlim=2)


def test_pairing_is_not_silently_truncated(ax):
    with pytest.raises(ValueError,match='matching units'):
        charts.paired(ax,[1,2,3],[2,3],styles={})


def test_pairwise_differences_preserve_sign(ax):
    s=charts.paired(ax,[1,2,4],[2,2,3],names=('A','B'),styles={'A':{'color':'black'},'B':{'color':'blue'}})
    assert s['n_pairs']==3
    assert s['difference']=={'n':3,'mean':0.,'sd':1.}


def test_pareto_keeps_exact_ties_and_removes_dominated_points():
    np.testing.assert_array_equal(charts.pareto_mask([10,20,15,10],[.8,.9,.7,.8]),[True,True,False,True])


def test_pareto_rejects_nonpositive_latency():
    with pytest.raises(ValueError,match='positive latencies'):charts.pareto_mask([0,2],[.8,.9])


def test_distribution_retains_raw_outlier(ax):
    values=[1,1,2,2,100]
    charts.distribution(ax,{'A':values},{'A':{'color':'black'}})
    plotted=np.asarray(ax.collections[-1].get_offsets())[:,1]
    np.testing.assert_array_equal(plotted,values)
