"""Statistical primitives for rich figures; densities are descriptive, never CIs."""
import numpy as np
from scipy.stats import gaussian_kde, rankdata


def sample(values):
    a=np.asarray(values,dtype=float)
    if a.ndim!=1 or len(a)<2 or not np.isfinite(a).all():
        raise ValueError('Expected at least two finite observations')
    return a


def density(values, points=160):
    a=sample(values)
    if np.ptp(a)==0:
        return np.array([a[0]]),np.array([0.])
    x=np.linspace(a.min(),a.max(),points)
    return x,gaussian_kde(a)(x)


def paired_effect(before,after,*,seed=42,resamples=5000):
    a,b=sample(before),sample(after)
    if a.shape!=b.shape:
        raise ValueError('Paired observations must have matching lengths')
    if resamples<100: raise ValueError('Use at least 100 resamples')
    d=b-a
    rng=np.random.default_rng(seed)
    boot=d[rng.integers(0,len(d),(resamples,len(d)))].mean(axis=1)
    return float(d.mean()),np.quantile(boot,[.025,.975]),boot


def ranks(scores):
    a=np.asarray(scores,dtype=float)
    if a.ndim!=2 or not np.isfinite(a).all():
        raise ValueError('Expected a finite benchmark-by-method matrix')
    return rankdata(-a,axis=1,method='average')


def bubble_areas(counts,scale=.36):
    a=np.asarray(counts,dtype=float)
    if not np.isfinite(a).all() or (a<0).any():
        raise ValueError('Counts must be finite and nonnegative')
    return a*scale
