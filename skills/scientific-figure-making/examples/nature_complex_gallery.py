"""Nature-informed composite studies. Synthetic data only; see complex-data.md."""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch,Rectangle
from matplotlib.colors import ListedColormap
import numpy as np
from scipy.cluster.hierarchy import linkage,dendrogram,leaves_list
from scipy.spatial.distance import squareform
from nature_data_gallery import load_colors
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature


def cluster_rows(x):
    x=np.asarray(x,float)
    if x.ndim!=2 or min(x.shape)<2 or not np.isfinite(x).all():raise ValueError('Finite 2D observations required')
    sd=x.std(axis=1,ddof=1)
    if (sd==0).any():raise ValueError('Constant rows cannot be standardized')
    z=(x-x.mean(axis=1,keepdims=True))/sd[:,None]
    return z,linkage(z,method='average',metric='euclidean',optimal_ordering=True)


def correlation_order(x):
    x=np.asarray(x,float)
    if x.ndim!=2 or not np.isfinite(x).all() or (x.std(axis=0)==0).any():raise ValueError('Finite nonconstant variables required')
    r=np.corrcoef(x,rowvar=False);dist=np.clip(1-r,0,2);dist=(dist+dist.T)/2;np.fill_diagonal(dist,0)
    tree=linkage(squareform(dist,checks=True),method='average',optimal_ordering=True)
    return r,tree


def flow_tables(records,sizes):
    a=np.asarray(records)
    if a.ndim!=2 or a.shape[1]!=len(sizes) or not np.issubdtype(a.dtype,np.integer):raise ValueError('One integer category per case and stage required')
    if any(((a[:,i]<0)|(a[:,i]>=n)).any() for i,n in enumerate(sizes)):raise ValueError('Category outside stage')
    return [np.bincount(a[:,i]*sizes[i+1]+a[:,i+1],minlength=sizes[i]*sizes[i+1]).reshape(sizes[i],sizes[i+1]) for i in range(len(sizes)-1)]


def demo():
    rng=np.random.default_rng(91);groups=np.repeat(np.arange(3),12)
    patterns=np.array([[1.4,-.3,-1],[-1,1.4,-.4],[-.4,-1,1.4]])
    x=patterns[np.repeat(np.arange(3),8)][:,groups]+rng.normal(0,.65,(24,36))
    latent=rng.normal(size=(160,3));load=np.repeat(np.eye(3),4,axis=0);load[4:8,0]=-.45
    features=latent@load.T+rng.normal(0,.6,(160,12))
    first=rng.choice(3,240,p=[.35,.4,.25]);mid=np.array([rng.choice(3,p=[[.7,.2,.1],[.2,.6,.2],[.1,.25,.65]][i]) for i in first]);last=np.array([rng.choice(3,p=[[.82,.13,.05],[.4,.45,.15],[.15,.3,.55]][i]) for i in mid]);records=np.column_stack([first,mid,last]);quality=np.clip(90-last*13+rng.normal(0,5,240),0,100)
    return dict(expression=x.tolist(),cohort=groups.tolist(),features=features.tolist(),records=records.tolist(),quality=quality.tolist())


def heading(fig,letter,title,subtitle):
    fig.text(.045,.954,letter,weight='bold',fontsize=8)
    fig.text(.085,.954,title,weight='bold',fontsize=9)
    fig.text(.085,.918,subtitle,fontsize=6,color='#555555')


def finish(fig,out,name):
    fig.text(.5,.025,'SYNTHETIC DEMONSTRATION · original layouts, not reproduced paper results',ha='center',fontsize=5,color='#666666')
    fig.savefig(out/(name+'.svg'));fig.savefig(out/(name+'.png'),dpi=220);plt.close(fig)


