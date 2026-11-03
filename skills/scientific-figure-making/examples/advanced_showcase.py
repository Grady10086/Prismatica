"""Original visual studies; synthetic data with computed projection, correlations and flows."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch,Ellipse
from matplotlib.colors import LinearSegmentedColormap,Normalize,TwoSlopeNorm
from sklearn.decomposition import PCA
from scipy.stats import gaussian_kde
from showcase_gallery import theme,clean,panel,footer,save,ci,BLUE,ROSE,PEACH,INK,GRAY,LIGHT

RAW={};META={}
def circular(out,rng):
 n=18;runs=24;group=np.repeat(np.arange(3),6);latent=rng.normal(size=(runs,3));baseline=58+rng.normal(0,5,(1,n))+4.5*latent[:,group]+rng.normal(0,1.1,(runs,n));effect=np.array([8,4,6,-2,7,3,9,5,6,7,-3,5,4,8,3,5,6,4]);updated=baseline+effect+rng.normal(0,1.3,baseline.shape);mean=updated.mean(0);diff=(updated-baseline).mean(0);spread=updated.std(0,ddof=1);corr=np.corrcoef(baseline,rowvar=False);links=[(i,j,float(corr[i,j])) for i in range(n) for j in range(i+1,n) if corr[i,j]>=.8]
 f=plt.figure(figsize=(10.4,6));a=f.add_axes([.045,.16,.53,.74],projection='polar');a.set_theta_offset(np.pi/2);a.set_theta_direction(-1);a.set_ylim(0,1.25);a.axis('off');th=np.arange(n)*2*np.pi/n;w=2*np.pi/n*.82
 sequential=LinearSegmentedColormap.from_list('iris',['#F2F2F8',BLUE]);div=LinearSegmentedColormap.from_list('gain',[ROSE,'#FAF9F7',BLUE]);graymap=LinearSegmentedColormap.from_list('variation',['#F4F2F0','#71808C'])
 for values,bottom,cmap,norm in [(mean,.68,sequential,Normalize(0,100)),(diff,.84,div,TwoSlopeNorm(0,-10,10)),(spread,1.,graymap,Normalize(0,8))]:a.bar(th,np.full(n,.12),bottom=bottom,width=w,color=cmap(norm(values)),edgecolor='white',lw=.4,zorder=4)
 # Chords use the same run-level correlation matrix, no causal/network claim.
 ax=f.add_axes([.045,.16,.53,.74],frameon=False);ax.set(xlim=(-1.25,1.25),ylim=(-1.25,1.25),aspect='equal');ax.axis('off')
 for i,j,r in links:
  t1,t2=np.pi/2-th[i],np.pi/2-th[j];p1=np.array([np.cos(t1),np.sin(t1)])*.62;p2=np.array([np.cos(t2),np.sin(t2)])*.62
  path=MP([p1,p1*.18,p2*.18,p2],[MP.MOVETO,MP.CURVE4,MP.CURVE4,MP.CURVE4]);ax.add_patch(PathPatch(path,fill=False,ec=[BLUE,ROSE,PEACH][group[i]],alpha=.25,lw=.6))
 for i,t in enumerate(th):
  deg=np.degrees(t);a.text(t,1.19,f'T{i+1:02}',ha='center',va='center',rotation=(-deg+90)%180-90,fontsize=6)
 f.text(.065,.945,'a  Multi-track experiment atlas',fontsize=11,fontweight='bold');f.text(.065,.90,'Inner → outer: mean score / paired gain / seed SD',fontsize=7,color='#78818B')
 b=f.add_axes([.67,.32,.28,.54]);panel(b,'b','Performance and variability')
 for g in range(3):
  m=group==g;b.scatter(mean[m],spread[m],s=32,c=[BLUE,ROSE,PEACH][g],marker=['o','s','^'][g],edgecolor=INK,lw=.35,label=f'Group {g+1}')
 b.set(xlabel='Updated task score · mean',ylabel='Across-seed SD');clean(b);b.legend(frameon=False,loc='upper left',fontsize=6)
 for x,cmap,norm,title in [(.10,sequential,Normalize(0,100),'Mean score'),(.36,div,Normalize(-10,10),'Gain'),(.68,graymap,Normalize(0,8),'Seed SD')]:
  cbax=f.add_axes([x,.12,.19,.016]);cb=f.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap),cax=cbax,orientation='horizontal');cb.ax.tick_params(length=0,labelsize=5.5);cb.outline.set_visible(False);f.text(x,.155,title,fontsize=6,color=INK)
 footer(f,f'18 synthetic tasks × 24 shared seeds; chords show all {len(links)} baseline correlations r ≥ 0.80, not causal links.');RAW.update(circular_baseline=baseline,circular_updated=updated,circular_corr=corr);META['circular']={'correlation_threshold':.8,'links':links,'track_limits':{'mean':[0,100],'gain':[-10,10],'sd':[0,8]}};save(f,out,'circular-fingerprint')

def representations(out,rng):
 n=360;g=np.repeat(np.arange(4),90);centers=np.array([[-4,-2,1,0,1,0],[3,-3,0,1,0,1],[-1,4,1,1,0,0],[4,3,0,0,1,1]]);noise=rng.normal(size=(n,6));before=centers[g]+noise*1.7;after=centers[g]+noise*.65+rng.normal(0,.16,(n,6));pca=PCA(2).fit(np.r_[before,after]);xy=pca.transform(after);xb=pca.transform(before);col=[BLUE,ROSE,PEACH,'#748C8B'];names=['Vision','Language','Spatial','Action'];f=plt.figure(figsize=(10.4,6));a=f.add_axes([.08,.21,.48,.64]);panel(a,'a','Representation geometry · shared PCA')
 for k in range(4):
  m=g==k;pts=xy[m];a.scatter(*pts.T,s=7,c=col[k],alpha=.63,lw=0,zorder=3);xx,yy=np.meshgrid(np.linspace(pts[:,0].min()-1,pts[:,0].max()+1,80),np.linspace(pts[:,1].min()-1,pts[:,1].max()+1,80));zz=gaussian_kde(pts.T)(np.vstack([xx.ravel(),yy.ravel()])).reshape(xx.shape);a.contour(xx,yy,zz,levels=zz.max()*np.array([.15,.4,.75]),colors=[col[k]],linewidths=.65,alpha=.5,zorder=2);a.text(*pts.mean(0),names[k],fontsize=7,fontweight='bold',ha='center',va='center',bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':2},zorder=5)
 a.set_xlim(min(xb[:,0].min(),xy[:,0].min())-.5,max(xb[:,0].max(),xy[:,0].max())+.5);a.set_ylim(min(xb[:,1].min(),xy[:,1].min())-.5,max(xb[:,1].max(),xy[:,1].max())+.5)
 a.set(xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.0%} pooled variance)',ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.0%})');clean(a);a.xaxis.grid(color=LIGHT,lw=.5);a.yaxis.grid(color=LIGHT,lw=.5)
 inset=f.add_axes([.455,.69,.105,.15]);inset.scatter(*xb.T,s=1,c=GRAY,alpha=.45,lw=0);inset.set(xlim=a.get_xlim(),ylim=a.get_ylim(),xticks=[],yticks=[]);inset.set_title('Before · same axes',fontsize=5.5,pad=3);inset.spines[['top','right']].set_visible(True)
 b=f.add_axes([.69,.51,.25,.34]);panel(b,'b','Within-group distance');ratios=[]
 for k in range(4):
  m=g==k;ratio=np.linalg.norm(after[m]-after[m].mean(0),axis=1)/np.linalg.norm(before[m]-before[m].mean(0),axis=1);ratios.append(ratio);v=np.sort(ratio);b.step(v,np.arange(1,len(v)+1)/len(v),where='post',color=col[k],lw=1.4,label=names[k])
 b.axvline(1,c=GRAY,ls='--',lw=.7);b.set(xlabel='Centroid distance ratio · after/before',ylabel='ECDF',ylim=(0,1.02),xlim=(.2,1.05));clean(b)
 c=f.add_axes([.69,.20,.25,.18]);panel(c,'c','Dispersion by group')
 for k,v in enumerate(ratios):
  q=np.quantile(v,[.25,.5,.75]);c.plot([q[0],q[2]],[k,k],c=col[k],lw=5,solid_capstyle='round');c.scatter(q[1],k,s=12,c=INK,zorder=3)
 c.set(yticks=range(4),yticklabels=names,xlabel='Distance ratio · median/IQR',ylim=(3.7,-.7));clean(c);footer(f,'360 paired synthetic vectors; PCA fitted to pooled before/after; contours = relative KDE levels, not confidence regions.');RAW.update(representation_before=before,representation_after=after,representation_groups=g,representation_xy_after=xy,representation_xy_before=xb);META['representation']={'relative_kde_levels':[.15,.4,.75],'pca_variance_ratio':pca.explained_variance_ratio_.tolist(),'distance_space':'original 6-D vectors; group centroid estimated from displayed examples','ratios':[v.tolist() for v in ratios]};save(f,out,'representation-landscape')

def flow(out,rng):
 n=180;s0=np.clip(rng.normal(48,22,n),0,100);s1=np.clip(s0+rng.normal(8,16,n),0,100);s2=np.clip(s1+rng.normal(5,12,n),0,100);scores=np.array([s0,s1,s2]);states=np.digitize(scores,[35,65]);counts=np.array([np.bincount(v,minlength=3) for v in states]);tables=np.array([np.array([[np.sum((states[k]==i)&(states[k+1]==j)) for j in range(3)] for i in range(3)]) for k in range(2)]);cols=[ROSE,PEACH,BLUE];names=['<35','35–<65','≥65'];f=plt.figure(figsize=(10.4,6));a=f.add_axes([.065,.20,.56,.65]);a.set(xlim=(-.08,2.12),ylim=(-.05,1.));a.axis('off');y=np.zeros((3,3));height=.72;gap=.055
 for k in range(3):
  bottom=.055
  for j in range(3):y[k,j]=bottom;bottom+=counts[k,j]/n*height+gap
 for k,t in enumerate(tables):
  left=y[k].copy();right=y[k+1].copy()
  for i in range(3):
   for j in range(3):
    h=t[i,j]/n*height
    if not h:continue
    l,r=left[i],right[j];x0,x1=k+.035,k+1-.035
    vertices=[(x0,l),(x0+.40,l),(x1-.40,r),(x1,r),(x1,r+h),(x1-.40,r+h),(x0+.40,l+h),(x0,l+h),(x0,l)]
    path=MP(vertices,[MP.MOVETO,MP.CURVE4,MP.CURVE4,MP.CURVE4,MP.LINETO,MP.CURVE4,MP.CURVE4,MP.CURVE4,MP.CLOSEPOLY]);a.add_patch(PathPatch(path,facecolor=cols[i],alpha=.40,ec='white',lw=.35));left[i]+=h;right[j]+=h
 for k in range(3):
  for j in range(3):
   h=counts[k,j]/n*height;a.add_patch(plt.Rectangle((k-.025,y[k,j]),.05,h,facecolor=cols[j],lw=0,zorder=3));a.text(k+.045,y[k,j]+h/2,f'{names[j]}  n={counts[k,j]}',fontsize=6,va='center',color=INK,zorder=4,bbox={'facecolor':'white','edgecolor':'none','pad':1,'alpha':.9})
  a.text(k,-.035,['Baseline','Update 1','Update 2'][k],ha='center',fontsize=8,color=INK)
 f.text(.065,.94,'a  The same cases across evaluation rounds',fontsize=11,fontweight='bold');f.text(.065,.89,'Band width encodes case count; fixed score bins at every stage.',fontsize=7,color='#78818B')
 b=f.add_axes([.745,.47,.20,.36]);panel(b,'b','Gain by initial bin');gain=s2-s0
 for i in range(3):
  v=gain[states[0]==i];m=v.mean();lo,hi=ci(v,rng);b.plot([i,i],[lo,hi],c=cols[i],lw=2);b.scatter(i,m,s=25,c=cols[i],edgecolor=INK,lw=.4,zorder=3)
 b.axhline(0,c=GRAY,lw=.7);b.set(xticks=range(3),xticklabels=names,xlabel='Baseline score bin',ylabel='Mean paired gain · 95% CI');clean(b)
 c=f.add_axes([.745,.20,.20,.16]);panel(c,'c','Individual changes');v=np.sort(gain);c.vlines(np.arange(n),0,v,colors=np.where(v>=0,BLUE,ROSE),lw=.7);c.axhline(0,c=GRAY,lw=.6);c.set(xlabel='Case · sorted by change',ylabel='Score change');clean(c);footer(f,'180 matched synthetic cases; bins fixed before comparison; all flows conserved; intervals bootstrap cases within baseline bins.');RAW.update(flow_scores=scores,flow_states=states,flow_counts=counts,flow_tables=tables);META['flow']={'thresholds':[35,65],'N':n,'tables':tables.tolist()};save(f,out,'evaluation-flow')

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);theme();rng=np.random.default_rng(1104);circular(args.out,rng);representations(args.out,rng);flow(args.out,rng);np.savez_compressed(args.out/'advanced-inputs.npz',**RAW);(args.out/'provenance.json').write_text(json.dumps({'kind':'ALL INPUTS SYNTHETIC; ORIGINAL COMPOSITIONS, NOT BENCHMARK RESULTS','seed':1104,'bootstrap_resamples':2000,'metadata':META},indent=2));print(args.out)
if __name__=='__main__':main()
