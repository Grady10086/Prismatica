"""Six rich statistical compositions. Explicit synthetic demo; editable SVG/PNG.
Run with --demo --out PATH; for real measurements call the plotting functions
with your arrays, paired case identities and units, and replace demo captions.
"""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from nature_data_gallery import load_colors
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature
import rich_charts as stats

NAMES=['Ours','Base A','Base B','Base C']

def demo():
    r=np.random.default_rng(42026)
    before=r.normal(76,5,28);after=before+r.normal(4,3,28)
    x=r.normal(75,9,160);y=10+.88*x+r.normal(0,4,160)
    return dict(groups=[r.normal(m,s,48).tolist() for m,s in [(85,3),(79,5),(74,4)]],
        before=before.tolist(),after=after.tolist(),pair_ids=[f'case-{i}' for i in range(28)],
        x=x.tolist(),y=y.tolist(),
        scores=[[88,85,82,80],[80,86,82,84],[84,83,86,80],[85,84,82,86],[89,87,85,88]],
        bubble=r.uniform(72,94,(7,4)).tolist(),counts=r.integers(50,501,(7,4)).tolist(),
        ridges=[r.normal(m,s,70).tolist() for m,s in [(74,6),(80,5),(85,4),(88,3)]])

def clean(ax):
    ax.tick_params(length=2,pad=3)
    return ax

def title(ax,text): ax.set_title(text,loc='left',pad=12,fontweight='bold')

def rain(fig,slot,d,c):
    ax=clean(fig.add_subplot(slot));rng=np.random.default_rng(2)
    for i,v in enumerate(d['groups']):
        v=np.array(v);x,p=stats.density(v);col=c.style(i)['color']
        ax.fill_between(x,i+.09,i+.09+p/max(p.max(),1e-12)*.48,color=col,alpha=.22,lw=0)
        ax.plot(x,i+.09+p/max(p.max(),1e-12)*.48,color=col,lw=.8)
        ax.scatter(v,i-.15+rng.uniform(-.075,.075,len(v)),s=5,color=col,alpha=.6,lw=0)
        q=np.quantile(v,[.25,.5,.75]);ax.plot(q[[0,2]],[i,i],color='black',lw=3,solid_capstyle='round')
        ax.scatter(q[1],i,s=9,c='white',edgecolors='black',lw=.5,zorder=5)
        ax.text(99,i,f'n = {len(v)}',ha='right',va='center',fontsize=5.5)
    ax.set(yticks=range(3),yticklabels=NAMES[:3],xlabel='Score (%)',xlim=(60,100),ylim=(-.45,2.75))
    ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0);title(ax,'Distribution · raincloud')
    return ax

def effect(fig,slot,d,c):
    grid=slot.subgridspec(1,2,width_ratios=[1.25,1],wspace=.6)
    ax=clean(fig.add_subplot(grid[0]));b,a=np.array(d['before']),np.array(d['after'])
    ax.plot([0,1],np.vstack([b,a]),color='#B8BCC5',alpha=.55,lw=.45)
    for i,v in enumerate([b,a]):ax.scatter(np.full(len(v),i),v,s=9,color=c.style([1,0][i])['color'],zorder=3,lw=0)
    ax.set(xticks=[0,1],xticklabels=['Before','After'],ylabel='Score (%)',xlim=(-.3,1.3));title(ax,'Paired effect · estimation')
    e,ci,boot=stats.paired_effect(b,a);right=clean(fig.add_subplot(grid[1]))
    x,p=stats.density(boot);col=c.style(0)['color']
    right.fill_betweenx(x,0,p/max(p.max(),1e-12)*.6,color=col,alpha=.2,lw=0)
    right.plot(p/max(p.max(),1e-12)*.6,x,color=col,lw=.8)
    right.plot([-.13,-.13],ci,color='black',lw=1.5);right.scatter(-.13,e,c='black',s=15,zorder=3)
    right.axhline(0,color='#777777',ls=':',lw=.6)
    right.set(xlim=(-.4,.8),xticks=[],ylabel='Paired difference (pp)')
    right.text(.98,.98,f'{e:.1f} pp\n95% CI [{ci[0]:.1f}, {ci[1]:.1f}]',transform=right.transAxes,ha='right',va='top',fontsize=5.5)
    return ax

