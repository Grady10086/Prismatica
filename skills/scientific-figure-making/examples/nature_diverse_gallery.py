"""Spatial, temporal and set-overlap composites; explicit synthetic examples."""
import argparse,json,sys
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,ConnectionPatch
import numpy as np
from nature_data_gallery import load_colors
from nature_complex_gallery import heading,finish
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature


def pca(x):
    x=np.asarray(x,float)
    if x.ndim!=2 or min(x.shape)<2 or not np.isfinite(x).all():raise ValueError('Finite sample-by-feature matrix required')
    a=x-x.mean(axis=0);u,s,v=np.linalg.svd(a,full_matrices=False)
    if (s*s).sum()==0:raise ValueError('PCA requires nonconstant data')
    return u[:,:2]*s[:2],s[:2]**2/(s*s).sum()


def intersections(membership):
    a=np.asarray(membership)
    if a.ndim!=2 or not np.isin(a,[0,1]).all():raise ValueError('Binary membership required')
    return sorted(Counter(map(tuple,a.astype(int))).items(),key=lambda kv:(-kv[1],kv[0]))


def spatial(out,c):
    rng=np.random.default_rng(519);xy=rng.uniform(-1,1,(1600,2));xy=xy[(xy[:,0]**2+(xy[:,1]/.75)**2<1)&~((xy[:,0]>.5)&(xy[:,1]<-.2))]*500
    classes=np.digitize(xy[:,0]+.4*xy[:,1],[-130,130]);signal=np.exp(-((xy[:,0]-100)**2+(xy[:,1]-80)**2)/40000)+rng.normal(0,.08,len(xy));features=np.column_stack([xy/500,signal,np.sin(xy[:,0]/200)])+rng.normal(0,.15,(len(xy),4));pc,var=pca(features)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'f','Spatial context to local measurements','Synthetic spatial observations · matched identities across spatial and PCA views')
    g=fig.add_gridspec(3,3,left=.08,right=.94,bottom=.15,top=.84,width_ratios=[1.25,.65,.9],height_ratios=[1,.9,.65],wspace=.65,hspace=.65)
    ax=fig.add_subplot(g[:2,:2]);cols=[c.style(k)['color'] for k in range(3)];ax.scatter(*xy.T,s=5,c=[cols[k] for k in classes],lw=0,alpha=.8);ax.set_aspect('equal');ax.axis('off');ax.set_title('Spatial domains · full field',loc='left',fontweight='bold',fontsize=7)
    bounds=[-80,180,-80,160];rect=Rectangle((bounds[0],bounds[2]),260,240,fill=False,ec='black',lw=.7);ax.add_patch(rect);ax.plot([-420,-220],[-360,-360],c='black',lw=1.5);ax.text(-320,-395,'200 μm',ha='center',fontsize=5)
    zoom=fig.add_subplot(g[0,2]);mask=(xy[:,0]>=-80)&(xy[:,0]<=180)&(xy[:,1]>=-80)&(xy[:,1]<=160);sc=zoom.scatter(*xy[mask].T,s=12,c=signal[mask],cmap=c.cmap('sequential'),vmin=-.3,vmax=1.3,lw=0);zoom.set(xlim=(-80,180),ylim=(-80,160),xticks=[],yticks=[]);zoom.set_aspect('equal');zoom.set_title('Matched region · signal',loc='left',fontsize=6);fig.colorbar(sc,ax=zoom,fraction=.045,pad=.05,label='Signal (a.u.)',ticks=[0,1])
    fig.add_artist(ConnectionPatch(xyA=(180,160),coordsA=ax.transData,xyB=(-80,160),coordsB=zoom.transData,color='#777777',lw=.5,ls=':'))
    emb=fig.add_subplot(g[1,2]);emb.scatter(*pc.T,s=3,c=[cols[k] for k in classes],alpha=.5,lw=0);emb.set(xlabel=f'PC1 ({var[0]:.0%})',ylabel=f'PC2 ({var[1]:.0%})');emb.set_title('PCA · computed from four features',loc='left',fontsize=6)
    for k in range(3):
        e=fig.add_subplot(g[2,k]);v=np.sort(signal[classes==k]);e.step(v,np.arange(1,len(v)+1)/len(v),where='post',c=cols[k]);e.set(xlim=(-.3,1.3),ylim=(0,1),xlabel='Signal (a.u.)');e.set_title(f'Domain {k+1} · n = {len(v)}',loc='left',fontsize=6)
        if k==0:e.set_ylabel('Empirical CDF')
    finish(fig,out,'spatial-context');return dict(xy_um=xy.tolist(),domain=classes.tolist(),signal=signal.tolist(),pca_input=features.tolist(),pca_variance_ratio=var.tolist())


