"""Circular, dose-response and survival composition studies; explicit synthetic data."""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge,PathPatch
from matplotlib.path import Path as MP
import numpy as np
from nature_data_gallery import load_colors
from nature_complex_gallery import heading,finish
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature
from advanced_stats import hill,fit_dose,km,at_risk


def circular(out,c):
    rng=np.random.default_rng(621);m=np.repeat(range(5),12);latent=rng.normal(size=(48,5));raw=latent[:,m]+rng.normal(0,.8,(48,60));means=raw.mean(axis=0);means=(means-means.mean())/np.std(means);det=rng.uniform(.2,.95,60);count=rng.integers(10,101,60);corr=np.corrcoef(raw,rowvar=False)
    links=sorted([(i,j,float(corr[i,j])) for i in range(60) for j in range(i) if m[i]!=m[j] and abs(corr[i,j])>.3],key=lambda x:-abs(x[2]))[:18]
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=135));heading(fig,'i','Circular atlas with linked quantitative tracks','60 synthetic features · five predefined modules · 48 observations per feature')
    g=fig.add_gridspec(2,3,left=.06,right=.94,bottom=.17,top=.84,width_ratios=[1,1,.95],height_ratios=[1,.75],wspace=.6,hspace=.65);ax=fig.add_subplot(g[:,:2]);ax.set_aspect('equal');ax.axis('off');ax.set(xlim=(-1.45,1.45),ylim=(-1.45,1.45));cols=[c.style(i)['color'] for i in range(5)];angles=[]
    for k in range(5):
        start=90+k*72+3;end=start+66;ax.add_patch(Wedge((0,0),1.24,start,end,width=.045,color=cols[k],lw=0));a=np.deg2rad((start+end)/2);ax.text(1.36*np.cos(a),1.36*np.sin(a),f'Module {k+1}',ha='center',va='center',fontsize=5.5)
        for j in range(12):
            i=k*12+j;lo=start+j*66/12;hi=lo+66/12-.5;theta=np.deg2rad((lo+hi)/2);angles.append(theta)
            ax.add_patch(Wedge((0,0),1.16,lo,hi,width=.11,color=c.cmap('diverging')((np.clip(means[i],-3,3)+3)/6),lw=0))
            ax.add_patch(Wedge((0,0),.82+.17*det[i],lo,hi,width=.17*det[i],color=cols[k],alpha=.55,lw=0))
            ax.plot([.65*np.cos(theta),(.65+.10*count[i]/100)*np.cos(theta)],[.65*np.sin(theta),(.65+.10*count[i]/100)*np.sin(theta)],c='#50545E',lw=.65)
    for i,j,r in links:
        p=np.array([[.59*np.cos(angles[i]),.59*np.sin(angles[i])],[0,0],[.59*np.cos(angles[j]),.59*np.sin(angles[j])]])
        ax.add_patch(PathPatch(MP(p,[MP.MOVETO,MP.CURVE3,MP.CURVE3]),facecolor='none',edgecolor='#767B85',lw=.4,alpha=.4))
    ax.text(0,0,f'{len(links)} links\n|r| > 0.30',ha='center',va='center',fontsize=5.5,bbox=dict(facecolor='white',edgecolor='none',pad=2))
    scax=fig.add_subplot(g[0,2]);sc=scax.scatter(det,means,s=count*.22,c=[cols[k] for k in m],alpha=.7,lw=0);scax.axhline(0,c='#BBBBBB',lw=.5);scax.set(xlabel='Detection fraction',ylabel='Standardized feature mean',xlim=(0,1));scax.set_title('Every feature in Cartesian coordinates',loc='left',fontsize=5.5)
    handles=[scax.scatter([],[],s=n*.22,c='#777777',lw=0) for n in [20,100]];scax.legend(handles,['20','100'],title='Count · point area',loc='lower left',fontsize=5,title_fontsize=5)
    summ=fig.add_subplot(g[1,2])
    for k in range(5):
        q=np.quantile(det[m==k],[.25,.5,.75]);summ.plot(q[[0,2]],[k,k],c=cols[k],lw=2);summ.scatter(q[1],k,s=13,c=cols[k])
    summ.set(yticks=range(5),yticklabels=[f'M{k+1}' for k in range(5)],xlim=(0,1),xlabel='Detection median and IQR');summ.invert_yaxis();summ.set_title('Predefined module summaries',loc='left',fontsize=6)
    fig.text(.08,.11,'Outside → inside: module identity · standardized mean · detection (0–1) · count (0–100)',fontsize=5.5)
    cb=fig.add_axes([.12,.073,.35,.012]);fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(-3,3),cmap=c.cmap('diverging')),cax=cb,orientation='horizontal',ticks=[-3,0,3]);cb.tick_params(labelsize=5,length=2)
    finish(fig,out,'circular-multitrack');return dict(raw=raw.tolist(),module=m.tolist(),standardized_means=means.tolist(),detection_fraction=det.tolist(),counts=count.tolist(),links=links)


