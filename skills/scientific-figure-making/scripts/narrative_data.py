"""Input-variant contracts; all changes are explicit and preserve array identity."""
import numpy as np


def variant(image,kind,amount):
    a=np.asarray(image,float)
    if a.shape!=(8,8) or not np.isfinite(a).all() or ((a<0)|(a>16)).any():raise ValueError('Finite 8×8 digit pixels within 0–16 required')
    b=a.copy()
    if kind=='occlusion':
        if not 0<=amount<=1:raise ValueError('Occlusion must be in 0–1')
        b[2:6,2:6]*=1-amount
    elif kind=='contrast':
        if not 0<=amount<=1:raise ValueError('Contrast must be in 0–1')
        b*=amount
    elif kind=='shift':
        if amount!=int(amount) or not 0<=amount<=7:raise ValueError('Shift must be an integer in 0–7')
        b=np.zeros_like(a);n=int(amount)
        if n:b[:,n:]=a[:,:-n]
        else:b=a.copy()
    else:raise ValueError('Unknown variant kind')
    return b


def corrupt(images,noise,sigma,occlusion):
    a=np.asarray(images,float);n=np.asarray(noise,float)
    if a.ndim!=3 or a.shape[1:]!=(8,8) or a.shape!=n.shape or not np.isfinite(a).all() or not np.isfinite(n).all() or not np.isfinite(sigma) or sigma<0 or not 0<=occlusion<=1:raise ValueError('Matched finite image/noise arrays and valid levels required')
    b=a.copy();b[:,2:6,2:6]*=1-occlusion
    return np.clip(b+sigma*n,0,16)
