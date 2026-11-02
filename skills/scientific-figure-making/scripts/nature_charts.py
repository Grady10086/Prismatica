"""Data-preserving statistical chart primitives; caller owns units and design.

Use nature_profile before constructing the figure. SD means sample standard
 deviation (ddof=1), not SEM, a confidence interval or predictive uncertainty.
No smoothing, significance tests, outlier deletion or resampling is automatic.
"""
from __future__ import annotations
from collections.abc import Mapping
import numpy as np
from matplotlib.colors import TwoSlopeNorm


def observations(values, *, minimum=2):
    a=np.asarray(values,dtype=float)
    if a.ndim!=1 or len(a)<minimum or not np.isfinite(a).all():
        raise ValueError(f'Expected at least {minimum} finite observations in one dimension')
    return a


def summarize(values):
    a=observations(values)
    return {'n':len(a),'mean':float(a.mean()),'sd':float(a.std(ddof=1))}


def comparison(ax, groups: Mapping, styles: Mapping, *, xlabel='Score (%)'):
    """Horizontal raw observations plus mean +/- SD; preserve supplied order."""
    result={}
    for i,(name,values) in enumerate(groups.items()):
        a=observations(values);s=summarize(a);result[name]=s
        color=styles[name]['color'];marker=styles[name].get('marker','o')
        offsets=np.linspace(-.12,.12,len(a))
        ax.scatter(a,i+offsets,s=9,color=color,alpha=.36,linewidths=0,zorder=2)
        ax.errorbar(s['mean'],i,xerr=s['sd'],fmt=marker,color=color,
                    markersize=4,capsize=2,elinewidth=.8,linewidth=.8,zorder=3)
    ax.set(yticks=range(len(groups)),yticklabels=list(groups),xlabel=xlabel)
    ax.invert_yaxis();ax.margins(y=.2)
    return result


def training(ax, steps, runs: Mapping, styles: Mapping, *, xlabel='Training steps (10³)',ylabel='Score (%)',legend=True):
    """One row per independent run; mean and pointwise +/- sample SD, unsmoothed."""
    x=observations(steps)
    if not np.all(np.diff(x)>0):raise ValueError('Training steps must be strictly increasing')
    result={}
    for name,values in runs.items():
        a=np.asarray(values,dtype=float)
        if a.ndim!=2 or a.shape[0]<2 or a.shape[1]!=len(x) or not np.isfinite(a).all():
            raise ValueError('Training arrays must be finite [runs >= 2, shared steps]')
        mean=a.mean(axis=0);sd=a.std(axis=0,ddof=1);sty=styles[name]
        for row in a:ax.plot(x,row,color=sty['color'],alpha=.15,linewidth=.35)
        ax.fill_between(x,mean-sd,mean+sd,color=sty['color'],alpha=.1,linewidth=0)
        ax.plot(x,mean,color=sty['color'],linestyle=sty.get('linestyle','-'),linewidth=.8,label=name)
        result[name]={'n':len(a),'mean':mean.tolist(),'sd':sd.tolist()}
    ax.set(xlabel=xlabel,ylabel=ylabel)
    if legend:ax.legend(loc='lower right',handlelength=1.8,labelspacing=.25)
    return result


