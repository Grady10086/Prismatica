"""Binary fixed-prediction evaluation contracts; no fitting or threshold tuning."""
import numpy as np


def validate(y,p):
    y,p=np.asarray(y),np.asarray(p,float)
    if y.ndim!=1 or not len(y) or p.shape!=y.shape or not np.isin(y,[0,1]).all() or not np.isfinite(p).all() or ((p<0)|(p>1)).any():raise ValueError('Matched binary labels and finite probabilities within 0–1 required')
    return y.astype(int),p


def calibration_bins(y,p,edges=None):
    y,p=validate(y,p);edges=np.linspace(0,1,11) if edges is None else np.asarray(edges,float)
    if edges.ndim!=1 or len(edges)<2 or edges[0]!=0 or edges[-1]!=1 or not np.isfinite(edges).all() or not (np.diff(edges)>0).all():raise ValueError('Strictly increasing bin edges from 0 to 1 required')
    ix=np.clip(np.searchsorted(edges,p,side='right')-1,0,len(edges)-2);result=[];z=1.95996398454
    for k in range(len(edges)-1):
        m=ix==k;n=int(m.sum())
        if not n:continue
        observed=float(y[m].mean());predicted=float(p[m].mean());den=1+z*z/n;center=(observed+z*z/(2*n))/den;radius=z*np.sqrt(observed*(1-observed)/n+z*z/(4*n*n))/den
        result.append(dict(bin=k,n=n,predicted=predicted,observed=observed,lo=0. if observed==0 else max(0.,center-radius),hi=1. if observed==1 else min(1.,center+radius)))
    ece=sum(v['n']*abs(v['predicted']-v['observed']) for v in result)/len(y)
    return result,float(ece),float(np.mean((p-y)**2))


def net_benefit(y,p,thresholds):
    y,p=validate(y,p);t=np.asarray(thresholds,float)
    if t.ndim!=1 or not np.isfinite(t).all() or ((t<=0)|(t>=1)).any():raise ValueError('Thresholds must lie strictly between 0 and 1')
    action=p[:,None]>=t[None,:];tp=((y[:,None]==1)&action).sum(axis=0);fp=((y[:,None]==0)&action).sum(axis=0)
    return tp/len(y)-fp/len(y)*t/(1-t)


def treat_all(y,t):
    y=np.asarray(y);t=np.asarray(t,float)
    if y.ndim!=1 or not len(y) or not np.isin(y,[0,1]).all() or t.ndim!=1 or not np.isfinite(t).all() or ((t<=0)|(t>=1)).any():raise ValueError('Binary labels and thresholds strictly between 0 and 1 required')
    rate=y.mean();return rate-(1-rate)*t/(1-t)
