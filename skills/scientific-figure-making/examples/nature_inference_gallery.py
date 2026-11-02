"""Volcano, enrichment and forest composites from explicit synthetic observations."""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from scipy.stats import ttest_ind
from nature_data_gallery import load_colors
from nature_complex_gallery import heading,finish
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature
from inference_stats import bh,ora,meta


def observations():
    rng=np.random.default_rng(721);mu=rng.normal(6,1.2,600);delta=np.zeros(600);delta[:65]=rng.uniform(1.1,2.2,65);delta[65:110]=-rng.uniform(1.1,2.2,45)
    a=mu[:,None]+rng.normal(0,.55,(600,8));b=mu[:,None]+delta[:,None]+rng.normal(0,.55,(600,8));p=ttest_ind(b,a,axis=1,equal_var=False).pvalue;q=bh(p);effect=b.mean(axis=1)-a.mean(axis=1)
    return a,b,effect,p,q


def volcano(out,c,data):
    a,b,e,p,q=data;sel=(q<.05)&(abs(e)>=1);colors=np.where(sel,np.where(e>0,c.style(0)['color'],c.style(1)['color']),'#BFC2CA');ids=np.argsort(q)[:3]
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'l','Differential signals from overview to observations','600 synthetic features · 8 independent observations per group · Welch tests + BH across all 600')
    g=fig.add_gridspec(3,3,left=.10,right=.94,bottom=.17,top=.83,width_ratios=[1,1,.9],height_ratios=[1,1,.7],wspace=.65,hspace=.75);ax=fig.add_subplot(g[:2,:2]);ax.scatter(e,-np.log10(q),s=7,c=colors,alpha=.65,lw=0);ax.axhline(-np.log10(.05),c='#888888',ls=':',lw=.6)
    for x in [-1,1]:ax.axvline(x,c='#888888',ls=':',lw=.6)
    ax.set(xlabel='Mean difference on log2 scale',ylabel='−log10(BH-adjusted P)');ax.set_title('Volcano · all tested features',loc='left',fontsize=7,fontweight='bold')
    ax.text(.03,.97,f'{sum(sel&(e<0))} lower',transform=ax.transAxes,va='top',fontsize=6,color=c.style(1)['color']);ax.text(.97,.97,f'{sum(sel&(e>0))} higher',transform=ax.transAxes,ha='right',va='top',fontsize=6,color=c.style(0)['color'])
    for n,i in enumerate(ids):ax.annotate(f'F{i+1:03}',(e[i],-np.log10(q[i])),xytext=(.63,.88-n*.075),textcoords='axes fraction',fontsize=5,arrowprops=dict(arrowstyle='-',lw=.4,color='#777777'))
    rng=np.random.default_rng(9)
    for k,i in enumerate(ids):
        sub=fig.add_subplot(g[k,2])
        for j,v in enumerate([a[i],b[i]]):
            col=c.style([1,0][j])['color'];sub.scatter(j+rng.uniform(-.09,.09,len(v)),v,s=9,c=col,lw=0);sub.plot([j-.14,j+.14],[v.mean(),v.mean()],c='black',lw=.8)
        sub.set(xticks=[0,1],xticklabels=['A','B'],ylabel='Log2 signal (a.u.)',xlim=(-.4,1.4));sub.set_title(f'F{i+1:03} · q = {q[i]:.1e}',loc='left',fontsize=6)
    ma=fig.add_subplot(g[2,:2]);ma.scatter((a.mean(axis=1)+b.mean(axis=1))/2,e,c=colors,s=5,alpha=.5,lw=0);ma.axhline(0,c='#888888',lw=.6);ma.set(xlabel='Mean log2 signal across groups',ylabel='Difference (log2)');ma.set_title('MA view · same features and selection',loc='left',fontsize=6)
    fig.text(.10,.075,'Selection: BH-adjusted P < 0.05 and |difference| ≥ 1 · three smallest-q features shown at right',fontsize=5.5)
    finish(fig,out,'volcano-evidence');return dict(selected=sel.tolist(),displayed_features=ids.tolist())