def joint(fig,slot,d,c):
    g=slot.subgridspec(2,2,height_ratios=[.24,1],width_ratios=[1,.24],hspace=.08,wspace=.08)
    ax=clean(fig.add_subplot(g[1,0]));top=fig.add_subplot(g[0,0],sharex=ax);side=fig.add_subplot(g[1,1],sharey=ax)
    x,y=np.array(d['x']),np.array(d['y']);col=c.style(0)['color']
    ax.scatter(x,y,s=7,alpha=.28,c=col,lw=0)
    xx,yy=np.mgrid[48:101:70j,48:101:70j];z=gaussian_kde(np.vstack([x,y]))(np.vstack([xx.ravel(),yy.ravel()])).reshape(xx.shape)
    ax.contour(xx,yy,z,levels=[.001,.003,.005],colors=[col],linewidths=.7)
    ax.plot([48,101],[48,101],color='#909090',ls=':',lw=.6)
    ax.set(xlim=(48,101),ylim=(48,101),xlabel='Measured score (%)',ylabel='Predicted score (%)')
    ax.text(.04,.94,f'r = {np.corrcoef(x,y)[0,1]:.2f}   n = {len(x)}',transform=ax.transAxes,va='top',fontsize=5.5)
    top.hist(x,bins=19,color=col,alpha=.5,lw=0);side.hist(y,bins=19,orientation='horizontal',color=col,alpha=.5,lw=0)
    top.axis('off');side.axis('off');title(top,'Joint density · marginal distributions')
    return top

def bubble(fig,slot,d,c):
    ax=clean(fig.add_subplot(slot));v=np.array(d['bubble']);n=np.array(d['counts']);yy,xx=np.indices(v.shape)
    sc=ax.scatter(xx.ravel(),yy.ravel(),s=stats.bubble_areas(n).ravel(),c=v.ravel(),cmap=c.cmap('sequential'),vmin=70,vmax=95,edgecolors='white',lw=.5)
    ax.set(xticks=range(4),xticklabels=NAMES,yticks=range(7),yticklabels=[f'Set {i+1:02}' for i in range(7)],xlim=(-.6,3.6),ylim=(6.6,-.6))
    ax.spines[['left','bottom']].set_visible(False);ax.tick_params(length=0)
    cb=fig.colorbar(sc,ax=ax,pad=.04,fraction=.04);cb.set_label('Accuracy (%)',fontsize=6);cb.ax.tick_params(labelsize=5,length=2)
    handles=[ax.scatter([],[],s=stats.bubble_areas([s])[0],color='#9096A1',lw=0) for s in [50,200,500]]
    ax.legend(handles,['50','200','500'],title='Cases · area',loc='upper center',bbox_to_anchor=(.5,-.13),ncol=3,fontsize=5,title_fontsize=5.5,handletextpad=.4,columnspacing=1.8,handlelength=2.5)
    title(ax,'Benchmark coverage · bubble matrix');return ax

def bump(fig,slot,d,c):
    ax=clean(fig.add_subplot(slot));r=stats.ranks(d['scores'])
    for i in range(4):
        st=c.style(i,redundant=True);ax.plot(range(5),r[:,i],color=st['color'],marker=st['marker'],ms=4,lw=1.3,label=NAMES[i])
    ax.set(xticks=range(5),xticklabels=[f'Task {i+1}' for i in range(5)],yticks=[1,2,3,4],ylim=(4.4,.6),ylabel='Rank (1 = best)')
    ax.legend(ncol=2,loc='upper center',bbox_to_anchor=(.5,-.18),fontsize=5.5)
    title(ax,'Relative ordering · rank trajectories');return ax

