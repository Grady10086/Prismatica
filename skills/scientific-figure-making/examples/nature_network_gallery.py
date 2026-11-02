"""Two additional composite layout studies. Explicit deterministic synthetic data."""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch,Rectangle
from matplotlib.path import Path as MP
import numpy as np
from nature_data_gallery import load_colors
from nature_complex_gallery import demo,correlation_order,flow_tables,heading,finish
from scipy.cluster.hierarchy import leaves_list
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature


def edges(r,threshold=.6):
    r=np.asarray(r,float)
    if r.ndim!=2 or r.shape[0]!=r.shape[1] or not np.isfinite(r).all() or not np.allclose(r,r.T):raise ValueError('Finite symmetric correlation matrix required')
    if not 0<=threshold<=1:raise ValueError('Threshold must be within 0–1')
    return [(i,j,float(r[i,j])) for i in range(len(r)) for j in range(i) if abs(r[i,j])>=threshold]


def network(out,d,c):
    r,t=correlation_order(d['features']);order=leaves_list(t);es=edges(r,.75);cols=[c.style(k)['color'] for k in range(3)];module=np.repeat(np.arange(3),4)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=135));heading(fig,'d','Association modules at three scales','160 matched cases · descriptive correlations · edges shown at |r| ≥ 0.75')
    g=fig.add_gridspec(2,2,left=.10,right=.94,bottom=.15,top=.83,width_ratios=[1,1],height_ratios=[1,.55],wspace=.5,hspace=.6)
    ax=fig.add_subplot(g[0,0]);ax.set_aspect('equal');theta=np.linspace(0,2*np.pi,12,endpoint=False)+np.pi/2;xy=np.c_[np.cos(theta),np.sin(theta)]
    for i,j,v in es:
        ax.plot(xy[[i,j],0],xy[[i,j],1],color='#555555' if v>0 else '#A05C70',alpha=.2+.4*abs(v),lw=.3+abs(v),ls='-' if v>0 else '--',zorder=1)
    for k,(x,y) in enumerate(xy):
        ax.scatter(x,y,s=60,c=cols[module[k]],edgecolors='white',lw=.8,zorder=3);ax.text(x*1.2,y*1.2,f'V{k+1:02}',ha='center',va='center',fontsize=5.5)
    ax.set(xlim=(-1.45,1.45),ylim=(-1.45,1.45));ax.axis('off');ax.set_title('Association network',loc='left',fontsize=7,fontweight='bold',pad=15)
    ax.text(.5,-.08,'Fixed circular positions · undirected associations',transform=ax.transAxes,ha='center',fontsize=5)
    heat=fig.add_subplot(g[0,1]);im=heat.imshow(r[np.ix_(order,order)],vmin=-1,vmax=1,cmap=c.cmap('diverging'));heat.set(xticks=range(12),yticks=range(12),xticklabels=[f'{k+1:02}' for k in order],yticklabels=[f'{k+1:02}' for k in order]);heat.tick_params(length=0,labelsize=5);heat.set_title('All associations · clustered order',loc='left',fontsize=7,fontweight='bold');fig.colorbar(im,ax=heat,fraction=.04,pad=.07,label='Pearson r',ticks=[-1,0,1])
    degree=np.zeros(12,int)
    for i,j,_ in es:degree[i]+=1;degree[j]+=1
    bar=fig.add_subplot(g[1,0]);idx=np.argsort(-degree,kind='stable');bar.bar(range(12),degree[idx],color=[cols[module[k]] for k in idx]);bar.set(xticks=[0,4,8,11],xticklabels=[f'V{k+1:02}' for k in idx[[0,4,8,11]]],ylabel='Displayed degree');bar.set_title('Threshold-dependent degree',loc='left',fontsize=6)
    small=fig.add_subplot(g[1,1]);means=np.empty((3,3))
    for a in range(3):
        for b in range(3):
            v=[r[i,j] for i in range(12) for j in range(i) if (module[i]==a and module[j]==b) or (module[i]==b and module[j]==a)]
            means[a,b]=np.mean(v)
    small.imshow(means,vmin=-1,vmax=1,cmap=c.cmap('diverging'))
    for i in range(3):
        for j in range(3):small.text(j,i,f'{means[i,j]:.2f}',ha='center',va='center',fontsize=5,color='white' if abs(means[i,j])>.65 else 'black')
    small.set(xticks=range(3),yticks=range(3),xticklabels=['M1','M2','M3'],yticklabels=['M1','M2','M3']);small.tick_params(length=0);small.set_title('Mean r by predefined module',loc='left',fontsize=6)
    finish(fig,out,'association-modules');return dict(edges=es,degree=degree.tolist(),module_mean_r=means.tolist(),module=module.tolist())