def temporal(out,c):
    rng=np.random.default_rng(520);t=np.linspace(-1,3,201);on=np.maximum(t,0);base=(1-np.exp(-on*5))*np.exp(-on*.8);runs=np.array([base*(1+rng.normal(0,.14))+rng.normal(0,.045,len(t)) for _ in range(30)])
    spikes=[]
    for i in range(40):spikes.append(t[rng.random(len(t))<(3+18*base)*(t[1]-t[0])].tolist())
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=130));heading(fig,'g','Event-aligned responses across scales','Synthetic observations · common time axis · stimulus onset at 0 s')
    g=fig.add_gridspec(3,3,left=.10,right=.94,bottom=.16,top=.83,width_ratios=[1,1,1.2],height_ratios=[1,.45,.85],wspace=.7,hspace=.65)
    raster=fig.add_subplot(g[0,:2]);raster.eventplot(spikes,colors=c.style(0)['color'],linewidths=.4,linelengths=.7);raster.axvline(0,c='black',lw=.6,ls=':');raster.set(xlim=(-1,3),ylabel='Synthetic unit',yticks=[0,20,39]);raster.tick_params(labelbottom=False);raster.set_title('Individual event times · 40 units',loc='left',fontsize=7,fontweight='bold')
    rate=fig.add_subplot(g[1,:2],sharex=raster);bins=np.linspace(-1,3,41);h,_=np.histogram(np.concatenate(spikes),bins=bins);rate.step((bins[:-1]+bins[1:])/2,h/(40*np.diff(bins)),where='mid',c=c.style(0)['color']);rate.set(ylabel='Rate (Hz)');rate.tick_params(labelbottom=False);rate.axvline(0,c='black',lw=.6,ls=':')
    trace=fig.add_subplot(g[2,:2],sharex=raster)
    for v in runs:trace.plot(t,v,c=c.style(1)['color'],alpha=.10,lw=.4)
    mu=runs.mean(axis=0);sd=runs.std(axis=0,ddof=1);trace.fill_between(t,mu-sd,mu+sd,color=c.style(1)['color'],alpha=.2,lw=0);trace.plot(t,mu,c=c.style(1)['color'],lw=1.1);trace.axvline(0,c='black',lw=.6,ls=':');trace.set(xlabel='Time from onset (s)',ylabel='Response (a.u.)');trace.text(.98,.95,'30 traces · mean ± SD',transform=trace.transAxes,ha='right',va='top',fontsize=5)
    phase=fig.add_subplot(g[:2,2]);u=np.linspace(0,2*np.pi,160)
    paths=[]
    for k in range(6):
        a=np.c_[np.sin(u)*(1+.05*k),np.sin(2*u)*.5+.08*k];paths.append(a.tolist());phase.plot(*a.T,c=c.style(2)['color'],alpha=.2+.1*k,lw=.7);phase.scatter(*a[0],s=8,c='black')
    phase.set(xlabel='Component 1 (a.u.)',ylabel='Component 2 (a.u.)');phase.set_title('Synthetic state trajectories',loc='left',fontsize=6);phase.text(.02,.02,'Separate synthetic trajectories',transform=phase.transAxes,fontsize=5)
    dist=fig.add_subplot(g[2,2]);peak=runs.max(axis=1);v=np.sort(peak);dist.step(v,np.arange(1,31)/30,where='post',c=c.style(1)['color']);dist.set(xlabel='Peak response (a.u.)',ylabel='Empirical CDF',ylim=(0,1));dist.set_title('One peak per trace',loc='left',fontsize=6)
    finish(fig,out,'temporal-evidence');return dict(time_s=t.tolist(),response_traces=runs.tolist(),event_times_s=spikes,illustrative_paths=paths,rate_bins_s=bins.tolist(),event_counts=h.tolist())