def ridge(fig,slot,d,c):
    ax=clean(fig.add_subplot(slot));cols=c.ramp('ours',4,lightest=2);curves=[stats.density(v) for v in d['ridges']];mx=max(p.max() for _,p in curves)
    for i,((x,p),v,col) in enumerate(zip(curves,d['ridges'],cols)):
        ax.fill_between(x,i,i+p/mx*1.2,color=col,alpha=.85,lw=0,zorder=i+2)
        ax.plot(x,i+p/mx*1.2,color='white',lw=.6,zorder=i+3)
        ax.scatter(v,np.full(len(v),i-.05),marker='|',s=8,c=col,lw=.4,zorder=10)
        q=np.quantile(v,[.05,.5,.95]);ax.plot(q[[0,2]],[i+.13,i+.13],c='black',lw=.6,zorder=15);ax.scatter(q[1],i+.13,s=8,c='white',edgecolors='black',lw=.4,zorder=16)
    ax.set(yticks=range(4),yticklabels=['Level 1','Level 2','Level 3','Level 4'],xlabel='Score (%)',xlim=(50,100),ylim=(-.35,4.4))
    ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0);title(ax,'Ordered distributions · ridgeline');return ax

PLOTS={'raincloud':rain,'paired-effect':effect,'joint-density':joint,'bubble-matrix':bubble,'rank-trajectories':bump,'ridgeline':ridge}

def save(fig,path):
    fig.text(.5,.012,'SYNTHETIC DEMONSTRATION · layout study, not experimental evidence',ha='center',fontsize=5,color='#555555')
    fig.savefig(path.with_suffix('.svg'));fig.savefig(path.with_suffix('.png'),dpi=250);plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',action='store_true',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--colors',type=Path);args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(args.out,args.colors);d=demo()
    (args.out/'input-data.json').write_text(json.dumps({'kind':'SYNTHETIC DEMONSTRATION','data':d},indent=2))
    for name,draw in PLOTS.items():
        fig=plt.figure(figsize=nature.figure_size('double' if name in ['paired-effect','bubble-matrix','rank-trajectories'] else 'single',height_mm=85))
        slot=fig.add_gridspec(1,1,left=.17 if name not in ['paired-effect','bubble-matrix','rank-trajectories'] else .12,right=.94,bottom=.23,top=.83)[0]
        draw(fig,slot,d,c);save(fig,args.out/name)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=170));grid=fig.add_gridspec(3,2,left=.10,right=.94,bottom=.11,top=.92,wspace=.62,hspace=.9)
    for i,(name,draw) in enumerate(PLOTS.items()):
        ax=draw(fig,grid[i//2,i%2],d,c);fig.text(.05 if i%2==0 else .52,[.955,.64,.325][i//2],'abcdef'[i],fontweight='bold',fontsize=8)
    save(fig,args.out/'rich-overview')
    e,ci,_=stats.paired_effect(d['before'],d['after'])
    (args.out/'computed-summaries.json').write_text(json.dumps({'paired_mean_pp':e,'paired_percentile_95_ci':ci.tolist(),'ranks':stats.ranks(d['scores']).tolist(),'pearson_r':float(np.corrcoef(d['x'],d['y'])[0,1])},indent=2))
    (args.out/'captions.txt').write_text('All data are deterministic synthetic examples (seed 42026). No significance tests.\nRaincloud: 48 cases per group; KDE (Scott bandwidth), raw points, median and IQR. Each density peak is normalized for shape comparison.\nEffect: 28 explicitly matched cases; mean paired difference, 95% percentile bootstrap CI; 5000 paired resamples, seed 42. Bootstrap density describes estimator variability.\nJoint: 160 paired cases; Pearson r; raw points and marginal histograms; KDE contours at density .001, .003, .005 (not probability-mass intervals). Identity line is a reference only.\nBubble: color fixed to 70–95% accuracy; marker area = .36 times evaluated case count; rows synthetic datasets.\nRank: descending accuracy, average ranks for ties. Lines guide ordering across discrete tasks, not temporal interpolation or effect magnitude.\nRidgeline: 70 cases per level; Scott KDE with common density scale, rugs show every observation; median dot and 5th–95th percentile data range (not confidence interval).\n')
    print(args.out)
if __name__=='__main__':main()
