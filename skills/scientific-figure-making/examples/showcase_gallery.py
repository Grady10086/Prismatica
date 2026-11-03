"""Curated manuscript/gallery examples; every numerical input is synthetic."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D
BLUE='#55609B';ROSE='#AB6690';PEACH='#E6A385';INK='#333F49';GRAY='#B7BEC7';LIGHT='#E9ECF0'
RAW={}
def theme():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'axes.titlesize':9,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'axes.edgecolor':'#CDD2D8','axes.labelcolor':INK,'text.color':INK,'xtick.color':INK,'ytick.color':INK,'axes.linewidth':.6,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
def clean(a):a.tick_params(length=0,pad=5);a.set_axisbelow(True)
def panel(a,letter,title):a.set_title(title,loc='left',pad=13);a.text(-.12,1.065,letter,transform=a.transAxes,fontweight='bold',fontsize=10)
def footer(f,s):f.text(.07,.025,'SYNTHETIC DEMONSTRATION  ·  '+s,fontsize=6,color='#78818B')
def save(f,out,name):
 for ext in ['png','svg','pdf']:f.savefig(out/(name+'.'+ext),dpi=220,facecolor='white')
 plt.close(f)
def ci(v,rng):return np.quantile(v[rng.integers(len(v),size=(2000,len(v)))].mean(1),[.025,.975])
def atlas(out,rng):
 names=['Locate','Navigate','Reconstruct','Retrieve','Ground','Read text','Reason','Count','Plan','Control','Manipulate','Recover'];base=rng.uniform(40,72,(12,1))+rng.normal(0,3,(12,8));effects=np.array([12,8,-3,10,6,9,14,-2,8,5,13,4]);updated=np.clip(base+effects[:,None]+rng.normal(0,2.2,(12,8)),0,100);m0=base.mean(1);m1=updated.mean(1);gain=updated-base
 f=plt.figure(figsize=(10.4,5.8));f.subplots_adjust(left=.05,right=.96,top=.85,bottom=.14);a=f.add_axes([.035,.15,.52,.69],projection='polar');a.set_theta_offset(np.pi/2);a.set_theta_direction(-1);a.set_ylim(0,138);a.set_axisbelow(True)
 th=np.arange(12)*2*np.pi/12;offset=.105
 a.bar(th-offset,m0,width=.17,bottom=22,color=GRAY,lw=0,label='Baseline',zorder=3);a.bar(th+offset,m1,width=.17,bottom=22,color=BLUE,lw=0,label='Updated',zorder=3)
 a.set_yticks([22,47,72,97,122],labels=['0','25','50','75','100']);a.set_rlabel_position(345)
 for tick in a.get_yticklabels():tick.set_bbox({'facecolor':'white','edgecolor':'none','pad':.7,'alpha':.9});tick.set_zorder(8)
 a.tick_params(axis='y',labelsize=5.5,colors='#89929B');a.yaxis.grid(color=LIGHT,lw=.6);a.xaxis.grid(False);a.spines['polar'].set_visible(False);a.set_xticks([])
 for t,n in zip(th,names):
  deg=np.degrees(t);rot=(-deg+90)%180-90;a.text(t,132,n,ha='center',va='center',rotation=rot,rotation_mode='anchor',fontsize=7.2)
 a.text(0,0,f'{m1.mean():.1f}',ha='center',va='center',fontsize=14,color=BLUE,fontweight='bold');a.text(.5,.455,'mean score',transform=a.transAxes,ha='center',va='center',fontsize=5,color='#78818B');f.text(.045,.93,'a  Benchmark coverage',fontsize=11,fontweight='bold');f.legend(handles=[Line2D([],[],color=GRAY,lw=5,label='Baseline'),Line2D([],[],color=BLUE,lw=5,label='Updated')],loc='upper left',bbox_to_anchor=(.05,.9),frameon=False,ncol=2)
 b=f.add_axes([.655,.15,.295,.68]);b.axvline(0,c='#A3ABB5',lw=.8)
 for i,v in enumerate(gain):
  lo,hi=ci(v,rng);m=v.mean();b.plot([lo,hi],[i,i],c=ROSE if m<0 else BLUE,lw=1.7);b.scatter(m,i,c=ROSE if m<0 else BLUE,s=19,zorder=3)
 b.set(yticks=range(12),yticklabels=names,xlabel='Paired score difference',ylim=(11.7,-.7),xlim=(-7,19));clean(b);b.xaxis.grid(color=LIGHT,lw=.6);f.text(.655,.93,'b  Improvement by task',fontsize=11,fontweight='bold');f.text(.655,.875,'Mean and 95% seed-bootstrap CI',fontsize=7,color='#78818B');footer(f,'8 matched seeds/task; radial bar length encodes score; all tasks retained.');RAW.update(atlas_baseline=base,atlas_updated=updated);save(f,out,'benchmark-atlas')
def estimation(out,rng):
 n=48;group=np.repeat(np.arange(4),12);before=rng.normal(68,9,n);after=before+np.array([7,3,-2,5])[group]+rng.normal(0,3,n);delta=after-before
 f=plt.figure(figsize=(10.4,5.8));a=f.add_axes([.08,.22,.38,.62]);b=f.add_axes([.59,.53,.35,.31]);c=f.add_axes([.59,.20,.35,.20]);panel(a,'a','Paired observations')
 for i in range(n):a.plot([0,1],[before[i],after[i]],c='#D6DCE1',lw=.65,zorder=1)
 a.scatter(np.zeros(n),before,s=11,c=GRAY,alpha=.8,zorder=2);a.scatter(np.ones(n),after,s=11,c=BLUE,alpha=.8,zorder=2)
 parts=a.violinplot([before,after],positions=[-.20,1.20],widths=.32,showextrema=False)
 for p,col in zip(parts['bodies'],[GRAY,BLUE]):p.set_facecolor(col);p.set_edgecolor('none');p.set_alpha(.20)
 a.set(xticks=[0,1],xticklabels=['Baseline','Updated'],ylabel='Task score',xlim=(-.55,1.55));clean(a);a.yaxis.grid(color=LIGHT,lw=.6)
 panel(b,'b','Distribution of within-pair change');x=np.linspace(delta.min()-3,delta.max()+3,250);y=gaussian_kde(delta)(x);b.fill_between(x,y,where=x>=0,color=BLUE,alpha=.25);b.fill_between(x,y,where=x<0,color=ROSE,alpha=.35);b.plot(x,y,c=INK,lw=.9);b.axvline(0,c=INK,lw=.7,ls='--');b.plot(delta,np.full(n,-.004),'|',c=BLUE,ms=5,alpha=.6);b.set(xlabel='Score difference (updated − baseline)',ylabel='Density');clean(b)
 panel(c,'c','Effects within predefined groups')
 for i,label in enumerate(['Spatial','Language','Counting','Control']):
  v=delta[group==i];lo,hi=ci(v,rng);m=v.mean();c.plot([lo,hi],[i,i],c=ROSE if m<0 else BLUE,lw=1.8);c.scatter(m,i,s=20,c=ROSE if m<0 else BLUE,zorder=3)
 c.axvline(0,c='#A3ABB5',lw=.7);c.set(yticks=range(4),yticklabels=['Spatial','Language','Counting','Control'],xlabel='Mean difference · 95% paired bootstrap CI',ylim=(3.7,-.7));clean(c);footer(f,'48 matched cases; 12/group; KDE and raw differences; 2,000 within-group bootstrap samples.');RAW.update(paired_before=before,paired_after=after,paired_group=group);save(f,out,'paired-estimation')
def scaling(out,rng):
 budget=np.array([4,8,16,32,64]);n=60;difficulty=rng.lognormal(-1,.5,n);errors=np.array([[difficulty/b**(.42+.055*k)+rng.uniform(.008,.020,n) for b in budget] for k in range(3)]);lat=np.array([[b*scale*rng.lognormal(0,.07,n) for b in budget] for scale in [.014,.020,.029]]);cols=[BLUE,ROSE,PEACH];markers=['o','s','^'];names=['Sampler A','Sampler B','Sampler C']
 f=plt.figure(figsize=(10.4,5.8));a=f.add_axes([.08,.21,.44,.63]);b=f.add_axes([.66,.53,.28,.31]);c=f.add_axes([.66,.20,.28,.20]);panel(a,'a','Quality–cost operating points')
 for k in range(3):
  xx=np.median(lat[k],axis=1);yy=np.median(errors[k],axis=1);a.plot(xx,yy,c=cols[k],marker=markers[k],ms=5,lw=1.5,label=names[k],markeredgecolor=INK,markeredgewidth=.4)
  a.annotate(names[k],(xx[-1],yy[-1]),xytext=(5,[-5,5,-4][k]),textcoords='offset points',fontsize=7,color=INK)
 a.set(xlabel='Latency (s) · median',ylabel='Reconstruction MSE · median ↓',xlim=(0,2.4));a.xaxis.grid(color=LIGHT,lw=.6);a.yaxis.grid(color=LIGHT,lw=.6);clean(a)
 panel(b,'b','Variability at fixed budget')
 for k in range(3):
  y=errors[k,3];q=np.quantile(y,[.25,.5,.75]);b.plot([k,k],[q[0],q[2]],color=cols[k],lw=7,solid_capstyle='round');b.scatter(k,q[1],s=14,c=INK,zorder=3)
 b.set(xticks=range(3),xticklabels=['A','B','C'],xlabel='Sampler at NFE = 32',ylabel='MSE');clean(b)
 panel(c,'c','Tail behavior at NFE = 32')
 for k in range(3):
  v=np.sort(errors[k,3]);c.step(v,np.arange(1,n+1)/n,where='post',c=cols[k],lw=1.5)
 c.set(xlabel='Reconstruction MSE',ylabel='ECDF',ylim=(0,1.02));clean(c);footer(f,'60 synthetic reconstruction instances; NFE 4–64; median/IQR in b; latency is simulated.');RAW.update(scaling_nfe=budget,scaling_errors=errors,scaling_latency=lat);save(f,out,'quality-cost')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);theme();rng=np.random.default_rng(1103);atlas(a.out,rng);estimation(a.out,rng);scaling(a.out,rng);np.savez_compressed(a.out/'showcase-inputs.npz',**RAW);(a.out/'provenance.json').write_text(json.dumps({'kind':'All data synthetic; original chart designs, not published benchmark results','seed':1103,'bootstrap_resamples':2000,'format':'10.4 × 5.8 inch gallery masters; rescale typography for the actual venue'},indent=2));print(a.out)
if __name__=='__main__':main()