def ribbon(ax,table,colors):
    table=np.asarray(table);n=table.sum();scale=.86/n;starts=[];counts=[table.sum(axis=1),table.sum(axis=0)]
    for stage in range(2):
        pos=[];y=0
        for k,v in enumerate(counts[stage]):
            pos.append(y);ax.add_patch(Rectangle((stage-.02,y),.04,v*scale,color=colors[k],lw=0));y+=v*scale+.07
        starts.append(np.array(pos))
    lo,hi=starts
    for i in range(3):
        for j in range(3):
            h=table[i,j]*scale
            if h==0:continue
            a,b=lo[i],hi[j];verts=[(.02,a),(.4,a),(.6,b),(.98,b),(.98,b+h),(.6,b+h),(.4,a+h),(.02,a+h),(.02,a)]
            ax.add_patch(PathPatch(MP(verts,[MP.MOVETO,*[MP.CURVE4]*3,MP.LINETO,*[MP.CURVE4]*3,MP.CLOSEPOLY]),facecolor=colors[i],alpha=.3,lw=0));lo[i]+=h;hi[j]+=h
    ax.set(xlim=(-.08,1.08),ylim=(-.1,1.05));ax.axis('off');ax.text(0,-.08,'Input',ha='center',fontsize=5);ax.text(1,-.08,'Final',ha='center',fontsize=5)


def transitions(out,d,c):
    rng=np.random.default_rng(819);colors=[c.style(k)['color'] for k in range(3)];matrices=[];records=[]
    probabilities=[[[.85,.10,.05],[.10,.75,.15],[.05,.15,.80]],[[.60,.25,.15],[.25,.50,.25],[.15,.25,.60]],[[.40,.35,.25],[.35,.40,.25],[.30,.30,.40]],[[.75,.20,.05],[.50,.40,.10],[.35,.40,.25]]]
    for p in probabilities:
        first=np.repeat(np.arange(3),60);last=np.array([rng.choice(3,p=p[i]) for i in first]);a=np.c_[first,last];records.append(a.tolist());matrices.append(flow_tables(a,[3,3])[0])
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=145));heading(fig,'e','Transition fingerprints across cohorts','Four synthetic cohorts · n = 180 each · identical count-to-width scale across all flows')
    g=fig.add_gridspec(3,4,left=.09,right=.95,bottom=.17,top=.82,height_ratios=[1,.65,.55],hspace=.7,wspace=.55)
    for k,table in enumerate(matrices):
        ax=fig.add_subplot(g[0,k]);ribbon(ax,table,colors);ax.set_title(f'Cohort {k+1}',loc='left',fontsize=7,fontweight='bold',pad=13)
        heat=fig.add_subplot(g[1,k]);rate=table/table.sum(axis=1,keepdims=True);im=heat.imshow(rate,vmin=0,vmax=1,cmap=c.cmap('sequential'))
        for i in range(3):
            for j in range(3):heat.text(j,i,f'{rate[i,j]:.0%}',ha='center',va='center',fontsize=5,color='white' if rate[i,j]>.65 else 'black')
        heat.set(xticks=range(3),yticks=range(3),xticklabels=['1','2','3'],yticklabels=['1','2','3'],xlabel='Final category');heat.tick_params(length=0,labelsize=5)
        if k==0:heat.set_ylabel('Input category')
    bar=fig.add_subplot(g[2,:2]);stay=np.array([np.trace(t)/t.sum() for t in matrices]);bar.barh(range(4),stay*100,color=c.style(0)['color'],height=.55);bar.set(yticks=range(4),yticklabels=[f'Cohort {k+1}' for k in range(4)],xlim=(0,100),xlabel='Unchanged category (%)');bar.invert_yaxis();bar.tick_params(labelsize=5)
    comp=fig.add_subplot(g[2,2:]);bottom=np.zeros(4)
    for k,col in enumerate(colors):
        values=np.array([m[:,k].sum()/m.sum()*100 for m in matrices]);comp.barh(range(4),values,left=bottom,color=col,height=.55,label=f'Category {k+1}');bottom+=values
    comp.set(yticks=range(4),yticklabels=[f'Cohort {k+1}' for k in range(4)],xlim=(0,100),xlabel='Final composition (%)');comp.invert_yaxis();comp.tick_params(labelsize=5);comp.legend(loc='upper center',bbox_to_anchor=(.5,1.35),ncol=3,fontsize=5)
    cb=fig.add_axes([.35,.105,.3,.012]);fig.colorbar(im,cax=cb,orientation='horizontal',ticks=[0,.5,1],label='Conditional transition probability · each row sums to 1');cb.tick_params(labelsize=5,length=2)
    finish(fig,out,'transition-fingerprints');return dict(case_records=records,tables=[m.tolist() for m in matrices],unchanged_fraction=stay.tolist())


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors);d=demo()
    result=dict(kind='SYNTHETIC DEMONSTRATION',features=d['features'],network=network(a.out,d,c),transitions=transitions(a.out,d,c));(a.out/'data-and-summaries.json').write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
