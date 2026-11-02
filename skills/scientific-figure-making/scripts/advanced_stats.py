"""Descriptive synthetic-demo primitives: 4PL fitting and right-censored KM."""
import numpy as np
from scipy.optimize import curve_fit


def hill(logdose,bottom,top,logec50,slope):
    return bottom+(top-bottom)/(1+10**((logec50-np.asarray(logdose))*slope))


def fit_dose(logdose,response):
    x,y=np.asarray(logdose,float),np.asarray(response,float)
    if x.shape!=y.shape or x.ndim!=1 or not np.isfinite(x).all() or not np.isfinite(y).all() or len(np.unique(x))<5:raise ValueError('At least five distinct finite doses with matched responses required')
    pars,_=curve_fit(hill,x,y,p0=[0,100,np.median(x),1],bounds=([-30,50,x.min(),.1],[40,130,x.max(),5]),maxfev=5000)
    return pars


def km(time,event):
    t=np.asarray(time,float);e=np.asarray(event)
    if t.ndim!=1 or not len(t) or t.shape!=e.shape or not np.isfinite(t).all() or (t<=0).any() or not np.isin(e,[0,1]).all():raise ValueError('Positive finite times and binary event indicators required')
    values=[0.];surv=[1.];lower=[1.];upper=[1.];s=1.;g=0.
    for u in np.unique(t):
        n=np.sum(t>=u);d=np.sum((t==u)&(e==1));s*=1-d/n
        if 0<s<1:
            g+=d/(n*(n-d));se=np.sqrt(g)/abs(np.log(s));a=np.log(-np.log(s));lo=np.exp(-np.exp(a+1.95996398454*se));hi=np.exp(-np.exp(a-1.95996398454*se))
        else:lo=hi=s
        values.append(float(u));surv.append(s);lower.append(lo);upper.append(hi)
    return tuple(np.array(v) for v in [values,surv,lower,upper])


def at_risk(time,points):
    t=np.asarray(time,float);return np.array([(t>=u).sum() for u in points])
