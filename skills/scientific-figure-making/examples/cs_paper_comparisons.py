"""Three compact CS comparison figures; reproducible synthetic fixtures, not benchmarks."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cs_paper_data_gallery import setup,fig,label,save,boot,C
RAW={};STATS={}
def ablation(out,rng):
 # Full 2^3 design, same eight seed indices in every configuration.
 configs=np.array([[int(c) for c in f'{i:03b}'] for i in range(8)]);seed=rng.normal(0,1.2,8);scores=[]
 for A,B,D in configs:scores.append(65+4*A+2*B+3*D+2.5*A*B-1.8*B*D+seed+rng.normal(0,.65,8))
 scores=np.array(scores);f=plt.figure(figsize=(180/25.4,120/25.4));gs=f.add_gridspec(2,2,left=.14,right=.97,top=.93,bottom=.15,wspace=.6,hspace=.64,width_ratios=[1.1,1]);aa=[f.add_subplot(gs[:,0]),f.add_subplot(gs[0,1]),f.add_subplot(gs[1,1])]
 label(aa[0],'a','Complete factorial configurations');aa[0].texts[0].set_position((-.2,1.04));means=scores.mean(1);cis=np.array([boot(v,rng) for v in scores]);aa[0].errorbar(means,np.arange(8),xerr=[means-cis[:,0],cis[:,1]-means],fmt='o',c=C[0],capsize=2,ms=3);aa[0].axvline(means[0],c='#AAAAAA',ls='--',lw=.6);aa[0].set(yticks=np.arange(8),yticklabels=['  '.join(map(str,c)) for c in configs],ylabel='Configuration (A, B, C)',xlabel='Task score · mean / 95% CI',ylim=(-.6,7.6))
 label(aa[1],'b','A × B interaction · averaged over C');interaction=[]
 for B in [0,1]:
  vals=np.array([scores[(configs[:,0]==A)&(configs[:,1]==B)].mean(0) for A in [0,1]]);m=vals.mean(1);ci=np.array([boot(v,rng) for v in vals]);aa[1].errorbar([0,1],m,yerr=[m-ci[:,0],ci[:,1]-m],fmt='o-',c=C[B],capsize=2,label=f'B = {B}',ms=3);interaction.append(vals)
 aa[1].set(xticks=[0,1],xticklabels=['A off','A on'],ylabel='Task score');aa[1].legend(frameon=False)
 label(aa[2],'c','Seed-wise factorial contrasts');effects=[];names=['A','B','C','A×B','B×C']
 for k in range(3):effects.append(scores[configs[:,k]==1].mean(0)-scores[configs[:,k]==0].mean(0))
 for k,j in [(0,1),(1,2)]:
  cell=lambda a,b:scores[(configs[:,k]==a)&(configs[:,j]==b)].mean(0)
  effects.append(cell(1,1)-cell(0,1)-cell(1,0)+cell(0,0))
 for i,v in enumerate(effects):
  lo,hi=boot(v,rng);m=v.mean();aa[2].errorbar(m,i,xerr=[[m-lo],[hi-m]],fmt='o',c=C[2] if i<3 else C[1],capsize=2,ms=3)
 aa[2].axvline(0,c='#999999',lw=.6);aa[2].set(yticks=range(5),yticklabels=names,xlabel='Score contrast · mean / 95% CI',ylim=(-.6,4.8));RAW.update(factorial_configs=configs,factorial_seed_scores=scores,factorial_effects=np.array(effects));STATS['factorial']={'config_means':means.tolist(),'effect_means':np.mean(effects,axis=1).tolist()};save(f,out,'paper-factorial-interactions','8 shared seed indices; percentile bootstrap over seeds; A=fusion, B=routing, C=auxiliary.')

def conflict(out,rng):
 n=240;conditions=['Image only','Text only','Congruent','Conflict'];latent=rng.normal(size=n);u=rng.uniform(size=(4,n));correct=[]
 for k in range(2):
  prob=1/(1+np.exp(-(1.1+.18*k+.40*latent[None,:]+np.array([-.3,-.2,.6,-.8+.35*k])[:,None])));correct.append(u<prob)
 correct=np.array(correct);f,aa=fig();label(aa[0],'a','Accuracy across input conditions');rates=correct.mean(2)
 for k in range(2):
  cis=np.array([boot(v.astype(float),rng) for v in correct[k]]);aa[0].errorbar(np.arange(4)+(k-.5)*.16,rates[k],yerr=[rates[k]-cis[:,0],cis[:,1]-rates[k]],fmt='o',c=C[k],capsize=2,label=f'Model {"AB"[k]}',ms=3)
 aa[0].set(xticks=range(4),xticklabels=['Image','Text','Congr.','Conflict'],ylabel='Accuracy',ylim=(0,1));aa[0].legend(frameon=False)
 label(aa[1],'b','Conflict · paired model outcomes');a,b=correct[:,3];table=np.array([[np.sum((a==i)&(b==j)) for j in [0,1]] for i in [0,1]]);im=aa[1].imshow(table,cmap='Blues',vmin=0,vmax=n,aspect='auto')
 for i in range(2):
  for j in range(2):aa[1].text(j,i,str(table[i,j]),ha='center',va='center',fontsize=9)
 aa[1].set(xticks=[0,1],xticklabels=['Wrong','Correct'],yticks=[0,1],yticklabels=['Wrong','Correct'],xlabel='Model B',ylabel='Model A');aa[1].grid(False)
 label(aa[2],'c','Conflict-induced drop · paired by item');drops=correct[:,:, :].astype(float)[:,2]-correct[:,:, :].astype(float)[:,3]
 for k in range(2):
  v=drops[k];m=v.mean();lo,hi=boot(v,rng);aa[2].errorbar(k,m,yerr=[[m-lo],[hi-m]],fmt='o',c=C[k],capsize=3,ms=4)
 aa[2].axhline(0,c='#AAAAAA',lw=.5);aa[2].set(xticks=[0,1],xticklabels=['Model A','Model B'],ylabel='Accuracy drop',xlabel='Congruent − conflict',xlim=(-.5,1.5))
 label(aa[3],'d','Accuracy gain · paired query bootstrap');gain=correct[1].astype(float)-correct[0].astype(float);means=[]
 for i,v in enumerate(gain):
  lo,hi=boot(v,rng);m=v.mean();means.append(m);aa[3].errorbar(m,i,xerr=[[m-lo],[hi-m]],fmt='o',c=C[2],capsize=2,ms=3)
 aa[3].axvline(0,c='#AAAAAA',lw=.6);aa[3].set(yticks=range(4),yticklabels=conditions,xlabel='Accuracy difference (B − A)',ylim=(-.7,4.2));RAW.update(condition_correct=correct,condition_contingency=table);STATS['conflict']={'accuracy':rates.tolist(),'conflict_contingency':table.tolist(),'gain':means};save(f,out,'paper-modality-conflict','240 shared synthetic queries; 95% paired query-bootstrap CIs; no causal claim.')

def sampler(out,rng):
 budgets=np.array([8,16,32]);n=100;base=rng.lognormal(-1,.45,n);errors=np.array([[base/(b**(.45+.06*k))+rng.uniform(.01,.025,n) for b in budgets] for k in range(3)]);latency=np.array([[b*scale*rng.lognormal(0,.08,n) for b in budgets] for scale in [.020,.027,.036]]);threshold=.10;f,aa=fig()
 label(aa[0],'a','Reconstruction quality versus latency')
 for k in range(3):
  aa[0].plot(np.median(latency[k],axis=1),np.median(errors[k],axis=1),'o-',c=C[k],ms=3,label=f'Sampler {"ABC"[k]}')
  for j in range(3):aa[0].annotate(str(budgets[j]),(np.median(latency[k,j]),np.median(errors[k,j])),xytext=(3,4),textcoords='offset points',fontsize=5)
 aa[0].set(xlabel='Latency (s) · median',ylabel='Reconstruction MSE · median ↓');aa[0].legend(frameon=False)
 label(aa[1],'b','Latency distribution at NFE = 32');vp=aa[1].violinplot(latency[:,-1].T,showmedians=True,showextrema=False)
 for k,body in enumerate(vp['bodies']):body.set_facecolor(C[k]);body.set_alpha(.3)
 aa[1].set(xticks=[1,2,3],xticklabels=['A','B','C'],xlabel='Sampler',ylabel='Latency (s)')
 label(aa[2],'c','Paired MSE difference at NFE = 32');delta=np.stack([errors[0,-1]-errors[k,-1] for k in [1,2]])
 for k,v in enumerate(delta):
  v=np.sort(v);aa[2].step(v,np.arange(1,n+1)/n,where='post',c=C[k+1],label=['A − B','A − C'][k])
 aa[2].axvline(0,c='#999999',lw=.6);aa[2].set(xlabel='MSE reduction versus A',ylabel='Empirical cumulative probability',ylim=(0,1.02));aa[2].legend(frameon=False)
 label(aa[3],'d',f'Fraction above MSE threshold {threshold:.2f}');fail=errors>threshold
 for k in range(3):
  m=fail[k].mean(1);ci=np.array([boot(v.astype(float),rng) for v in fail[k]]);aa[3].errorbar(budgets,m,yerr=[m-ci[:,0],ci[:,1]-m],fmt='o-',c=C[k],capsize=2,ms=3,label=f'{"ABC"[k]}')
 aa[3].set(xlabel='Function evaluations (NFE)',ylabel='Threshold exceedance fraction',xticks=budgets,ylim=(0,1));aa[3].legend(frameon=False,ncol=3)
 RAW.update(sampler_nfe=budgets,sampler_mse=errors,sampler_latency=latency);STATS['sampler']={'threshold':threshold,'exceedance':fail.mean(2).tolist()};save(f,out,'paper-sampler-cost-quality','100 synthetic paired instances; threshold fixed in advance; 95% instance-bootstrap CIs in d.')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);setup();rng=np.random.default_rng(732);ablation(a.out,rng);conflict(a.out,rng);sampler(a.out,rng);np.savez_compressed(a.out/'comparison-inputs.npz',**RAW);(a.out/'comparison-summary.json').write_text(json.dumps({'provenance':'SYNTHETIC DEMONSTRATION FIXTURES; NO REPORTED BENCHMARK DATA','seed':732,'summary':STATS},indent=2));print(a.out)
if __name__=='__main__':main()
