"""ROC/PR, calibration and decision-analysis compositions. Explicit synthetic data."""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import expit
from sklearn.metrics import roc_curve,roc_auc_score,precision_recall_curve,average_precision_score
import numpy as np
from nature_data_gallery import load_colors
from nature_complex_gallery import heading,finish
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature
from prediction_stats import validate,calibration_bins,net_benefit,treat_all


def cohort(seed,n,shift=0):
    rng=np.random.default_rng(seed);z=rng.normal(-1.55+shift,1.35,n);y=rng.binomial(1,expit(z));scores=np.column_stack([expit(z+rng.normal(0,.35,n)),expit(1.5*(z+rng.normal(0,.7,n))),expit(z+rng.normal(0,1.1,n)+.5)])
    return y,scores


def bootstrap(y,p,B=400,seed=925):
    
    for k in range(p.shape[1]):validate(y,p[:,k])
    if len(np.unique(y))!=2:raise ValueError('ROC/PR evaluation requires both outcome classes')
    rng=np.random.default_rng(seed);result=[]
    for _ in range(B):
        ix=rng.integers(0,len(y),len(y));sy=y[ix]
        if len(np.unique(sy))<2:continue
        result.append([[roc_auc_score(sy,p[ix,k]),average_precision_score(sy,p[ix,k])] for k in range(p.shape[1])])
    if len(result)<.95*B:raise ValueError('Too many one-class bootstrap samples')
    return np.array(result)


def discrimination(out,c,y,p):
    boots=bootstrap(y,p);fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'r','Discrimination and ranking on the same cases',f'Synthetic cohort 1 · n = {len(y)} · positives = {y.sum()} ({y.mean():.1%}) · fixed simulated probabilities')
    g=fig.add_gridspec(2,6,left=.10,right=.94,bottom=.18,top=.82,height_ratios=[1.15,.65],wspace=1.1,hspace=.7);roc=fig.add_subplot(g[0,:3]);pr=fig.add_subplot(g[0,3:]);dist=fig.add_subplot(g[1,:2]);auc=fig.add_subplot(g[1,2:4]);ap=fig.add_subplot(g[1,4:]);values=[]
    for k in range(3):
        col=c.style(k)['color'];fpr,tpr,_=roc_curve(y,p[:,k],drop_intermediate=False);precision,recall,_=precision_recall_curve(y,p[:,k]);a=roc_auc_score(y,p[:,k]);b=average_precision_score(y,p[:,k]);values.append(dict(auroc=float(a),ap=float(b),auroc_ci=np.quantile(boots[:,k,0],[.025,.975]).tolist(),ap_ci=np.quantile(boots[:,k,1],[.025,.975]).tolist()))
        roc.plot(fpr,tpr,c=col,label=f'Model {"ABC"[k]} · {a:.3f}',lw=1);pr.step(recall,precision,where='post',c=col,label=f'Model {"ABC"[k]} · AP {b:.3f}',lw=.9)
        for ax,j,v in [(auc,0,a),(ap,1,b)]:
            lo,hi=np.quantile(boots[:,k,j],[.025,.975]);ax.plot([lo,hi],[k,k],c=col,lw=1.2);ax.scatter(v,k,s=15,c=col,zorder=3)
    roc.plot([0,1],[0,1],c='#999999',ls=':',lw=.6);pr.axhline(y.mean(),c='#999999',ls=':',lw=.6,label=f'Prevalence {y.mean():.1%}')
    for ax,xlabel,ylabel,title in [(roc,'False-positive rate','True-positive rate','ROC · exact empirical thresholds'),(pr,'Recall','Precision','Precision–recall · step curve')]:ax.set(xlabel=xlabel,ylabel=ylabel,xlim=(0,1),ylim=(0,1.02));ax.set_title(title,loc='left',fontsize=7,fontweight='bold');ax.legend(fontsize=5,loc='lower right' if ax==roc else 'lower left')
    pr.legend(fontsize=5,loc='lower left',frameon=True,facecolor='white',edgecolor='white',framealpha=.95)
    for label,ls,name in [(0,'--','Negative'),(1,'-','Positive')]:
        v=np.sort(p[y==label,0]);dist.step(v,np.arange(1,len(v)+1)/len(v),where='post',c=c.style(0)['color'],ls=ls,label=f'{name}, n={len(v)}')
    dist.set(xlabel='Model A probability',ylabel='Empirical CDF',ylim=(0,1),xlim=(0,1));dist.set_title('Score separation',loc='left',fontsize=6);dist.legend(fontsize=5)
    for ax,name in [(auc,'AUROC'),(ap,'Average precision')]:ax.set(yticks=range(3),yticklabels=['A','B','C'],xlabel=name,xlim=(0,1),ylim=(2.5,-.5));ax.set_title('400 paired row resamples · 95% CI',loc='left',fontsize=5.5)
    fig.text(.10,.075,'AP is non-interpolated average precision, not trapezoidal PR area · intervals are percentile bootstrap',fontsize=5.5)
    finish(fig,out,'roc-pr-evidence');return dict(metrics=values,bootstrap_metrics=boots.tolist())


