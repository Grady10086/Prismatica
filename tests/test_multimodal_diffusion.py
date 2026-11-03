"""Check numerical semantics independently of the plotted summaries."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
import pytest
from scipy.special import logsumexp

@pytest.fixture
def plate(monkeypatch):
 path=Path(__file__).resolve().parents[1]/'skills/scientific-figure-making/examples'
 monkeypatch.syspath_prepend(str(path))
 spec=importlib.util.spec_from_file_location('mm_plate',path/'multimodal_diffusion_plate.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module

def test_score_matches_log_marginal_gradient(plate):
 x=np.array([[.3,-.7],[1.8,.2]]);sigma=.8;eps=1e-5
 def logdensity(v):return logsumexp(-np.sum((v[:,None,:]-plate.CENTRES[None])**2,axis=-1)/(2*(sigma*sigma+plate.SIGMA**2)),axis=1)
 gradient=np.column_stack([(logdensity(x+np.eye(2)[i]*eps)-logdensity(x-np.eye(2)[i]*eps))/(2*eps) for i in range(2)])
 assert np.allclose(plate.drift(x,sigma),-sigma*gradient,rtol=1e-7,atol=1e-8)

@pytest.mark.parametrize('method',['Euler','Heun','Midpoint'])
def test_budget_counts_score_evaluations(plate,monkeypatch,method):
 calls=[];original=plate.drift
 def counted(x,s):calls.append(s);return original(x,s)
 monkeypatch.setattr(plate,'drift',counted)
 result,path,s=plate.integrate(np.array([[1.,2.],[-1.,.4]]),16,method)
 assert len(calls)==16
 assert np.array_equal(result,path[-1])
 assert s[0]==3 and s[-1]==.01 and np.all(np.diff(s)<0)

@pytest.mark.parametrize('budget',[0,3])
def test_invalid_two_stage_budget(plate,budget):
 with pytest.raises(ValueError):plate.integrate(np.ones((2,2)),budget,'Heun')