def dose(out,c):
    rng=np.random.default_rng(622);x=np.linspace(-3,2,10);grid=np.linspace(-3,2,150);data=[];results=[]
    for k in range(3):
        y=hill(x,5,95,[-.8,-.1,.55][k],1.1)[:,None]+rng.normal(0,4,(10,5));fit=fit_dose(np.repeat(x,5),y.ravel());boots=[]
        for _ in range(200):
            by=np.array([v[rng.integers(0,5,5)] for v in y])
            try:boots.append(fit_dose(np.repeat(x,5),by.ravel()))
            except (RuntimeError,ValueError):pass
        if len(boots)<180:raise ValueError('Too many failed bootstrap fits')
        boots=np.array(boots);data.append(y);results.append((fit,boots))
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=130));heading(fig,'j','Dose response from observations to fitted potency','Three synthetic conditions · 10 positive doses × 5 independent observations · increasing 4PL model')
    g=fig.add_gridspec(2,3,left=.10,right=.94,bottom=.17,top=.82,width_ratios=[1,1,1.1],height_ratios=[1,.65],wspace=.7,hspace=.7);ax=fig.add_subplot(g[0,:2]);res=fig.add_subplot(g[1,:2]);pot=fig.add_subplot(g[0,2]);dist=fig.add_subplot(g[1,2])
    for k,(y,(fit,boot)) in enumerate(zip(data,results)):
        col=c.style(k)['color'];curves=np.array([hill(grid,*p) for p in boot]);lo,hi=np.quantile(curves,[.025,.975],axis=0)
        ax.fill_between(10**grid,lo,hi,color=col,alpha=.15,lw=0);ax.plot(10**grid,hill(grid,*fit),color=col,label=f'Condition {k+1}',lw=1.1);ax.scatter(np.repeat(10**x,5),y.ravel(),s=5,c=col,alpha=.4,lw=0)
        res.scatter(np.repeat(10**x,5),y.ravel()-hill(np.repeat(x,5),*fit),s=5,c=col,alpha=.45,lw=0)
        q=10**np.quantile(boot[:,2],[.025,.5,.975]);pot.plot(q[[0,2]],[k,k],c=col,lw=1.3);pot.scatter(10**fit[2],k,s=20,c=col)
        residual=y.ravel()-hill(np.repeat(x,5),*fit);v=np.sort(residual);dist.step(v,np.arange(1,51)/50,where='post',c=col)
    ax.set(xscale='log',ylabel='Response (%)',ylim=(-10,115),xlim=(.001,100));ax.legend(fontsize=5);ax.set_title('Raw observations + fitted response',loc='left',fontweight='bold',fontsize=7)
    res.axhline(0,c='#777777',lw=.6);res.set(xscale='log',xlim=(.001,100),xlabel='Concentration (μM)',ylabel='Residual (pp)');res.set_title('Residuals in the measured units',loc='left',fontsize=6)
    pot.set(xscale='log',yticks=range(3),yticklabels=['C1','C2','C3'],xlabel='Fitted EC50 (μM)');pot.invert_yaxis();pot.set_xticks([.1,1,5]);pot.set_xticklabels(['0.1','1','5']);pot.set_xlim(.08,6);pot.xaxis.set_minor_formatter(plt.NullFormatter());pot.set_title('EC50 · bootstrap 95% interval',loc='left',fontsize=6)
    dist.set(xlabel='Residual (pp)',ylabel='Empirical CDF',ylim=(0,1));dist.set_title('Residual distribution',loc='left',fontsize=6)
    fig.text(.1,.075,'Bands: pointwise 95% percentile bootstrap · 200 within-dose resamples · not prediction intervals',fontsize=5.5)
    finish(fig,out,'dose-response');return dict(log10_dose=x.tolist(),responses=[v.tolist() for v in data],fits=[p.tolist() for p,_ in results],bootstrap_parameters=[b.tolist() for _,b in results])


