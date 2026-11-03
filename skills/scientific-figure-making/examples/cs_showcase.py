"""CS experiment compositions. All arrays are synthetic; no benchmark claims."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from showcase_gallery import theme,clean,panel,footer,save,ci,BLUE,ROSE,PEACH,INK,GRAY,LIGHT
RAW={}
def panel(a,letter,title):
 a.set_title(title,loc='left',pad=13)
 a.text(-min(.12,.035/a.get_position().width),1.065,letter,transform=a.transAxes,fontweight='bold',fontsize=10)

COL=[BLUE,ROSE,PEACH,'#758E8B'];MARK=['o','s','^','D']
def analysis(out,rng):
 n=240;difficulty=rng.uniform(0,1,n);base=np.clip(.90-.48*difficulty+rng.normal(0,.11,n),0,1);updated=np.clip(base+.13-.21*difficulty+rng.normal(0,.07,n),0,1);delta=updated-base
 # One actual run-level fixture, not separately fabricated summaries.
 layers=np.arange(1,13);probe=np.clip(48+23*(1-np.exp(-layers/3))[:,None]+rng.normal(0,1.5,(12,10)),0,100)
 f=plt.figure(figsize=(11,6.4));a=f.add_axes([.075,.25,.36,.61875]);f.text(.075,.97,'a  Where does the model improve?',fontsize=10,fontweight='bold')
 a.plot([0,1],[0,1],c=GRAY,ls='--',lw=.8);sc=a.scatter(base,updated,c=delta,cmap=LinearSegmentedColormap.from_list('gain',[ROSE,'#F3F1EE',BLUE]),vmin=-.25,vmax=.25,s=19,alpha=.75,lw=.25,edgecolor='white');a.set(xlabel='Baseline correctness probability',ylabel='Updated correctness probability',xlim=(0,1),ylim=(0,1),aspect='equal');clean(a)
 # Marginal distributions align to the main axes.
 top=f.add_axes([.075,.89,.36,.045]);edges=np.linspace(0,1,22);top.hist(base,bins=edges,color=GRAY,alpha=.75);top.set(xlim=(0,1));top.axis('off')
 right=f.add_axes([.445,.25,.025,.61875]);right.hist(updated,bins=edges,orientation='horizontal',color=BLUE,alpha=.5);right.set(ylim=(0,1));right.axis('off')
 cb=f.colorbar(sc,cax=f.add_axes([.14,.12,.23,.014]),orientation='horizontal',extend='both');cb.set_label('Paired probability change',fontsize=7);cb.set_ticks([-.25,0,.25])
 a.text(.04,.91,'Above diagonal: improved',transform=a.transAxes,fontsize=7,color=BLUE)
 b=f.add_axes([.65,.59,.29,.27]);panel(b,'b','Layer-wise linear probes');m=probe.mean(1);se=probe.std(1,ddof=1)/np.sqrt(10);b.fill_between(layers,m-2.262*se,m+2.262*se,color=BLUE,alpha=.17);b.plot(layers,m,c=BLUE,marker='o',ms=3,lw=1.3);b.set(xlabel='Frozen backbone layer',ylabel='Probe accuracy (%)',xticks=[1,4,8,12]);clean(b)
 c=f.add_axes([.65,.23,.29,.22]);panel(c,'c','Difficulty-conditioned change');bins=np.linspace(0,1,5)
 for k in range(4):
  v=delta[(difficulty>=bins[k])&(difficulty<bins[k+1])];lo,hi=ci(v,rng);c.plot([lo,hi],[k,k],c=COL[k],lw=2);c.scatter(v.mean(),k,c=COL[k],s=23,zorder=3)
 c.axvline(0,c=GRAY,lw=.8);c.set(yticks=range(4),yticklabels=['0–.25','.25–.50','.50–.75','.75–1'],xlabel='Mean paired Δ · 95% bootstrap CI',ylabel='Input difficulty',ylim=(3.6,-.6));clean(c);footer(f,'240 paired synthetic cases; difficulty fixed independently; probes: 10 seeds, pointwise t intervals (df=9).')
 RAW.update(analysis_difficulty=difficulty,analysis_base=base,analysis_updated=updated,analysis_probe=probe);save(f,out,'cs-model-analysis')
def ablation(out,rng):
 # Full 2^3 factorial; common seed offsets preserve paired contrasts.
 config=np.array([[a,b,c] for a in [0,1] for b in [0,1] for c in [0,1]]);shared=rng.normal(0,1.8,16);y=np.array([65+4*a+2*b-1*c+3*a*b-2*b*c+shared+rng.normal(0,.65,16) for a,b,c in config]);means=y.mean(1)
 f=plt.figure(figsize=(11,6.4));a=f.add_axes([.075,.27,.43,.58]);panel(a,'a','Every configuration, every seed')
 for j in range(8):
  lo,hi=ci(y[j],rng);a.scatter(y[j],np.full(16,j)+np.linspace(-.13,.13,16),c=COL[0] if j==7 else GRAY,s=10,alpha=.65);a.plot([lo,hi],[j,j],c=BLUE,lw=2);a.scatter(means[j],j,c=BLUE,s=23,zorder=4)
 a.set(yticks=range(8),yticklabels=['None','C','B','B+C','A','A+C','A+B','A+B+C'],xlabel='Task score · mean and 95% seed-bootstrap CI',ylim=(7.7,-.7));a.xaxis.grid(color=LIGHT,lw=.6);clean(a)
 mat=f.add_axes([.075,.12,.43,.065]);mat.imshow(config.T,aspect='auto',cmap=LinearSegmentedColormap.from_list('binary',['#F1F2F4',BLUE]),vmin=0,vmax=1);mat.set(yticks=[0,1,2],yticklabels=['A','B','C'],xticks=range(8),xticklabels=['∅','C','B','BC','A','AC','AB','ABC']);mat.tick_params(length=0,labelsize=6);mat.spines[:].set_visible(False)
 b=f.add_axes([.65,.57,.29,.28]);panel(b,'b','Marginal component effects')
 for j in range(3):
  v=y[config[:,j]==1].mean(0)-y[config[:,j]==0].mean(0);lo,hi=ci(v,rng);b.plot([lo,hi],[j,j],c=COL[j],lw=2);b.scatter(v.mean(),j,c=COL[j],s=26)
 b.axvline(0,c=GRAY,lw=.8);b.set(yticks=range(3),yticklabels=['A · retrieval','B · routing','C · regularizer'],xlabel='Average on − off · 95% paired CI',ylim=(2.6,-.6));clean(b)
 c=f.add_axes([.65,.18,.29,.23]);panel(c,'c','A × B interaction, averaged over C')
 for a0 in range(2):
  vals=[y[(config[:,0]==a0)&(config[:,1]==b0)].mean(0) for b0 in range(2)];c.plot([0,1],[v.mean() for v in vals],c=COL[a0],marker=MARK[a0],lw=1.5,label=f'A {"on" if a0 else "off"}')
 c.set(xticks=[0,1],xticklabels=['B off','B on'],ylabel='Task score');c.legend(frameon=False,loc='upper left');clean(c);footer(f,'Full 2³ design; 16 shared seeds; effects average all other factors; bootstrap resamples seed IDs jointly.')
 RAW.update(ablation_config=config,ablation_score=y);save(f,out,'cs-factorial-ablation')
def performance(out,rng):
 n=20;bud=np.array([1,2,4,8]);offset=rng.normal(0,1.2,n);scores=np.array([[61+6*np.log2(b)+k*2.0-((k==3)*3*np.log2(b))+offset+rng.normal(0,.7,n) for b in bud] for k in range(4)]);lat=np.array([[b*s*rng.lognormal(0,.08,n) for b in bud] for s in [.10,.16,.25,.06]]);names=['Reference','Compact','Adaptive','Early exit'];task_offsets=rng.normal(0,4,(10,4,20));task_offsets-=task_offsets.mean(0,keepdims=True);task_runs=scores[:,2,:][None,:,:]+task_offsets;tasks=task_runs.mean(2)
 f=plt.figure(figsize=(11,6.4));a=f.add_axes([.08,.40,.47,.45]);panel(a,'a','Performance across operating budgets')
 for k in range(4):
  x=np.median(lat[k],1);m=scores[k].mean(1);a.plot(x,m,c=COL[k],marker=MARK[k],lw=1.4,ms=4,label=names[k]);a.annotate(names[k],(x[-1],m[-1]),xytext=(5,0),textcoords='offset points',fontsize=7,color=COL[k])
 a.set(xscale='log',xlabel='Simulated median latency (s) · log scale',ylabel='Task score ↑',xlim=(.045,3.4));a.yaxis.grid(color=LIGHT,lw=.6);clean(a)
 b=f.add_axes([.73,.40,.21,.45]);panel(b,'b','Paired gain at budget = 4');base=scores[0,2]
 for j,k in enumerate([1,2,3]):
  v=scores[k,2]-base;lo,hi=ci(v,rng);b.plot([lo,hi],[j,j],c=COL[k],lw=2);b.scatter(v.mean(),j,c=COL[k],marker=MARK[k],s=28)
 b.axvline(0,c=GRAY,lw=.8);b.set(yticks=range(3),yticklabels=names[1:],xlabel='Score Δ · 95% paired CI',ylim=(2.6,-.6));clean(b)
 c=f.add_axes([.08,.15,.86,.12]);panel(c,'c','Task-by-task audit at budget = 4')
 for i in range(10):
  x=i+np.array([-.24,-.08,.08,.24]);c.plot(x,tasks[i],c='#D5DAE0',lw=.8)
  for k in range(4):c.scatter(x[k],tasks[i,k],c=COL[k],marker=MARK[k],s=17)
 c.set(xticks=range(10),xticklabels=[f'T{i+1:02}' for i in range(10)],ylabel='Task score');clean(c);footer(f,'20 matched seeds; four evaluated budgets only; no interpolated optimum; task audit averages to the fixed-budget panel; latency is simulated.')
 RAW.update(performance_budgets=bud,performance_scores=scores,performance_latency=lat,performance_tasks=tasks,performance_task_runs=task_runs);save(f,out,'cs-performance-audit')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);theme();rng=np.random.default_rng(1105);analysis(a.out,rng);ablation(a.out,rng);performance(a.out,rng);np.savez_compressed(a.out/'cs-inputs.npz',**RAW);(a.out/'provenance.json').write_text(json.dumps({'kind':'All inputs synthetic; original layouts, no model performance claims','seed':1105,'bootstrap_resamples':2000,'dimensions':'11 × 6.4 inch gallery masters; adapt typography for paper width','probe_interval':'pointwise t interval, df=9; other intervals percentile bootstrap of matched seed/case differences'},indent=2));print(a.out)
if __name__=='__main__':main()