def overlap(out,c):
    rng=np.random.default_rng(521);m=rng.random((420,4))<np.array([.8,.7,.65,.6]);m[~m.any(axis=1),0]=True;items=intersections(m);counts=np.array([v for _,v in items]);patterns=np.array([k for k,_ in items]);sites=np.repeat(np.arange(3),30);intensity=rng.lognormal(2,.5,(90,8));intensity+=sites[:,None]*.15;pc,var=pca(np.log2(intensity))
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=135));heading(fig,'h','Feature coverage and sample-level distributions','420 synthetic features in a union · exclusive intersections · 90 independent synthetic samples')
    g=fig.add_gridspec(3,3,left=.10,right=.94,bottom=.17,top=.83,width_ratios=[1,1,.95],height_ratios=[.85,.55,1],wspace=.6,hspace=.6)
    top=fig.add_subplot(g[0,:2]);x=np.arange(len(items));top.vlines(x,0,counts,color='#BFC2CA',lw=1);top.scatter(x,counts,c=c.style(0)['color'],s=18);top.set(xlim=(-.6,len(items)-.4),ylabel='Features',xticks=[]);top.set_title('Exclusive intersections · all 15 nonempty combinations',loc='left',fontweight='bold',fontsize=7)
    for i,n in enumerate(counts):top.text(i,n+3,str(n),ha='center',fontsize=5)
    top.set_ylim(0,counts.max()+16)
    member=fig.add_subplot(g[1,:2]);member.scatter(*np.meshgrid(x,range(4)),s=9,c='#DDDFE5')
    for j,row in enumerate(patterns):
        active=np.where(row)[0];member.plot([j,j],[active.min(),active.max()],c=c.style(0)['color'],lw=.8);member.scatter(np.full(len(active),j),active,s=13,c=c.style(0)['color'])
    member.set(xlim=top.get_xlim(),ylim=(3.5,-.5),xticks=[],yticks=range(4),yticklabels=[f'Assay {i+1}' for i in range(4)]);member.tick_params(length=0);member.spines[['top','right','bottom','left']].set_visible(False)
    coverage=fig.add_subplot(g[:2,2]);angles=np.linspace(0,2*np.pi,5)
    for i in range(4):
        coverage.scatter(m[:,i].sum(),i,s=30,c=c.style(0)['color']);coverage.hlines(i,0,m[:,i].sum(),color='#BFC2CA',lw=.7);coverage.text(m[:,i].sum()+7,i,str(m[:,i].sum()),va='center',fontsize=5)
    coverage.set(xlim=(0,420),yticks=range(4),yticklabels=[f'Assay {i+1}' for i in range(4)],xlabel='Detected union features');coverage.invert_yaxis();coverage.set_title('Set sizes · memberships overlap',loc='left',fontsize=6)
    ec=fig.add_subplot(g[2,0]);scatter=fig.add_subplot(g[2,1]);coverage2=fig.add_subplot(g[2,2])
    for k in range(3):
        vals=np.sort(np.log2(intensity[sites==k]).mean(axis=1));col=c.style(k)['color'];ec.step(vals,np.arange(1,31)/30,where='post',c=col,label=f'Site {k+1}');scatter.scatter(*pc[sites==k].T,s=8,c=col,alpha=.6,lw=0)
        a=np.log2(intensity[sites==k]);q=np.quantile(a,[.1,.5,.9],axis=0);coverage2.plot(range(1,9),q[1],c=col,lw=.8);coverage2.fill_between(range(1,9),q[0],q[2],color=col,alpha=.10,lw=0)
    ec.set(xlabel='Mean log2 intensity (a.u.)',ylabel='Empirical CDF');ec.legend(fontsize=5,loc='upper left');scatter.set(xlabel=f'PC1 ({var[0]:.0%})',ylabel=f'PC2 ({var[1]:.0%})');coverage2.set(xlabel='Measured channel',ylabel='Log2 intensity (a.u.)',xticks=[1,4,8]);coverage2.set_title('Median and 10–90% data range',loc='left',fontsize=5.5)
    finish(fig,out,'overlap-quality');return dict(feature_membership=m.astype(int).tolist(),exclusive_patterns=patterns.tolist(),exclusive_counts=counts.tolist(),sample_site=sites.tolist(),intensity=intensity.tolist(),pca_variance_ratio=var.tolist())


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors)
    data={name:draw(a.out,c) for name,draw in [('spatial',spatial),('temporal',temporal),('overlap',overlap)]};(a.out/'data-and-summaries.json').write_text(json.dumps(dict(kind='SYNTHETIC DEMONSTRATION',seeds=[519,520,521],data=data),indent=2));print(a.out)
if __name__=='__main__':main()
