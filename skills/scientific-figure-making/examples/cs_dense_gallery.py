"""Dense CS composites from the reproducible cs_showcase arrays; all inputs synthetic."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.colors import LinearSegmentedColormap,TwoSlopeNorm
from showcase_gallery import theme,save,ci,BLUE,ROSE,PEACH,INK,GRAY,LIGHT
COL=[BLUE,ROSE,PEACH,'#758E8B'];LABEL=['Reference','Compact','Adaptive','Early exit']
def style(a,letter,title):
 a.set_title(title,loc='left',fontsize=8,pad=7)
 a.text(-min(.13,.025/a.get_position().width),1.04,letter,transform=a.transAxes,fontweight='bold',fontsize=10)
 a.tick_params(length=2,width=.5,pad=2,labelsize=6);a.spines[['top','right']].set_visible(False)
def fig():
 f=plt.figure(figsize=(11,6.7));return f,f.add_gridspec(2,3,left=.065,right=.955,bottom=.09,top=.94,wspace=.48,hspace=.43)
def end(f,out,name):
 f.text(.065,.015,'SYNTHETIC DATA  |  Original composition · matched arrays · pointwise intervals; definitions in gallery',fontsize=5.5,color='#7D8790');save(f,out,name)
def density(a,v,y,col,width=.72):
 pad=max(np.ptp(v)*.18,.001);xx=np.linspace(v.min()-pad,v.max()+pad,180);d=gaussian_kde(v)(xx);d=d/d.max()*width
 a.fill_between(xx,y,y-d,color=col,alpha=.35,lw=0);a.plot(xx,y-d,c=col,lw=.7)
 a.scatter(v,np.full(len(v),y)+np.linspace(.035,.12,len(v)),s=5,c=col,alpha=.65,lw=0)
def ablation(z,out,rng):
 c=z['ablation_config'];y=z['ablation_score'];names=['None','C','B','BC','A','AC','AB','ABC'];f=plt.figure(figsize=(11,6.7));g=f.add_gridspec(2,3,left=.075,right=.955,bottom=.09,top=.94,wspace=.45,hspace=.40,width_ratios=[1.25,1,1]);a=f.add_subplot(g[:,0]);style(a,'a','Full-factorial response distributions')
 for i,v in enumerate(y):
  density(a,v,i,COL[0] if c[i,0] else COL[1],.62);lo,hi=ci(v,rng);a.plot([lo,hi],[i+.25,i+.25],c=INK,lw=1);a.scatter(v.mean(),i+.25,c=INK,s=9)
 a.set(yticks=range(8),yticklabels=names,xlabel='Task score',ylim=(7.7,-.9));a.xaxis.grid(color=LIGHT,lw=.4)
 effects=np.array([y[c[:,j]==1].mean(0)-y[c[:,j]==0].mean(0) for j in range(3)])
 b=f.add_subplot(g[0,1]);style(b,'b','Marginal factor effects')
 for j,v in enumerate(effects):
  density(b,v,j,COL[j],.5);lo,hi=ci(v,rng);b.plot([lo,hi],[j+.25,j+.25],c=INK,lw=1);b.scatter(v.mean(),j+.25,c=INK,s=9)
 b.axvline(0,c=GRAY,ls='--',lw=.6);b.set(yticks=range(3),yticklabels=['A','B','C'],xlabel='Paired on − off',ylim=(2.7,-.8))
 d=f.add_subplot(g[0,2]);style(d,'c','Within-seed response structure');delta=y-y[0];order=np.argsort(delta.mean(0));im=d.imshow(delta[:,order],aspect='auto',cmap=LinearSegmentedColormap.from_list('signed',[ROSE,'#FAF8F4',BLUE]),norm=TwoSlopeNorm(0,-10,10),interpolation='nearest');d.set(yticks=range(8),yticklabels=names,xticks=[0,7,15],xticklabels=['1','8','16'],xlabel='Seed · sorted by mean gain');cb=f.colorbar(im,ax=d,fraction=.045,pad=.025,extend='both');cb.set_label('Δ vs none',fontsize=6);cb.ax.tick_params(labelsize=5,length=2)
 for p,(i,j) in enumerate([(0,1),(0,2)]):
  ax=f.add_subplot(g[1,p+1]);style(ax,'de'[p],f'{"ABC"[i]} × {"ABC"[j]} interaction')
  for on in [0,1]:
   vals=[y[(c[:,i]==on)&(c[:,j]==v)].mean(0) for v in [0,1]]
   for seed in range(16):ax.plot([0,1],[v[seed] for v in vals],c=COL[on],alpha=.14,lw=.5)
   means=[v.mean() for v in vals];bounds=np.array([ci(v,rng) for v in vals]);ax.errorbar([0,1],means,yerr=[means-bounds[:,0],bounds[:,1]-means],c=COL[on],marker=['o','s'][on],ms=4,lw=1.5,capsize=2,label=f'{"ABC"[i]} {"on" if on else "off"}')
  ax.set(xticks=[0,1],xticklabels=[f'{"ABC"[j]} off',f'{"ABC"[j]} on'],ylabel='Task score',xlim=(-.12,1.12));ax.legend(frameon=False,fontsize=6,loc='upper left')
 end(f,out,'editorial-ablation')
def analysis(z,out,rng):
 x=z['analysis_base'];y=z['analysis_updated'];v=y-x;dif=z['analysis_difficulty'];p=z['analysis_probe'];f,g=fig();a=f.add_subplot(g[0,0]);style(a,'a','Paired prediction density');counts=a.hexbin(x,y,gridsize=24,mincnt=1,cmap=LinearSegmentedColormap.from_list('count',['#E7E8F0',BLUE]),linewidths=.15);a.plot([0,1],[0,1],c=GRAY,ls='--',lw=.7);a.set(xlabel='Baseline probability',ylabel='Updated probability',xlim=(0,1),ylim=(0,1))
 cb=f.colorbar(counts,cax=a.inset_axes([.08,.90,.32,.025]),orientation='horizontal');cb.set_label('Cases / hexagon',fontsize=5);cb.ax.tick_params(labelsize=5,length=1,pad=1)
 b=f.add_subplot(g[0,1]);style(b,'b','Layer-wise probe distributions')
 parts=b.violinplot(list(p),positions=np.arange(1,13),widths=.8,showextrema=False)
 for body in parts['bodies']:body.set_facecolor(BLUE);body.set_alpha(.3);body.set_edgecolor('none')
 b.plot(np.arange(1,13),p.mean(1),c=BLUE,marker='o',ms=2.5,lw=1);b.set(xlabel='Frozen backbone layer',ylabel='Accuracy (%)',xticks=[1,4,8,12])
 d=f.add_subplot(g[0,2]);style(d,'c','Difficulty-dependent residuals');d.scatter(dif,v,s=7,c=np.where(v>=0,BLUE,ROSE),alpha=.45,lw=0);d.axhline(0,c=GRAY,lw=.6,ls='--');d.set(xlabel='Input difficulty',ylabel='Paired probability change',xlim=(0,1))
 e=f.add_subplot(g[1,0]);style(e,'d','Change distributions by difficulty')
 for j in range(4):density(e,v[(dif>=j/4)&(dif<(j+1)/4)],j,COL[j],.65)
 e.axvline(0,c=GRAY,lw=.6,ls='--');e.set(yticks=range(4),yticklabels=['0–.25','.25–.50','.50–.75','.75–1'],xlabel='Paired probability change',ylim=(3.5,-.8))
 h=f.add_subplot(g[1,1]);style(h,'e','Case-wise change audit');vv=np.sort(v);h.bar(np.arange(len(vv)),vv,width=1,color=np.where(vv>=0,BLUE,ROSE),lw=0);h.axhline(0,c=GRAY,lw=.5);h.set(xlabel='Case · ordered by change',ylabel='Δ probability',xlim=(0,len(vv)))
 k=f.add_subplot(g[1,2]);style(k,'f','Effect estimates across difficulty')
 for j in range(4):
  vv=v[(dif>=j/4)&(dif<(j+1)/4)];lo,hi=ci(vv,rng);k.errorbar(j,vv.mean(),yerr=[[vv.mean()-lo],[hi-vv.mean()]],fmt='o',color=COL[j],ms=4,capsize=3,lw=1.2);k.scatter(j+np.linspace(-.15,.15,len(vv)),vv,s=3,c=COL[j],alpha=.16)
 k.axhline(0,c=GRAY,lw=.6);k.set(xticks=range(4),xticklabels=['Q1','Q2','Q3','Q4'],xlabel='Fixed difficulty bins',ylabel='Mean Δ · 95% case-bootstrap CI');end(f,out,'editorial-analysis')
def performance(z,out,rng):
 scores=z['performance_scores'];lat=z['performance_latency'];tasks=z['performance_tasks'];runs=z['performance_task_runs'];f,g=fig();a=f.add_subplot(g[0,:2]);style(a,'a','Quality–cost operating points and seed variability')
 for k in range(4):
  xx=np.median(lat[k],1);yy=scores[k].mean(1);sd=scores[k].std(1,ddof=1);a.errorbar(xx,yy,yerr=sd,c=COL[k],marker=['o','s','^','D'][k],ms=4,lw=1.4,capsize=2,label=LABEL[k]);a.scatter(lat[k].ravel(),scores[k].ravel(),c=COL[k],alpha=.13,s=5,lw=0)
 a.set(xscale='log',xlabel='Simulated latency (s)',ylabel='Task score');a.legend(frameon=False,ncol=2,fontsize=6,loc='lower right');a.yaxis.grid(color=LIGHT,lw=.4)
 b=f.add_subplot(g[0,2]);style(b,'b','Paired fixed-budget effects')
 for k in range(1,4):density(b,scores[k,2]-scores[0,2],k-1,COL[k],.65)
 b.axvline(0,c=GRAY,lw=.6,ls='--');b.set(yticks=range(3),yticklabels=LABEL[1:],xlabel='Δ score at budget 4',ylim=(2.5,-.8))
 c=f.add_subplot(g[1,0]);style(c,'c','Task-dependent method profiles')
 for k in range(4):c.plot(np.arange(10),tasks[:,k],c=COL[k],marker=['o','s','^','D'][k],ms=2.5,lw=.9,alpha=.9)
 c.set(xticks=[0,3,6,9],xticklabels=['T01','T04','T07','T10'],xlabel='Task',ylabel='Mean task score')
 d=f.add_subplot(g[1,1]);style(d,'d','Task effects relative to reference');delta=tasks[:,1:]-tasks[:,[0]];im=d.imshow(delta.T,aspect='auto',cmap=LinearSegmentedColormap.from_list('effect',[ROSE,'#FAF8F4',BLUE]),norm=TwoSlopeNorm(0,-6,6));d.set(yticks=range(3),yticklabels=LABEL[1:],xticks=[0,3,6,9],xticklabels=['T01','T04','T07','T10'],xlabel='Task');cb=f.colorbar(im,ax=d,orientation='horizontal',fraction=.06,pad=.17,extend='both');cb.set_label('Mean Δ score',fontsize=6);cb.ax.tick_params(labelsize=5,length=2)
 e=f.add_subplot(g[1,2]);style(e,'e','Seed-consistent task wins')
 for k in range(1,4):
  win=(runs[:,k,:]>runs[:,0,:]).mean(0);sv=np.sort(win);e.step(sv,np.arange(1,21)/20,c=COL[k],lw=1.3,label=LABEL[k]);e.scatter(sv,np.arange(1,21)/20,s=7,c=COL[k],lw=0)
 e.set(xlabel='Fraction of tasks beating reference / seed',ylabel='ECDF across 20 seeds',xlim=(0,1),ylim=(0,1.02));e.legend(frameon=False,fontsize=6,loc='upper left');end(f,out,'editorial-performance')
def main():
 p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);z=np.load(a.inputs);theme();plt.rcParams.update({'font.size':7,'axes.labelsize':7,'axes.linewidth':.5,'xtick.labelsize':6,'ytick.labelsize':6});rng=np.random.default_rng(1106);ablation(z,a.out,rng);analysis(z,a.out,rng);performance(z,a.out,rng);(a.out/'editorial-provenance.json').write_text(json.dumps({'kind':'Synthetic inputs; original dense layouts','input':a.inputs.name,'seed':1106,'bootstrap_resamples':2000,'density':'Gaussian KDE; descriptive, not a confidence region','intervals':'Pointwise percentile bootstrap over paired seeds/cases; performance operating point bars show seed SD'},indent=2));print(a.out)
if __name__=='__main__':main()