def enrichment(out,c,data):
    a,b,e,p,q=data;rng=np.random.default_rng(722);query=set(np.where((q<.05)&(e>=1))[0].tolist());sets={}
    for k in range(12):
        size=int(rng.integers(35,100));items=set(rng.choice(600,size,replace=False).tolist())
        if k<4:items.update(rng.choice(np.arange(65),18-k*3,replace=False).tolist())
        sets[f'Set {k+1:02}']=items
    vals=sorted(ora(range(600),query,sets),key=lambda v:v['q']);fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'m','Enrichment from tested universe to set structure',f'{len(query)} synthetic selected features · 600 tested background features · 12 predefined synthetic sets')
    g=fig.add_gridspec(2,3,left=.12,right=.91,bottom=.18,top=.82,width_ratios=[1.15,1,1],height_ratios=[1,1],wspace=.8,hspace=.65);dot=fig.add_subplot(g[:,0]);frac=np.array([v['hits']/v['size'] for v in vals]);score=-np.log10(np.maximum([v['q'] for v in vals],1e-300));sc=dot.scatter(frac,range(12),s=np.array([v['hits'] for v in vals])*5,c=score,cmap=c.cmap('sequential'),vmin=0,vmax=max(3,score.max()),edgecolors='white',lw=.4);dot.set(yticks=range(12),yticklabels=[v['name'] for v in vals],xlabel='Query hits / set size');dot.invert_yaxis();dot.set_title('Overrepresentation · 12 sets',loc='left',fontweight='bold',fontsize=6)
    cb=fig.colorbar(sc,ax=dot,orientation='horizontal',fraction=.04,pad=.16);cb.set_label('−log10(BH-adjusted P)',fontsize=5);cb.ax.tick_params(labelsize=5,length=2)
    handles=[dot.scatter([],[],s=n*5,c='#888888',lw=0) for n in [5,20]];dot.legend(handles,['5','20'],title='Hit count · area',loc='upper center',bbox_to_anchor=(.5,-.32),fontsize=5,title_fontsize=5,ncol=2)
    order=np.argsort(-e);selected=sets[vals[0]['name']];hits=np.isin(order,list(selected));weight=np.abs(e[order]);inc=np.where(hits,weight/max(weight[hits].sum(),1e-15),-1/(600-hits.sum()));running=np.cumsum(inc)
    run=fig.add_subplot(g[0,1:]);run.plot(range(1,601),running,c=c.style(0)['color'],lw=1);run.axhline(0,c='#999999',lw=.6);run.set(xlim=(1,600),xlabel='Feature rank by decreasing difference',ylabel='Weighted running score');run.set_title(f'{vals[0]["name"]} · weighted rank profile',loc='left',fontsize=6)
    for pos in np.where(hits)[0]+1:run.axvline(pos,ymin=0,ymax=.04,color=c.style(0)['color'],lw=.4)
    net=fig.add_subplot(g[1,1:]);chosen=[v['name'] for v in vals[:4]];genes=sorted(set.union(*(sets[n]&query for n in chosen)))[:14]
    for k,n in enumerate(chosen):
        net.scatter(0,k,s=45,c=c.style(k)['color'],marker='s',zorder=3);net.text(-.05,k,n,ha='right',va='center',fontsize=5)
    for j,i in enumerate(genes):
        y=j*3/max(1,len(genes)-1);net.scatter(1,y,s=12,c='#666666',zorder=3);net.text(1.04,y,f'F{i+1:03}',va='center',fontsize=5)
        for k,n in enumerate(chosen):
            if i in sets[n]:net.plot([0,1],[k,y],c=c.style(k)['color'],alpha=.3,lw=.5)
    net.set(xlim=(-.3,1.3),ylim=(-.4,3.4));net.axis('off');net.set_title('Membership detail · top 4 sets, first 14 query IDs',loc='left',fontsize=6)
    fig.text(.12,.075,'ORA: upper-tail hypergeometric test, BH over 12 sets · sets overlap · rank profile has no permutation P or NES',fontsize=5)
    finish(fig,out,'enrichment-structure');return dict(query=sorted(query),sets={k:sorted(v) for k,v in sets.items()},ora=vals,rank_order=order.tolist(),running_score=running.tolist(),displayed_membership_features=genes)