def heatmap(out,d,c):
    x=np.array(d['expression']);z,rt=cluster_rows(x);ct=linkage(z.T,method='average',metric='euclidean',optimal_ordering=True)
    ri,ci=leaves_list(rt),leaves_list(ct);group=np.array(d['cohort']);cols=[c.style(i)['color'] for i in range(3)]
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=130));heading(fig,'a','Clustered response atlas','24 features × 36 cases · row z-scores · average-linkage Euclidean clustering')
    g=fig.add_gridspec(4,4,left=.10,right=.93,bottom=.15,top=.85,width_ratios=[.17,1,.035,.40],height_ratios=[.18,.035,1,.19],wspace=.45,hspace=.20)
    top=fig.add_subplot(g[0,1]);dendrogram(ct,ax=top,no_labels=True,color_threshold=0,above_threshold_color='#555555');top.axis('off')
    left=fig.add_subplot(g[2,0]);dendrogram(rt,ax=left,orientation='left',no_labels=True,color_threshold=0,above_threshold_color='#555555');left.invert_yaxis();left.axis('off')
    for k,i in enumerate(ri):
        if k%3==0:left.text(-.08,1-(k+.5)/24,f'F{i+1:02}',transform=left.transAxes,ha='right',va='center',fontsize=5)
    ann=fig.add_subplot(g[1,1]);ann.imshow(group[ci][None,:],aspect='auto',cmap=ListedColormap(cols),vmin=0,vmax=2);ann.axis('off')
    ax=fig.add_subplot(g[2,1]);im=ax.imshow(z[np.ix_(ri,ci)],aspect='auto',cmap=c.cmap('diverging'),vmin=-3,vmax=3,interpolation='nearest');ax.set(xticks=[],yticks=[],xlabel='');ax.tick_params(length=0,labelsize=5)
    cb=fig.colorbar(im,cax=fig.add_subplot(g[2,2]));cb.set_label('Row z-score');cb.set_ticks([-3,0,3])
    profiles=fig.add_subplot(g[2,3]);means=np.column_stack([z[:,group==k].mean(axis=1) for k in range(3)])
    for k in range(3):profiles.plot(means[ri,k],np.arange(24),color=cols[k],lw=.9,label=f'Cohort {k+1}')
    profiles.axvline(0,c='#AAAAAA',lw=.5);profiles.set(ylim=(23.5,-.5),yticks=[],xlabel='Cohort mean z');profiles.spines[['top','right','left']].set_visible(False);profiles.legend(loc='upper center',bbox_to_anchor=(.5,-.2),fontsize=5)
    bar=fig.add_subplot(g[3,1]);bar.bar(np.arange(36),x[:,ci].mean(axis=0),width=.85,color=[cols[k] for k in group[ci]]);bar.axhline(0,c='#777777',lw=.5);bar.set(xticks=[],ylabel='Raw mean (a.u.)',xlabel='Cases · clustered order');bar.tick_params(labelsize=5)
    finish(fig,out,'clustered-atlas');return dict(row_order=ri.tolist(),column_order=ci.tolist(),z_scores=z.tolist())


def correlation(out,d,c):
    x=np.array(d['features']);r,t=correlation_order(x);order=leaves_list(t);r=r[np.ix_(order,order)];labels=[f'V{i+1:02}' for i in order]
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=125));heading(fig,'b','Correlation architecture','160 matched cases · Pearson r · average linkage on distance 1 − r')
    g=fig.add_gridspec(2,3,left=.11,right=.94,bottom=.18,top=.85,width_ratios=[1,.04,.65],height_ratios=[.18,1],wspace=.5,hspace=.04)
    tree=fig.add_subplot(g[0,0]);dendrogram(t,ax=tree,no_labels=True,color_threshold=0,above_threshold_color='#555555');tree.axis('off')
    ax=fig.add_subplot(g[1,0]);im=ax.imshow(np.ma.masked_where(np.triu(np.ones((12,12)),1).astype(bool),r),cmap=c.cmap('diverging'),vmin=-1,vmax=1)
    ax.set(xticks=range(12),yticks=range(12),xticklabels=labels,yticklabels=labels);ax.tick_params(length=0,labelsize=5);plt.setp(ax.get_xticklabels(),rotation=90)
    for i in range(12):
        for j in range(i):
            if abs(r[i,j])>=.6:ax.text(j,i,f'{r[i,j]:.1f}',ha='center',va='center',fontsize=5,color='white' if abs(r[i,j])>.65 else 'black')
    for sp in ax.spines.values():sp.set_visible(False)
    cb=fig.colorbar(im,cax=fig.add_subplot(g[1,1]));cb.set_label('Pearson r');cb.set_ticks([-1,0,1])
    sub=g[:,2].subgridspec(2,1,hspace=.55)
    raw=fig.add_subplot(sub[0]);i,j=0,1;raw.scatter(x[:,i],x[:,j],s=6,c=c.style(0)['color'],alpha=.3,lw=0);raw.set(xlabel='V01 (a.u.)',ylabel='V02 (a.u.)');raw.set_title('A pair in the original units',loc='left',fontsize=6)
    hist=fig.add_subplot(sub[1]);v=r[np.tril_indices(12,-1)];hist.hist(v,bins=np.linspace(-1,1,15),color=c.style(1)['color'],edgecolor='white',lw=.4);hist.axvline(0,c='#888888',ls=':',lw=.6);hist.set(xlabel='Pairwise Pearson r',ylabel='Variable pairs',xlim=(-1,1));hist.set_title('All 66 unique pairs',loc='left',fontsize=6)
    finish(fig,out,'correlation-architecture');return dict(order=order.tolist(),pearson=r.tolist())