def survival(out,c):
    rng=np.random.default_rng(623);groups=[]
    for scale in [16,23,30]:
        failure=rng.weibull(1.3,80)*scale;censor=np.minimum(rng.uniform(12,40,80),36);groups.append((np.minimum(failure,censor),(failure<=censor).astype(int)))
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=140));heading(fig,'k','Time-to-event evidence with censoring','Three synthetic groups · n = 80 each · right censoring · no treatment or causal claim')
    g=fig.add_gridspec(3,3,left=.10,right=.94,bottom=.17,top=.83,width_ratios=[1,1,1.1],height_ratios=[1,.42,.65],wspace=.7,hspace=.65);ax=fig.add_subplot(g[:2,:2]);risk=fig.add_subplot(g[2,:2]);follow=fig.add_subplot(g[:2,2]);summ=fig.add_subplot(g[2,2]);ticks=np.array([0,6,12,18,24,30,36]);summary=[]
    for k,(t,e) in enumerate(groups):
        col=c.style(k)['color'];u,s,lo,hi=km(t,e);ax.step(u,s,where='post',c=col,label=f'Group {k+1}',lw=1);ax.fill_between(u,lo,hi,step='post',color=col,alpha=.12,lw=0);ct=t[e==0];cy=s[np.searchsorted(u,ct,side='right')-1];ax.scatter(ct,cy,marker='+',s=10,c=col,lw=.6)
        for j,n in enumerate(at_risk(t,ticks)):risk.text(ticks[j],k,str(n),ha='center',va='center',fontsize=5.5)
        # All follow-up durations shown; events are filled circles, censoring is a plus.
        y=k+rng.uniform(-.16,.16,len(t));follow.scatter(t[e==1],y[e==1],s=5,c=col,lw=0,alpha=.5);follow.scatter(t[e==0],y[e==0],s=9,c=col,marker='+',lw=.5)
        idx=np.searchsorted(u,18,side='right')-1;summ.plot([lo[idx],hi[idx]],[k,k],c=col,lw=1.2);summ.scatter(s[idx],k,s=16,c=col)
        summary.append(dict(at_risk=at_risk(t,ticks).tolist(),events=int(e.sum()),censored=int((1-e).sum()),survival_18=float(s[idx]),ci_18=[float(lo[idx]),float(hi[idx])]))
    ax.set(xlim=(0,36),ylim=(0,1.02),xticks=ticks,xlabel='Follow-up (months)',ylabel='Survival probability');ax.set_title('Kaplan–Meier · pointwise 95% confidence bands',loc='left',fontsize=6.5,fontweight='bold');ax.legend(fontsize=5);ax.text(.97,.05,'+ censored',transform=ax.transAxes,ha='right',fontsize=5)
    risk.set(xlim=(0,36),ylim=(2.5,-.5),yticks=range(3),yticklabels=['Group 1','Group 2','Group 3'],xticks=ticks,xlabel='Follow-up (months)');risk.set_title('At risk immediately before each time',loc='left',fontsize=6);risk.tick_params(axis='y',length=0,pad=16)
    for sp in risk.spines.values():sp.set_visible(False)
    follow.set(yticks=range(3),yticklabels=['G1','G2','G3'],xlim=(0,36),xlabel='Observed duration (months)');follow.invert_yaxis();follow.set_title('Every case · event ● / censor +',loc='left',fontsize=6)
    summ.set(yticks=range(3),yticklabels=['G1','G2','G3'],xlim=(0,1),xlabel='Survival at 18 months');summ.invert_yaxis();summ.set_title('Estimate and pointwise 95% CI',loc='left',fontsize=6)
    fig.text(.1,.075,'Confidence bands: Greenwood variance, log–log transform · risk counts include tied events/censors at that time',fontsize=5)
    finish(fig,out,'survival-evidence');return dict(groups=[dict(time=t.tolist(),event=e.tolist()) for t,e in groups],risk_times=ticks.tolist(),summary=summary)


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors)
    data={name:draw(a.out,c) for name,draw in [('circular',circular),('dose',dose),('survival',survival)]};(a.out/'data-and-summaries.json').write_text(json.dumps(dict(kind='SYNTHETIC DEMONSTRATION',seeds=[621,622,623],data=data),indent=2));print(a.out)
if __name__=='__main__':main()