def calibration(out,c,y,p):
    summaries=[calibration_bins(y,p[:,k]) for k in range(3)];fig=plt.figure(figsize=nature.figure_size('double',height_mm=145));heading(fig,'s','Calibration, support and proper scoring',f'Synthetic cohort 1 · same {len(y)} cases · ten fixed equal-width probability bins · no recalibration fitted')
    g=fig.add_gridspec(3,3,left=.10,right=.94,bottom=.18,top=.82,width_ratios=[1,1,.9],height_ratios=[1,.8,.55],wspace=.7,hspace=.8);rel=fig.add_subplot(g[:2,:2]);hist=fig.add_subplot(g[0,2]);support=fig.add_subplot(g[1,2]);brier=fig.add_subplot(g[2,0]);ece=fig.add_subplot(g[2,1]);error=fig.add_subplot(g[2,2]);rel.plot([0,1],[0,1],c='#999999',ls=':',lw=.7)
    for k,(rows,e,b) in enumerate(summaries):
        col=c.style(k)['color'];x=np.array([r['predicted'] for r in rows]);obs=np.array([r['observed'] for r in rows]);lo=np.array([r['lo'] for r in rows]);hi=np.array([r['hi'] for r in rows]);rel.plot(x,obs,c=col,lw=.8,label=f'Model {"ABC"[k]}');rel.errorbar(x,obs,yerr=[obs-lo,hi-obs],fmt='none',ecolor=col,alpha=.4,lw=.6);rel.scatter(x,obs,s=np.array([r['n'] for r in rows])*.18,c=col,lw=0,zorder=3)
        hist.hist(p[:,k],bins=np.linspace(0,1,21),histtype='step',color=col,lw=.8);support.plot([r['bin'] for r in rows],[r['n'] for r in rows],c=col,marker='o',ms=2,lw=.7)
        brier.scatter(b,k,c=col,s=18);brier.text(b+.006,k,f'{b:.3f}',va='center',fontsize=5);ece.scatter(e,k,c=col,s=18);ece.text(e+.006,k,f'{e:.3f}',va='center',fontsize=5);error.plot(x,obs-x,c=col,marker='o',ms=2,lw=.7)
    rel.set(xlabel='Mean predicted probability in bin',ylabel='Observed positive fraction in bin',xlim=(0,1),ylim=(0,1));rel.set_title('Reliability diagram · binomial 95% Wilson intervals',loc='left',fontsize=6.5,fontweight='bold');rel.legend(loc='upper left',fontsize=5)
    handles=[rel.scatter([],[],s=n*.18,c='#888888',lw=0) for n in [20,100]];rel.add_artist(rel.get_legend());rel.legend(handles,['20','100'],title='Bin n · point area',loc='lower right',ncol=2,fontsize=5,title_fontsize=5)
    hist.set(xlabel='Predicted probability',ylabel='Cases');hist.set_title('Prediction support',loc='left',fontsize=6);support.set(xlabel='Fixed bin index',ylabel='Cases',xticks=[0,4,9]);support.set_title('Support by bin',loc='left',fontsize=6)
    for ax,label,limit in [(brier,'Brier score',.3),(ece,'Binned ECE',.25)]:ax.set(yticks=range(3),yticklabels=['A','B','C'],ylim=(2.5,-.5),xlim=(0,limit),xlabel=label);ax.set_title('Lower is better',loc='left',fontsize=6)
    error.axhline(0,c='#999999',lw=.6);error.set(xlabel='Mean predicted probability',ylabel='Observed − predicted',xlim=(0,1));error.set_title('Signed bin error',loc='left',fontsize=6)
    fig.text(.10,.075,'Empty bins omitted · Wilson intervals describe bin outcome rates · Brier score also reflects discrimination',fontsize=5)
    finish(fig,out,'calibration-diagnostics');return [dict(bins=r,ece=e,brier=b) for r,e,b in summaries]