def sankey(out,d,c):
    records=np.array(d['records']);tables=flow_tables(records,[3,3,3]);N=len(records);colors=[c.style(i)['color'] for i in range(3)]
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=125));heading(fig,'c','Cohort transitions and outcomes','240 persistent case identities · ribbon width encodes count · conservation at every stage')
    g=fig.add_gridspec(2,3,left=.09,right=.94,bottom=.17,top=.81,width_ratios=[1,1,.85],height_ratios=[1,.32],wspace=.55,hspace=.4)
    ax=fig.add_subplot(g[0,:2]);ax.set(xlim=(-.15,2.15),ylim=(0,1.05));ax.axis('off');gap=.055;scale=(1-2*gap)/N
    counts=[np.bincount(records[:,s],minlength=3) for s in range(3)];starts=[]
    for s in range(3):
        y=0;pos=[]
        for k,n in enumerate(counts[s]):
            pos.append(y);ax.add_patch(Rectangle((s-.025,y),.05,n*scale,color=colors[k],lw=0,zorder=5));ax.text(s-.04,y+n*scale/2,str(n),ha='right',va='center',fontsize=5,color='black',zorder=6);y+=n*scale+gap
        starts.append(np.array(pos));ax.text(s,1.05,['Input cohorts','Intermediate states','Final outcomes'][s],ha='center',va='bottom',weight='bold',fontsize=6)
    for stage,table in enumerate(tables):
        lo=starts[stage].copy();hi=starts[stage+1].copy()
        for i in range(3):
            for j in range(3):
                h=table[i,j]*scale
                if not h:continue
                a,b=lo[i],hi[j];x0,x1=stage+.025,stage+1-.025
                verts=[(x0,a),(x0+.4,a),(x1-.4,b),(x1,b),(x1,b+h),(x1-.4,b+h),(x0+.4,a+h),(x0,a+h),(x0,a)]
                codes=[MPath.MOVETO,*([MPath.CURVE4]*3),MPath.LINETO,*([MPath.CURVE4]*3),MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts,codes),facecolor=colors[i],alpha=.28,edgecolor='none'));lo[i]+=h;hi[j]+=h
    for k,col in enumerate(colors):ax.text(.0,-.10-k*.06,f'Category {k+1}',color=col,fontsize=6,transform=ax.transAxes)
    q=fig.add_subplot(g[0,2]);quality=np.array(d['quality']);rng=np.random.default_rng(3)
    vals=[quality[records[:,-1]==k] for k in range(3)];parts=q.violinplot(vals,positions=range(3),showextrema=False,widths=.8)
    for k,(body,v) in enumerate(zip(parts['bodies'],vals)):
        body.set_facecolor(colors[k]);body.set_alpha(.2);body.set_edgecolor(colors[k]);q.scatter(k+rng.uniform(-.18,.18,len(v)),v,s=3,c=colors[k],alpha=.35,lw=0);q.scatter(k,np.median(v),s=14,c='white',edgecolors='black',lw=.6,zorder=4)
    q.set(xticks=range(3),xticklabels=['1','2','3'],xlabel='Final category',ylabel='Outcome score (%)',ylim=(40,103));q.set_title('Case-level outcomes',loc='left',fontsize=6)
    for s in range(3):
        mini=fig.add_subplot(g[1,s]);bottom=0
        for k,n in enumerate(counts[s]):mini.barh(0,n/N*100,left=bottom,color=colors[k],height=.14);bottom+=n/N*100
        mini.set(xlim=(0,100),ylim=(-.3,.3),yticks=[],xticks=[0,50,100],xlabel=['Input (%)','Intermediate (%)','Final (%)'][s]);mini.spines[['left','top','right']].set_visible(False);mini.tick_params(labelsize=5,length=2)
    finish(fig,out,'transition-observatory');return dict(tables=[v.tolist() for v in tables],stage_counts=[v.tolist() for v in counts])


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    nature.apply(font_size=6);c=load_colors(a.out,a.colors);d=demo();summaries={}
    for name,draw in [('cluster',heatmap),('correlation',correlation),('flow',sankey)]:summaries[name]=draw(a.out,d,c)
    (a.out/'input-data.json').write_text(json.dumps({'kind':'SYNTHETIC DEMONSTRATION','seed':91,'data':d},indent=2));(a.out/'computed-summaries.json').write_text(json.dumps(summaries,indent=2));(a.out/'captions.txt').write_text((Path(__file__).resolve().parents[1]/'references'/'complex-data.md').read_text());print(a.out)
if __name__=='__main__':main()
