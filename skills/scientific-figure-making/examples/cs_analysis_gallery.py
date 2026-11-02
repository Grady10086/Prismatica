"""Image-conscious CS experiment layouts; every value is synthetic demonstration data."""
import argparse, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

INK='#242B38'; MUTED='#78818C'; BG='#FAF8F3'; BLUE='#426E9C'; TEAL='#388C83'; RED='#C9685B'; GOLD='#C4A05B'
CM=LinearSegmentedColormap.from_list('ink_mint',['#F1EEE5','#B8D8CB','#559A99','#34476D'])
DATA={}
def ax(fig,rect,label,title):
 a=fig.add_axes(rect);a.set_facecolor(BG);a.text(0,1.10,label,transform=a.transAxes,fontweight='bold',fontsize=10,color=RED);a.text(.065,1.10,title,transform=a.transAxes,fontsize=9,color=INK)
 for s in ['top','right']:a.spines[s].set_visible(False)
 for s in ['left','bottom']:a.spines[s].set_color('#D6D6D1')
 a.tick_params(labelsize=7,length=2,color='#BBBDBA');return a

def page(n,title,sub):
 f=plt.figure(figsize=(12,8),facecolor=BG)
 f.text(.06,.947,f'{n}  /  COMPUTATIONAL STUDIES',fontsize=8,color=TEAL)
 f.text(.06,.875,title,fontfamily='DejaVu Serif',fontsize=30,color=INK)
 f.text(.06,.827,sub,fontsize=9,color=MUTED)
 f.text(.06,.027,'SYNTHETIC DEMONSTRATION DATA  ·  no reported model performance  ·  replace with your experiments',fontsize=7,color=MUTED)
 return f

def save(f,out,name):
 f.savefig(out/(name+'.png'),dpi=190,facecolor=BG);f.savefig(out/(name+'.svg'),facecolor=BG);plt.close(f)

def representation(out):
 rng=np.random.default_rng(24);f=page('01','Inside the representation.','Layer correspondence, token routing and specialization — one coherent analytical view.')
 # A constructed similarity matrix, explicitly not measured CKA.
 i,j=np.mgrid[:16,:16];sim=np.exp(-abs(i-j)/4)*.65+.25*np.exp(-((i-11)**2+(j-9)**2)/30);sim=np.clip(sim,0,1)
 a=ax(f,[.065,.245,.43,.49],'a','Layer correspondence · illustrative similarity');im=a.imshow(sim,cmap=CM,vmin=0,vmax=1,origin='lower',aspect='auto');a.set(xlabel='Encoder layer',ylabel='Decoder layer',xticks=[0,5,10,15],yticks=[0,5,10,15]);cb=f.colorbar(im,ax=a,fraction=.028,pad=.03);cb.ax.tick_params(labelsize=7);cb.set_label('Similarity (constructed)',fontsize=7)
 a=ax(f,[.60,.48,.34,.25],'b','Token routing across depth');x=np.arange(1,13);p=np.stack([np.linspace(.55,.15,12),np.linspace(.2,.55,12),np.linspace(.25,.3,12)]);a.stackplot(x,p,colors=['#ADC9D8',TEAL,'#DFC58E'],labels=['Visual','Text','Shared']);a.set(xlim=(1,12),ylim=(0,1),xlabel='Layer',ylabel='Routing fraction');a.legend(frameon=False,ncol=3,fontsize=7,loc='upper center',bbox_to_anchor=(.5,1.03))
 a=ax(f,[.60,.16,.34,.20],'c','Specialization without a single score');labels=['Locality','Semantic','Cross-modal','Long range'];v=np.array([[.76,.43,.31,.26],[.49,.68,.59,.46],[.29,.72,.83,.79]])
 for k,(row,col) in enumerate(zip(v,[BLUE,TEAL,RED])):a.plot(np.arange(4),row,'o-',color=col,lw=1.8,ms=4,label=['Early','Middle','Late'][k])
 a.set(xticks=np.arange(4),xticklabels=labels,ylim=(0,1),ylabel='Probe score (a.u.)');a.legend(ncol=3,frameon=False,fontsize=7,loc='lower left')
 f.text(.065,.12,'Read across scales',fontfamily='DejaVu Serif',fontsize=16,color=INK);f.text(.065,.085,'Global alignment → routing dynamics → layer-wise probes',fontsize=8,color=MUTED)
 DATA['representation']={'constructed_similarity':sim.tolist(),'routing':p.tolist(),'probe_scores':v.tolist()};save(f,out,'cs-representation')