def decision(out,c,y,p,sy,sp):
    thresholds=np.linspace(.05,.30,101);all1=treat_all(y,thresholds);all2=treat_all(sy,thresholds);nb=np.array([net_benefit(y,p[:,k],thresholds) for k in range(3)]);secondary=np.array([net_benefit(sy,sp[:,k],thresholds) for k in range(3)]);rng=np.random.default_rng(926);diff=[]
    for _ in range(400):
        ix=rng.integers(0,len(y),len(y));diff.append(net_benefit(y[ix],p[ix,0],thresholds)-treat_all(y[ix],thresholds))
    lo,hi=np.quantile(diff,[.025,.975],axis=0)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'t','Decision thresholds, utility and action rates','Two independent synthetic cohorts · fixed 5–30% threshold range · descriptive utility comparison')
    g=fig.add_gridspec(2,3,left=.10,right=.94,bottom=.18,top=.82,width_ratios=[1,1,1],height_ratios=[1,.7],wspace=.7,hspace=.8);main=fig.add_subplot(g[0,:2]);shift=fig.add_subplot(g[0,2]);delta=fig.add_subplot(g[1,:2]);action=fig.add_subplot(g[1,2]);ylow=min(all1.min(),all2.min(),nb.min(),secondary.min())-.02;yhigh=max(all1.max(),all2.max(),nb.max(),secondary.max())+.02
    for k in range(3):
        col=c.style(k)['color'];main.plot(thresholds,nb[k],c=col,label=f'Model {"ABC"[k]}',lw=1);shift.plot(thresholds,secondary[k],c=col,lw=.8);action.plot(thresholds,(p[:,k,None]>=thresholds).mean(axis=0),c=col,lw=.8)
    for ax,curve,n,rate in [(main,all1,len(y),y.mean()),(shift,all2,len(sy),sy.mean())]:
        ax.plot(thresholds,curve,c='#888888',ls='--',lw=.8,label='Act on all');ax.axhline(0,c='black',ls=':',lw=.7,label='Act on none');ax.set(xlabel='Threshold probability',ylabel='Net benefit per case',xlim=(.05,.3),ylim=(ylow,yhigh));ax.set_title(f'Cohort {1 if ax==main else 2} · n={n} · positives {rate:.1%}',loc='left',fontsize=6.5,fontweight='bold')
    main.legend(fontsize=5,ncol=2,loc='lower left');delta.fill_between(thresholds,lo,hi,color=c.style(0)['color'],alpha=.15,lw=0);delta.plot(thresholds,nb[0]-all1,c=c.style(0)['color']);delta.axhline(0,c='#888888',ls=':',lw=.6);delta.set(xlabel='Threshold probability',ylabel='Δ net benefit per case',xlim=(.05,.3));delta.set_title('Model A − act on all · paired bootstrap pointwise 95% interval',loc='left',fontsize=6)
    action.set(xlabel='Threshold probability',ylabel='Fraction acted on',xlim=(.05,.3),ylim=(0,1));action.set_title('Cohort 1 · action burden',loc='left',fontsize=6)
    fig.text(.10,.075,'NB = TP/N − FP/N × pt/(1−pt) · no threshold optimization or clinical recommendation · negative values retained',fontsize=5)
    finish(fig,out,'decision-utility');return dict(thresholds=thresholds.tolist(),net_benefit=nb.tolist(),secondary_net_benefit=secondary.tolist(),act_all=all1.tolist(),secondary_act_all=all2.tolist(),difference_lo=lo.tolist(),difference_hi=hi.tolist())


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors);y,probs=cohort(921,800);sy,sp=cohort(922,500,shift=-.45)
    result=dict(kind='SYNTHETIC DEMONSTRATION',cohort1=dict(y=y.tolist(),probabilities=probs.tolist()),cohort2=dict(y=sy.tolist(),probabilities=sp.tolist()),discrimination=discrimination(a.out,c,y,probs),calibration=calibration(a.out,c,y,probs),decision=decision(a.out,c,y,probs,sy,sp));(a.out/'data-and-summaries.json').write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