def ablation(ax, deltas, rows, columns, *, cmap,vlim):
    """Mean paired differences [condition, dataset, unit]; all-NaN means missing.

    Compute deltas from matching unit IDs before calling. Paired design cannot be
    inferred from matrix shape. Missing measurements are never replaced with 0.
    """
    a=np.asarray(deltas,dtype=float)
    if a.ndim!=3 or a.shape[:2]!=(len(rows),len(columns)) or np.isinf(a).any():
        raise ValueError('Expected [condition, dataset, replicate] differences; no infinity')
    if not np.isfinite(vlim) or vlim<=0:raise ValueError('vlim must be finite and positive')
    count=np.isfinite(a).sum(axis=2)
    mean=np.divide(np.nansum(a,axis=2),count,out=np.full(count.shape,np.nan),where=count>0)
    if np.any(np.abs(mean[np.isfinite(mean)])>vlim):
        raise ValueError('Color limits would hide measured means; increase vlim')
    im=ax.imshow(np.ma.masked_invalid(mean),cmap=cmap,
                 norm=TwoSlopeNorm(vmin=-vlim,vcenter=0,vmax=vlim),aspect='auto')
    for i in range(len(rows)):
        for j in range(len(columns)):
            value=mean[i,j]
            label='NA' if not np.isfinite(value) else f'{value:+.1f}'
            # Keep text black; use a quiet white backing for dark heatmap cells.
            ax.text(j,i,label,ha='center',va='center',fontsize=6,color='black',
                    bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':.5})
    ax.set(xticks=range(len(columns)),xticklabels=columns,yticks=range(len(rows)),yticklabels=rows)
    ax.tick_params(length=0)
    return im,{'mean':mean.tolist(),'n':count.tolist()}


def distribution(ax, groups: Mapping, styles: Mapping, *, ylabel='Score (%)',seed=0):
    """Raw dots, median/IQR box, Tukey whiskers; optional KDE if n >= 10.

    Box outliers remain visible among raw dots. KDE is descriptive, not uncertainty.
    Randomness affects horizontal display positions only, never the observations.
    """
    rng=np.random.default_rng(seed);result={}
    for i,(name,values) in enumerate(groups.items()):
        a=observations(values);color=styles[name]['color']
        if len(a)>=10 and np.ptp(a)>0:
            violin=ax.violinplot([a],positions=[i],widths=.65,showextrema=False)
            for body in violin['bodies']:body.set(facecolor=color,edgecolor='none',alpha=.14)
        box=ax.boxplot([a],positions=[i],widths=.14,whis=1.5,showfliers=False,patch_artist=True,
                        medianprops={'color':'black','linewidth':.8},
                        boxprops={'facecolor':'white','edgecolor':'black','linewidth':.6},
                        whiskerprops={'color':'black','linewidth':.6},capprops={'color':'black','linewidth':.6})
        ax.scatter(i+rng.uniform(.16,.31,len(a)),a,s=7,color=color,alpha=.5,linewidths=0,zorder=3)
        result[name]={'n':len(a),'median':float(np.median(a)),
                      'q1':float(np.quantile(a,.25)),'q3':float(np.quantile(a,.75))}
    ax.set(xticks=range(len(groups)),xticklabels=list(groups),ylabel=ylabel)
    ax.margins(x=.22)
    return result


def paired(ax, before, after, *, names=('Baseline','Ours'),styles,ylabel='Score (%)'):
    """Matching rows are the same units; no independent-sample error bars."""
    a=observations(before);b=observations(after)
    if a.shape!=b.shape:raise ValueError('Paired observations must have matching units')
    for u,v in zip(a,b):ax.plot([0,1],[u,v],color='#A9ADB4',linewidth=.5,alpha=.65,zorder=1)
    for i,(name,data) in enumerate(zip(names,[a,b])):
        ax.scatter(np.full(len(data),i),data,s=10,color=styles[name]['color'],
                   marker=styles[name].get('marker','o'),linewidths=0,zorder=2)
    ax.set(xticks=[0,1],xticklabels=names,ylabel=ylabel,xlim=(-.3,1.3))
    return {'n_pairs':len(a),'difference':summarize(b-a)}


def pareto_mask(latency, score):
    """Minimize latency, maximize score; exact ties do not dominate each other."""
    x=observations(latency,minimum=1);y=observations(score,minimum=1)
    if x.shape!=y.shape or np.any(x<=0):raise ValueError('Need matching scores and positive latencies')
    return np.array([not np.any((x<=xx)&(y>=yy)&((x<xx)|(y>yy))) for xx,yy in zip(x,y)])


def pareto(ax, latency, score, names, styles, *, offsets=None):
    x=observations(latency);y=observations(score)
    if len(names)!=len(x):raise ValueError('One label is required per operating point')
    front=pareto_mask(x,y)
    order=np.flatnonzero(front)[np.argsort(x[front])]
    ax.plot(x[order],y[order],color='#777777',linestyle='--',linewidth=.6,zorder=1)
    for i,(xx,yy,name) in enumerate(zip(x,y,names)):
        sty=styles[name]
        ax.scatter(xx,yy,s=19,color=sty['color'],marker=sty.get('marker','o'),zorder=3)
        delta=(4,4) if offsets is None else offsets[i]
        ax.annotate(name,(xx,yy),xytext=delta,textcoords='offset points',fontsize=6,color='black')
    ax.set(xlabel='Latency (ms)',ylabel='Score (%)');ax.margins(x=.2,y=.18)
    return {'non_dominated':[names[i] for i in order], 'dominance':'latency min; score max'}