def ablation(out):
 rng=np.random.default_rng(19);f=page('02','What actually matters?','A complete 2³ factorial design connects configuration scores to effects and interactions.')
 configs=np.array([[int(b) for b in f'{k:03b}'] for k in range(8)]);runs=[]
 for A,B,C in configs:runs.append(68+5*A+2*B+3*C+3*A*B-2*B*C+rng.normal(0,.65,6))
 runs=np.array(runs);mean=runs.mean(1);se=runs.std(1,ddof=1)/np.sqrt(6)
 a=ax(f,[.09,.25,.30,.46],'a','All configurations · six seeds');y=np.arange(8);a.errorbar(mean,y,xerr=se,fmt='o',color=BLUE,ecolor='#B4BBC1',capsize=3);a.set(yticks=y,yticklabels=[''.join(map(str,c)) for c in configs],xlabel='Task score · mean ± SEM',ylabel='A / B / C enabled',ylim=(-.6,7.6));a.axvline(mean[0],ls=':',color=MUTED,lw=.8)
 a=ax(f,[.51,.46,.41,.25],'b','B changes the contribution of A');
 for b,col in [(0,BLUE),(1,RED)]:
  vals=[mean[(configs[:,0]==aa)&(configs[:,1]==b)].mean() for aa in [0,1]];a.plot([0,1],vals,'o-',color=col,lw=2,label=f'B = {b}')
 a.set(xticks=[0,1],xticklabels=['A disabled','A enabled'],ylabel='Score · averaged over C');a.legend(frameon=False,fontsize=8)
 a=ax(f,[.51,.15,.41,.18],'c','Marginal effects · average over other factors');effects=np.array([mean[configs[:,k]==1].mean()-mean[configs[:,k]==0].mean() for k in range(3)]);a.hlines(range(3),0,effects,color=['#426E9C',TEAL,RED],lw=3);a.scatter(effects,range(3),c=[BLUE,TEAL,RED],s=40,zorder=3);a.axvline(0,color=MUTED,lw=.7);a.set(yticks=range(3),yticklabels=['A · fusion','B · routing','C · auxiliary'],xlabel='Average score difference',ylim=(-.5,2.5))
 f.text(.09,.11,'A · Fusion    B · Routing    C · Auxiliary objective',fontsize=8,color=INK)
 DATA['ablation']={'configurations':configs.tolist(),'seed_scores':runs.tolist(),'mean':mean.tolist(),'sem':se.tolist(),'marginal_effects':effects.tolist()};save(f,out,'cs-factorial-ablation')

def performance(out):
 f=page('03','Accuracy has a cost.','A deployment-oriented comparison: efficiency, scaling, robustness and task-level trade-offs.')
 names=['Atlas','Birch','Cedar','Delta','Elm','Flux'];cost=np.array([12,22,38,55,80,115]);score=np.array([68,73,72,79,81,80]);colors=[BLUE,TEAL,GOLD,RED,'#7A6FA1','#7A8C75'];pareto=[0,1,3,4]
 a=ax(f,[.065,.39,.49,.34],'a','Quality–latency frontier');a.plot(cost[pareto],score[pareto],color='#A8B1B3',ls='--',lw=1)
 for i,n in enumerate(names):a.scatter(cost[i],score[i],s=[48,70,90,120,145,170][i],color=colors[i],edgecolor=BG,zorder=3);a.annotate(n,(cost[i],score[i]),xytext=(7,5),textcoords='offset points',fontsize=7,color=INK)
 a.set(xlabel='Latency per sample (ms) ↓',ylabel='Task score ↑',xlim=(0,140),ylim=(65,85));a.text(.03,.93,'Circle area ∝ parameter count',transform=a.transAxes,fontsize=7,color=MUTED)
 a=ax(f,[.66,.43,.28,.30],'b','Performance under shift');shift=np.arange(5);rob=[]
 for i in [1,3,4]:
  v=score[i]-np.array([0,2,5,9,14])*(1+.12*(i-3));rob.append(v.tolist());a.plot(shift,v,'o-',color=colors[i],label=names[i],lw=1.5,ms=3)
 a.set(xlabel='Shift severity',ylabel='Task score',xticks=shift);a.legend(frameon=False,fontsize=7)
 a=ax(f,[.065,.13,.26,.15],'c','Budget scaling');budget=np.array([1,2,4,8,16]);scales=[]
 for i in [1,3,4]:
  v=score[i]-10/np.sqrt(budget);scales.append(v.tolist());a.plot(budget,v,'o-',color=colors[i],ms=3,lw=1.4)
 a.set_xscale('log',base=2);a.set(xlabel='Training budget (relative)',ylabel='Task score',xticks=budget,xticklabels=budget)
 a=ax(f,[.44,.13,.50,.15],'d','Task-wise gains over Birch');gains=np.array([[3,6,7,8],[6,7,10,9]]);yy=np.arange(4)
 for k,col in enumerate([RED,colors[4]]):a.scatter(gains[k],yy+(.07 if k else -.07),c=col,s=30,label=['Delta','Elm'][k])
 a.hlines(yy,np.minimum(*gains),np.maximum(*gains),color='#C5C9C8',lw=1,zorder=0);a.axvline(0,color=MUTED,lw=.7);a.set(yticks=yy,yticklabels=['Reasoning','Retrieval','Grounding','Generation'],xlabel='Score difference (points)',xlim=(-1,11),ylim=(-.5,3.5));a.legend(frameon=False,fontsize=7,ncol=2,loc='lower right')
 DATA['performance']={'models':names,'latency_ms':cost.tolist(),'score':score.tolist(),'parameter_count_relative':[48,70,90,120,145,170],'pareto_indices':pareto,'shift_scores':rob,'budget':budget.tolist(),'budget_scores':scales,'gains_over_birch':gains.tolist()};save(f,out,'cs-performance-tradeoffs')

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'svg.fonttype':'none'});representation(args.out);ablation(args.out);performance(args.out);(args.out/'demo-data.json').write_text(json.dumps({'provenance':'ALL VALUES SYNTHETIC; NOT BENCHMARK RESULTS','data':DATA},indent=2));print(args.out)
if __name__=='__main__':main()