def forest(out,c):
    rng=np.random.default_rng(723);se=rng.uniform(.12,.35,12);y=rng.normal(.25,.22,12)+rng.normal(0,se);r=meta(y,se);loo=[meta(np.delete(y,i),np.delete(se,i)) for i in range(12)];weights=np.array(r['weights']);fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'n','Independent study effects and model sensitivity','12 synthetic studies · log odds ratios with supplied standard errors · REML random-effects synthesis')
    g=fig.add_gridspec(2,3,left=.13,right=.94,bottom=.17,top=.82,width_ratios=[1.15,1,.95],height_ratios=[1,1],wspace=.9,hspace=.7);ax=fig.add_subplot(g[:,:2]);ax.axvline(1,c='#999999',lw=.7,ls=':')
    for i,(v,s,w) in enumerate(zip(y,se,weights)):
        ci=np.exp([v-1.95996398454*s,v+1.95996398454*s]);ax.plot(ci,[i,i],c='#656A74',lw=.8);ax.scatter(np.exp(v),i,s=w*650,c=c.style(0)['color'],marker='s',zorder=3)
        ax.text(1.03,i,f'{np.exp(v):.2f} [{ci[0]:.2f}, {ci[1]:.2f}]   {w:.1%}',transform=ax.get_yaxis_transform(),va='center',fontsize=5,clip_on=False)
    for j,(mu,err,name,col) in enumerate([(r['common'],r['common_se'],'Common effect',c.style(1)['color']),(r['mean'],r['se'],'REML pooled',c.style(0)['color'])]):
        row=13+j;ci=np.exp([mu-1.95996398454*err,mu+1.95996398454*err]);ax.add_patch(Polygon([[ci[0],row],[np.exp(mu),row-.22],[ci[1],row],[np.exp(mu),row+.22]],color=col,lw=0));ax.text(1.03,row,f'{np.exp(mu):.2f} [{ci[0]:.2f}, {ci[1]:.2f}]',transform=ax.get_yaxis_transform(),va='center',fontsize=5)
    ax.set(xscale='log',xlim=(.25,5),ylim=(15,-1),yticks=list(range(12))+[13,14],yticklabels=[f'Study {i+1:02}' for i in range(12)]+['Common effect','REML pooled'],xticks=[.25,.5,1,2,4],xlabel='Odds ratio · null = 1');ax.set_xticklabels(['0.25','0.5','1','2','4']);ax.xaxis.set_minor_formatter(plt.NullFormatter());ax.tick_params(axis='y',length=0);ax.set_title('Study estimates · square area encodes REML weight',loc='left',fontsize=6.5,fontweight='bold');ax.text(1.03,-1,'OR [95% CI]     Weight',transform=ax.get_yaxis_transform(),fontsize=5,va='bottom')
    # Reserve the numeric text column before the right diagnostic panels.
    pos=ax.get_position();ax.set_position([pos.x0,pos.y0,pos.width*.68,pos.height])
    funnel=fig.add_subplot(g[0,2]);funnel.scatter(y,se,s=14,c=c.style(1)['color'],alpha=.7,lw=0);funnel.axvline(r['mean'],c='#999999',ls=':',lw=.6);funnel.set(xlabel='Study log odds ratio',ylabel='Standard error');funnel.invert_yaxis();funnel.set_title('Precision view · no bias test',loc='left',fontsize=6)
    sens=fig.add_subplot(g[1,2]);sens.axvline(np.exp(r['mean']),c='#999999',lw=.6,ls=':')
    for i,v in enumerate(loo):sens.plot(np.exp(v['ci']),[i,i],c='#BBBEC6',lw=.6);sens.scatter(np.exp(v['mean']),i,s=8,c=c.style(0)['color'])
    sens.set(yticks=[0,5,11],yticklabels=['Omit 01','Omit 06','Omit 12'],xlabel='Pooled odds ratio',ylim=(11.7,-.7));sens.set_title('Leave-one-study-out · refit REML',loc='left',fontsize=6)
    fig.text(.13,.08,f'REML τ² = {r["tau2"]:.3f} (log-OR units squared) · pooled intervals use normal/Wald approximation',fontsize=5.5)
    finish(fig,out,'forest-sensitivity');return dict(log_or=y.tolist(),standard_errors=se.tolist(),pooled=r,leave_one_out=loo)


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors);d=observations();result=dict(kind='SYNTHETIC DEMONSTRATION',seed=[721,722,723],group_a=d[0].tolist(),group_b=d[1].tolist(),mean_difference=d[2].tolist(),p=d[3].tolist(),q=d[4].tolist(),volcano=volcano(a.out,c,d),enrichment=enrichment(a.out,c,d),forest=forest(a.out,c));(a.out/'data-and-summaries.json').write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
