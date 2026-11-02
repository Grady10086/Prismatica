"""Geometric contracts for compositional and spatial plotting."""
import numpy as np


def ternary_xy(parts):
    a=np.asarray(parts,float)
    if a.ndim!=2 or a.shape[1]!=3 or not np.isfinite(a).all() or (a<0).any() or not np.allclose(a.sum(axis=1),1,atol=1e-8,rtol=0):raise ValueError('Three nonnegative finite fractions summing to one required; normalize explicitly upstream')
    return np.c_[a[:,1]+a[:,2]/2,np.sqrt(3)*a[:,2]/2]


def field(x,y):
    x,y=np.asarray(x),np.asarray(y)
    return .12+.08*np.pi*np.sin(np.pi*x)*np.cos(np.pi*y),-.08*np.pi*np.cos(np.pi*x)*np.sin(np.pi*y)


def crop_mask(xy,bounds):
    a=np.asarray(xy,float);b=np.asarray(bounds,float)
    if a.ndim!=2 or a.shape[1]!=2 or not np.isfinite(a).all() or b.shape!=(4,) or not np.isfinite(b).all() or not (b[0]<b[1] and b[2]<b[3]):raise ValueError('Finite point coordinates and ordered xmin,xmax,ymin,ymax required')
    return (a[:,0]>=b[0])&(a[:,0]<=b[1])&(a[:,1]>=b[2])&(a[:,1]<=b[3])
