"""Compact 180-mm CS experiment templates; all source data are synthetic fixtures."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
C=['#356C92','#C46B56','#3B8C7D','#9B86B1'];RAW={};SUMMARY={}
def setup():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'axes.labelsize':7,'axes.titlesize':7.5,'xtick.labelsize':6,'ytick.labelsize':6,'legend.fontsize':6,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.5,'xtick.major.width':.5,'ytick.major.width':.5,'lines.linewidth':1.2,'svg.fonttype':'none','pdf.fonttype':42})
def fig():
 f,axs=plt.subplots(2,2,figsize=(180/25.4,120/25.4));f.subplots_adjust(left=.105,right=.97,bottom=.15,top=.93,hspace=.64,wspace=.45);return f,axs.ravel()
def label(a,l,t):a.set_title(t,loc='left',pad=6);a.text(-.2,1.11,l,transform=a.transAxes,fontweight='bold',fontsize=9)
def save(f,out,name,note):
 f.text(.105,.035,'SYNTHETIC DEMO · '+note,fontsize=5.5,color='#666666')
 for ext in ['svg','pdf','png']:f.savefig(out/(name+'.'+ext),dpi=300)
 plt.close(f)
def band(a,x,v,c,label):
 med=np.median(v,axis=0);lo,hi=np.quantile(v,[.25,.75],axis=0);a.plot(x,med,c=c,label=label);a.fill_between(x,lo,hi,color=c,alpha=.16,lw=0)
def train(out,rng):
 f,aa=fig();x=np.arange(0,101);train=[];val=[];grads=[]
 for k,decay in enumerate([28,21]):
  tr=np.array([.3+1.8*np.exp(-x/(decay+rng.normal(0,1)))+rng.normal(0,.015,len(x)) for _ in range(8)]);va=tr+.06+.10*(x/100)**2+rng.normal(0,.012,tr.shape);g=np.array([.15+1.3*np.exp(-x/(14+k*2))+np.abs(rng.normal(0,.055,len(x))) for _ in range(8)]);train.append(tr);val.append(va);grads.append(g)
 label(aa[0],'a','Optimization and validation');
 for k in range(2):
  band(aa[0],x,val[k],C[k],f'Model {"AB"[k]} · val');aa[0].plot(x,np.median(train[k],axis=0),c=C[k],ls='--',alpha=.65)
 aa[0].set(xlabel='Training epoch',ylabel='Cross-entropy');aa[0].legend(frameon=False);aa[0].text(.97,.5,'Dashed: train\nBand: seed IQR',ha='right',transform=aa[0].transAxes,fontsize=6,color='#666666')
 label(aa[1],'b','Gradient magnitude across seeds')
 for k in range(2):band(aa[1],x,grads[k],C[k],f'Model {"AB"[k]}')
 aa[1].set(xlabel='Training epoch',ylabel='Gradient L2 norm');aa[1].legend(frameon=False)
 label(aa[2],'c','Validation loss at fixed checkpoints');positions=[];data=[]
 for i,e in enumerate([20,50,100]):
  for k in range(2):positions.append(i+(k-.5)*.25);data.append(val[k][:,e])
 b=aa[2].boxplot(data,positions=positions,widths=.19,patch_artist=True,showfliers=False,medianprops={'color':'#222222'},boxprops={'linewidth':.5},whiskerprops={'linewidth':.5},capprops={'linewidth':.5})
 for i,p in enumerate(b['boxes']):p.set(facecolor=C[i%2],alpha=.35)
 for j,(pos,v) in enumerate(zip(positions,data)):aa[2].scatter(pos+np.linspace(-.05,.05,8),v,s=7,c=C[j%2],zorder=3)
 aa[2].set(xticks=[0,1,2],xticklabels=['20','50','100'],xlabel='Training epoch',ylabel='Validation cross-entropy')
 label(aa[3],'d','Final loss · seed-matched comparison');v0=val[0][:,-1];v1=val[1][:,-1]
 for i in range(8):aa[3].plot([0,1],[v0[i],v1[i]],c='#C1C5C8',lw=.6,zorder=1)
 aa[3].scatter(np.zeros(8),v0,c=C[0],s=14,zorder=2);aa[3].scatter(np.ones(8),v1,c=C[1],s=14,zorder=2);aa[3].set(xticks=[0,1],xticklabels=['Model A','Model B'],xlim=(-.3,1.3),ylabel='Validation cross-entropy')
 RAW.update(train=np.array(train),validation=np.array(val),gradients=np.array(grads));save(f,out,'paper-training-dynamics','8 seeds; curves median/IQR; boxes Q1–Q3, whiskers 1.5 IQR; points retained.')
def boot(v,rng):
 return np.quantile(v[rng.integers(0,len(v),(2000,len(v)))].mean(1),[.025,.975])
def align(out,rng):
 n=120;d=64;image=rng.normal(size=(n,d));image/=np.linalg.norm(image,axis=1,keepdims=True);texta=image+.40*rng.normal(size=(n,d));textb=image+.26*rng.normal(size=(n,d));texta/=np.linalg.norm(texta,axis=1,keepdims=True);textb/=np.linalg.norm(textb,axis=1,keepdims=True);sims=np.array([image@texta.T,image@textb.T]);ranks=np.array([(s>=np.diag(s)[:,None]).sum(1) for s in sims]);f,aa=fig()
 label(aa[0],'a','Image-to-text retrieval')
 for k in range(2):aa[0].step(np.arange(1,21),[(ranks[k]<=j).mean() for j in range(1,21)],where='post',c=C[k],label=f'Encoder {"AB"[k]}')
 aa[0].set(xlabel='Retrieved rank k',ylabel='Recall@k',ylim=(0,1.02),xlim=(1,20),xticks=[1,5,10,15,20]);aa[0].legend(frameon=False)
 label(aa[1],'b','Matched versus shifted image–text pairs');vals=[]
 for k in range(2):vals.extend([np.diag(sims[k]),sims[k,np.arange(n),(np.arange(n)+1)%n]])
 v=aa[1].violinplot(vals,positions=[0,1,3,4],widths=.8,showmedians=True,showextrema=False)
 for k,b in enumerate(v['bodies']):b.set_facecolor(C[k//2]);b.set_alpha(.3)
 aa[1].axhline(0,c='#BBBBBB',lw=.5);aa[1].set(xticks=[0,1,3,4],xticklabels=['A +','A −','B +','B −'],ylabel='Cosine similarity');aa[1].text(.03,.95,'+ matched; − cyclic-shifted',transform=aa[1].transAxes,fontsize=6,va='top')
 label(aa[2],'c','Paired alignment gain by source');delta=np.diag(sims[1])-np.diag(sims[0]);order=np.argsort(delta);aa[2].vlines(np.arange(n),0,delta[order],colors=np.where(delta[order]>=0,C[2],C[1]),lw=.7);aa[2].axhline(0,c='#777777',lw=.5);aa[2].set(xlabel='Image–text pair · sorted by gain',ylabel='Cosine difference (B − A)')
 label(aa[3],'d','Aggregate gains · paired bootstrap');vv=[(ranks[1]<=k).astype(float)-(ranks[0]<=k).astype(float) for k in [1,5,10]];cis=[boot(v,rng) for v in vv];means=[v.mean() for v in vv]
 # All three rows use recall differences on the same scale.
 for i in range(3):aa[3].errorbar(means[i],i,xerr=[[means[i]-cis[i][0]],[cis[i][1]-means[i]]],fmt='o',c=C[i],capsize=3)
 aa[3].axvline(0,c='#AAAAAA',lw=.6);aa[3].set(yticks=[0,1,2],yticklabels=['Recall@1 Δ','Recall@5 Δ','Recall@10 Δ'],xlabel='Recall difference (B − A)',ylim=(-.7,3.0));aa[3].text(.03,.96,'Mean and 95% paired bootstrap CI',transform=aa[3].transAxes,va='top',fontsize=6)
 RAW.update(image_embeddings=image,text_embeddings_A=texta,text_embeddings_B=textb,retrieval_ranks=ranks);SUMMARY['alignment']={'means':means,'ci95':[v.tolist() for v in cis],'bootstrap_unit':'image-text pair','n':n};save(f,out,'paper-crossmodal-alignment','120 synthetic pairs; cyclic negatives; descriptive projection-free diagnostics.')
def diffusion(out,rng):
 budgets=np.array([4,8,16,32]);n=80;difficulty=rng.lognormal(-1,.5,n);err=np.array([[difficulty/(b**(.5+.08*k))+.012+rng.uniform(0,.015,n) for b in budgets] for k in range(2)]);f,aa=fig()
 label(aa[0],'a','Reconstruction fidelity versus compute')
 for k in range(2):
  med=np.median(err[k],axis=1);q=np.quantile(err[k],[.25,.75],axis=1);aa[0].errorbar(budgets,med,yerr=[med-q[0],q[1]-med],fmt='o-',c=C[k],label=f'Sampler {"AB"[k]}',capsize=2,ms=3)
 aa[0].set_xscale('log',base=2);aa[0].set(xticks=budgets,xticklabels=budgets,xlabel='Function evaluations (NFE)',ylabel='Reconstruction MSE ↓');aa[0].legend(frameon=False)
 label(aa[1],'b','Instance-level gain at matched NFE');delta=err[0,-1]-err[1,-1];aa[1].hist(delta,bins=14,color=C[2],edgecolor='white',lw=.5);aa[1].axvline(0,c='#777777',ls='--',lw=.7);aa[1].set(xlabel='MSE reduction (A − B) at NFE = 32',ylabel='Number of instances')
 label(aa[2],'c','Distribution tails, not only the median')
 for k in range(2):
  v=np.sort(err[k,-1]);aa[2].step(v,np.arange(1,n+1)/n,where='post',c=C[k],label=f'Sampler {"AB"[k]}')
 aa[2].set(xlabel='MSE at NFE = 32',ylabel='Empirical cumulative probability',ylim=(0,1.02));aa[2].legend(frameon=False)
 label(aa[3],'d','Gains by instance difficulty');groups=np.array_split(np.argsort(difficulty),4);ci=[];means=[]
 for i,g in enumerate(groups):
  v=delta[g];lo,hi=boot(v,rng);m=v.mean();ci.append([float(lo),float(hi)]);means.append(float(m));aa[3].errorbar(i,m,yerr=[[m-lo],[hi-m]],fmt='o',c=C[2],capsize=3)
 aa[3].axhline(0,c='#AAAAAA',lw=.6);aa[3].set(xticks=range(4),xticklabels=['Q1','Q2','Q3','Q4'],xlabel='Input difficulty quartile',ylabel='Mean MSE reduction');aa[3].text(.03,.96,'95% paired bootstrap CI',transform=aa[3].transAxes,va='top',fontsize=6)
 RAW.update(diffusion_nfe=budgets,diffusion_mse=err,diffusion_difficulty=difficulty);SUMMARY['diffusion']={'quartile_gain':means,'ci95':ci,'bootstrap_unit':'instance','n':n};save(f,out,'paper-diffusion-evaluation','80 synthetic reconstruction instances; panel a median/IQR; paired comparisons.')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);setup();rng=np.random.default_rng(521);train(a.out,rng);align(a.out,rng);diffusion(a.out,rng);np.savez_compressed(a.out/'demo-inputs.npz',**RAW);(a.out/'summary.json').write_text(json.dumps({'provenance':'ALL DATA SYNTHETIC; NO PAPER BENCHMARK RESULTS','seed':521,'summary':SUMMARY},indent=2));print(a.out)
if __name__=='__main__':main()
