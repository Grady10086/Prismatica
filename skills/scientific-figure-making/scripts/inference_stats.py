"""Scoped demo primitives: BH, overrepresentation and independent-effect REML."""
import numpy as np
from scipy.stats import hypergeom
from scipy.optimize import minimize_scalar


def bh(p):
    p=np.asarray(p,float)
    if p.ndim!=1 or not len(p) or not np.isfinite(p).all() or ((p<0)|(p>1)).any():raise ValueError('Finite p-values within 0–1 required')
    order=np.argsort(p);q=np.empty_like(p);q[order]=np.minimum(1,np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1]);return q


def ora(background,query,sets):
    bg=set(background);query=set(query)
    if not bg or not query<=bg:raise ValueError('Query must be a subset of a nonempty background')
    values=[]
    for name,items in sets.items():
        items=set(items)
        if not items or not items<=bg:raise ValueError('Each nonempty set must belong to tested background')
        k=len(query&items);values.append(dict(name=name,size=len(items),hits=k,p=float(hypergeom.sf(k-1,len(bg),len(items),len(query)))))
    for v,q in zip(values,bh([v['p'] for v in values])):v['q']=float(q)
    return values


def meta(y,se):
    y,se=np.asarray(y,float),np.asarray(se,float)
    if y.ndim!=1 or len(y)<3 or y.shape!=se.shape or not np.isfinite(y).all() or not np.isfinite(se).all() or (se<=0).any():raise ValueError('At least three independent effects and positive finite standard errors required')
    v=se**2
    def objective(tau):
        w=1/(v+tau);mu=np.sum(w*y)/sum(w);return .5*(np.log(v+tau).sum()+np.log(sum(w))+np.sum(w*(y-mu)**2))
    upper=max(1.,float(np.var(y)*4))
    for _ in range(10):
        fit=minimize_scalar(objective,bounds=(0,upper),method='bounded')
        if fit.x<upper*.95:break
        upper*=4
    else:raise ValueError('REML search failed to bracket heterogeneity')
    tau=0. if objective(0)<=fit.fun else float(fit.x);w=1/(v+tau);mu=float(sum(w*y)/sum(w));err=float(np.sqrt(1/sum(w)));wf=1/v;common=float(sum(wf*y)/sum(wf))
    return dict(mean=mu,se=err,ci=[mu-1.95996398454*err,mu+1.95996398454*err],tau2=tau,weights=(w/sum(w)).tolist(),common=common,common_se=float(np.sqrt(1/sum(wf))))
