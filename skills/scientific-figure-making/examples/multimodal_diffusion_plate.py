"""Original multimodal and diffusion plates; synthetic embeddings/logits, computed toy sampling."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,TwoSlopeNorm
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch
from scipy.special import softmax
from scipy.stats import gaussian_kde
from showcase_gallery import theme,save,ci
BLUE='#4266A0';TEAL='#328E89';ROSE='#B9647C';GOLD='#C69B4B';INK='#333F49';GRAY='#B7BEC7'
COL=[BLUE,TEAL,ROSE,GOLD];RAW={}
SEQ=LinearSegmentedColormap.from_list('depth',['#F7F5F0','#B0CAD5',BLUE,'#233B61'])
DIV=LinearSegmentedColormap.from_list('change',[ROSE,'#F8F6F1',TEAL])
def panel(a,l,title):
 a.set_title(title,loc='left',fontsize=8,pad=6);a.text(-min(.13,.022/a.get_position().width),1.04,l,transform=a.transAxes,fontweight='bold',fontsize=10);a.tick_params(length=2,width=.5,pad=2,labelsize=6);a.spines[['top','right']].set_visible(False)
def finish(f,out,name,kind):
 f.text(.06,.014,kind+' · original layouts · definitions and inputs in gallery',fontsize=5.5,color='#7B858D');save(f,out,name)
def ramp(a,im,label):
 cb=a.figure.colorbar(im,ax=a,fraction=.037,pad=.025);cb.set_label(label,fontsize=6);cb.ax.tick_params(labelsize=5,length=2)
def norm(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
def ranks(s):return 1+np.sum(s>np.diag(s)[:,None],axis=1)
def retrieval(out,rng):
 n=96;group=np.repeat(np.arange(4),24);centres=rng.normal(0,.35,(4,24));latent=rng.normal(0,1,(n,24))+centres[group];noise=rng.normal(size=(n,24));image=norm(latent+rng.normal(0,.6,(n,24)));text0=norm(latent+noise*1.6);text1=norm(latent+noise*.95);sim=np.array([image@text0.T,image@text1.T]);rank=np.array([[ranks(s),ranks(s.T)] for s in sim]);f=plt.figure(figsize=(11.5,6.6));g=f.add_gridspec(2,3,left=.06,right=.955,bottom=.09,top=.94,wspace=.44,hspace=.34,width_ratios=[1,1,.95])
 for k in range(2):
  a=f.add_subplot(g[0,k]);panel(a,'ab'[k],['Baseline alignment','Updated alignment'][k]);im=a.imshow(sim[k],vmin=-1,vmax=1,cmap=DIV,interpolation='nearest');a.set(xlabel='Text ID · fixed group order',ylabel='Image ID',xticks=[0,47,95],xticklabels=['1','48','96'],yticks=[0,47,95],yticklabels=['1','48','96'])
  for boundary in [23.5,47.5,71.5]:a.axhline(boundary,c='white',lw=.6);a.axvline(boundary,c='white',lw=.6)
  if k==1:ramp(a,im,'Cosine similarity')
 c=f.add_subplot(g[0,2]);panel(c,'c','True pair versus nearest distractor')
 for k in range(2):
  other=sim[k].copy();np.fill_diagonal(other,-np.inf);v=np.diag(sim[k])-other.max(1);xx=np.linspace(-.65,.65,200);d=gaussian_kde(v)(xx);c.fill_between(xx,d,color=COL[k],alpha=.15);c.plot(xx,d,c=COL[k],lw=1.1,label=['Baseline','Updated'][k])
 c.axvline(0,c=GRAY,lw=.6,ls='--');c.set(xlabel='Cosine margin · paired − distractor',ylabel='Density');c.legend(frameon=False,fontsize=6)
 d=f.add_subplot(g[1,0]);panel(d,'d','Bidirectional retrieval')
 for k in range(2):
  for direction in range(2):d.plot(np.arange(1,21),[(rank[k,direction]<=v).mean() for v in range(1,21)],c=COL[k],ls=['-','--'][direction],lw=1.2,label=['Base','Updated'][k]+[' I→T',' T→I'][direction])
 d.set(xlabel='Retrieval cutoff k',ylabel='Recall@k',ylim=(0,1.03),xticks=[1,5,10,20]);d.legend(frameon=False,fontsize=5.5,ncol=2,loc='lower right')
 e=f.add_subplot(g[1,1]);panel(e,'e','Query-level reciprocal-rank changes');gain=1/rank[1,0]-1/rank[0,0];order=np.argsort(gain);e.bar(np.arange(n),gain[order],width=1,color=np.array(COL)[group[order]],lw=0);e.axhline(0,c=GRAY,lw=.6);e.set(xlabel='Query · ordered by change',ylabel='Δ reciprocal rank',xlim=(0,n))
 for j,label in enumerate(['Spatial','Text','Objects','Action']):e.plot([],[],c=COL[j],lw=3,label=label)
 e.legend(frameon=False,fontsize=5.5,ncol=2,loc='upper left')
 h=f.add_subplot(g[1,2]);panel(h,'f','Recall@1 change by query group')
 for j in range(4):
  v=(rank[1,0,group==j]==1).astype(float)-(rank[0,0,group==j]==1);lo,hi=ci(v,rng);h.plot([lo,hi],[j,j],c=COL[j],lw=2);h.scatter(v.mean(),j,c=COL[j],s=22)
 h.axvline(0,c=GRAY,lw=.6);h.set(yticks=range(4),yticklabels=['Spatial','Text','Objects','Action'],xlabel='Paired Δ · 95% query-bootstrap CI',ylim=(3.6,-.6));RAW.update(retrieval_image=image,retrieval_text_base=text0,retrieval_text_updated=text1,retrieval_similarity=sim,retrieval_rank=rank,retrieval_group=group);finish(f,out,'multimodal-retrieval','SYNTHETIC EMBEDDINGS · 96 matched pairs · 96 candidates/query')
def flow(a,states,cols):
 n=states.shape[1];counts=np.array([np.bincount(v,minlength=3) for v in states]);yy=np.zeros((3,3));height=.75;gap=.06
 for k in range(3):
  p=.02
  for j in range(3):yy[k,j]=p;p+=counts[k,j]/n*height+gap
 for k in range(2):
  left=yy[k].copy();right=yy[k+1].copy()
  for i in range(3):
   for j in range(3):
    count=np.sum((states[k]==i)&(states[k+1]==j));h=count/n*height
    if not count:continue
    l,r=left[i],right[j];x0,x1=k+.035,k+1-.035;p=[(x0,l),(x0+.4,l),(x1-.4,r),(x1,r),(x1,r+h),(x1-.4,r+h),(x0+.4,l+h),(x0,l+h),(x0,l)];a.add_patch(PathPatch(MP(p,[MP.MOVETO,MP.CURVE4,MP.CURVE4,MP.CURVE4,MP.LINETO,MP.CURVE4,MP.CURVE4,MP.CURVE4,MP.CLOSEPOLY]),facecolor=cols[i],ec='white',lw=.3,alpha=.45));left[i]+=h;right[j]+=h
 for k in range(3):
  for j in range(3):
   h=counts[k,j]/n*height;a.add_patch(plt.Rectangle((k-.025,yy[k,j]),.05,h,color=cols[j],lw=0));a.text(k+.045,yy[k,j]+h/2,str(counts[k,j]),fontsize=6,va='center',bbox=dict(facecolor='white',edgecolor='none',pad=.6))
 a.set(xlim=(-.07,2.18),ylim=(-.08,1),xticks=range(3),xticklabels=['Image only','Aligned text','Conflicting text'],yticks=[]);a.spines[:].set_visible(False);return counts
def conflict(out,rng):
 n=240;quality=rng.uniform(.1,1,n);text_strength=rng.uniform(.15,1,n);shared=rng.normal(0,.65,(n,3));logits=np.array([np.column_stack([quality*2.4,quality*.3,np.ones(n)*.8])+shared,np.column_stack([quality*2.4+.8,quality*.3,np.ones(n)*.8])+shared,np.column_stack([quality*2.4,text_strength*2.6,np.ones(n)*.8])+shared]);prob=softmax(logits,axis=-1);states=prob.argmax(-1);p=prob[:,:,0];f=plt.figure(figsize=(11.5,6.5));g=f.add_gridspec(2,3,left=.06,right=.95,bottom=.09,top=.94,wspace=.48,hspace=.34)
 a=f.add_subplot(g[0,:2]);panel(a,'a','Answer identity under matched evidence changes');counts=flow(a,states,[TEAL,ROSE,GOLD]);a.text(.01,.98,'Visual answer',c=TEAL,transform=a.transAxes,fontsize=6);a.text(.28,.98,'Text alternative',c=ROSE,transform=a.transAxes,fontsize=6);a.text(.61,.98,'Other',c=GOLD,transform=a.transAxes,fontsize=6)
 b=f.add_subplot(g[0,2]);panel(b,'b','Conflict-response surface');q=np.linspace(.1,1,80);t=np.linspace(.15,1,80);qq,tt=np.meshgrid(q,t);surface=softmax(np.stack([2.4*qq,2.6*tt,np.full_like(qq,.8)],-1),axis=-1)[:,:,0];im=b.imshow(surface,origin='lower',extent=[.1,1,.15,1],aspect='auto',vmin=0,vmax=1,cmap=SEQ);b.contour(qq,tt,surface,levels=[.25,.5,.75],colors='white',linewidths=.6);b.set(xlabel='Visual quality',ylabel='Conflicting text strength');ramp(b,im,'P(visual answer)')
 c=f.add_subplot(g[1,0]);panel(c,'c','Correct-answer probability by condition')
 for k in range(3):
  parts=c.violinplot(p[k],positions=[k],widths=.7,showextrema=False)
  for body in parts['bodies']:body.set_facecolor([BLUE,TEAL,ROSE][k]);body.set_alpha(.3);body.set_edgecolor('none')
  c.scatter(k+np.linspace(-.15,.15,n),p[k],c=[BLUE,TEAL,ROSE][k],s=2,alpha=.18,lw=0);c.scatter(k,p[k].mean(),c=INK,s=15,zorder=3)
 c.set(xticks=range(3),xticklabels=['Image','Aligned','Conflict'],ylabel='P(visual answer)',ylim=(0,1))
 d=f.add_subplot(g[1,1]);panel(d,'d','Conflict penalty by visual quality')
 bounds=[]
 for j in range(4):
  mask=(quality>=.1+j*.225)&(quality<.1+(j+1)*.225);v=p[2,mask]-p[0,mask];lo,hi=ci(v,rng);bounds.extend([lo,hi]);d.plot([lo,hi],[j,j],c=COL[j],lw=2);d.scatter(v.mean(),j,c=COL[j],s=20)
 d.axvline(0,c=GRAY,lw=.6);d.set(yticks=range(4),yticklabels=['Low','Mid-low','Mid-high','High'],xlabel='Paired ΔP · 95% case-bootstrap CI',ylim=(3.6,-.6),xlim=(min(bounds)-.025,max(bounds)+.025))
 e=f.add_subplot(g[1,2]);panel(e,'e','Selective prediction under conflict');confidence=prob[2].max(-1);order=np.argsort(-confidence);wrong=states[2]!=0;risk=np.cumsum(wrong[order])/np.arange(1,n+1);e.plot(np.arange(1,n+1)/n,risk,c=ROSE,lw=1.5);e.axhline(wrong.mean(),c=GRAY,lw=.7,ls='--',label='All-case error');e.set(xlabel='Retained case fraction',ylabel='Error among retained cases',ylim=(0,1));e.legend(frameon=False,fontsize=6);RAW.update(conflict_logits=logits,conflict_probabilities=prob,conflict_states=states,conflict_counts=counts,conflict_quality=quality,conflict_text_strength=text_strength,conflict_surface=surface);finish(f,out,'multimodal-conflict','SYNTHETIC LOGITS · 240 matched cases · visual answer is the stipulated target')
# VE probability-flow ODE for a known eight-mode Gaussian mixture. No neural model is trained.
CENTRES=np.column_stack([np.cos(np.arange(8)*np.pi/4),np.sin(np.arange(8)*np.pi/4)])*2
SIGMA=.16

def drift(x,s):
 v=SIGMA**2+s*s;diff=x[:,None,:]-CENTRES[None,:,:];weights=softmax(-np.sum(diff**2,axis=-1)/(2*v),axis=1);score=-np.sum(weights[:,:,None]*diff,axis=1)/v;return -s*score

def integrate(x0,nfe,method,keep=False):
 if method not in ['Euler','Heun','Midpoint']:raise ValueError('Unknown integration method')
 if nfe<=0 or int(nfe)!=nfe or (method!='Euler' and nfe%2):raise ValueError('NFE must be positive; two-stage methods require an even budget')
 steps=int(nfe) if method=='Euler' else int(nfe)//2;s=np.geomspace(3,.01,steps+1);x=x0.copy();path=[x.copy()]
 for lo,hi in zip(s[:-1],s[1:]):
  h=hi-lo;k=drift(x,lo)
  if method=='Euler':x=x+h*k
  elif method=='Heun':x=x+h*(k+drift(x+h*k,hi))/2
  else:x=x+h*drift(x+h*k/2,(lo+hi)/2)
  path.append(x.copy())
 return x,np.array(path),s

def diffusion(out,rng):
 n=384;mode=rng.integers(8,size=n);x0=CENTRES[mode]+rng.normal(size=(n,2))*np.sqrt(9+SIGMA**2);ref,_,_=integrate(x0,2048,'Heun');budgets=np.array([8,16,32,64]);names=['Euler','Heun','Midpoint'];outputs=[];errors=[]
 for method in names:
  outs=np.array([integrate(x0,int(b),method)[0] for b in budgets]);outputs.append(outs);errors.append(np.linalg.norm(outs-ref[None],axis=-1))
 outputs=np.array(outputs);errors=np.array(errors);_,path,s=integrate(x0,32,'Heun');f=plt.figure(figsize=(11.5,7));g=f.add_gridspec(3,4,left=.055,right=.955,bottom=.08,top=.94,wspace=.52,hspace=.32,height_ratios=[.85,1,1])
 a=f.add_subplot(g[0,:]);panel(a,'a','Probability-flow samples · same initial particles at every checkpoint');a.axis('off');chosen=[0,4,8,12,16];mode_colors=np.array(['#4266A0','#328E89','#B9647C','#C69B4B','#7596BB','#75B0A0','#C994A3','#D8BD82']);final_mode=np.linalg.norm(path[-1,:,None,:]-CENTRES[None,:,:],axis=-1).argmin(1)
 for j,idx in enumerate(chosen):
  ax=a.inset_axes([j*.202,.04,.182,.92]);ax.scatter(path[idx,:,0],path[idx,:,1],s=2,c=mode_colors[final_mode],alpha=.65,lw=0);radius=np.ceil(np.abs(path[idx]).max()*1.03);ax.set(xlim=(-radius,radius),ylim=(-radius,radius),aspect='equal',xticks=[],yticks=[]);ax.spines[:].set_visible(False);ax.set_title(f'σ = {s[idx]:.2f} · axes ±{radius:g}',fontsize=7,pad=2)
  if j<4:a.text((j+.92)*.202,.5,'→',transform=a.transAxes,fontsize=11,c=GRAY)
 b=f.add_subplot(g[1:,0:2]);panel(b,'b','Particle trajectories and final modes')
 xx=np.linspace(-3,3,160);yy=np.linspace(-3,3,160);gx,gy=np.meshgrid(xx,yy);v=SIGMA**2+.01**2;pdf=np.exp(-((gx[:,:,None]-CENTRES[:,0])**2+(gy[:,:,None]-CENTRES[:,1])**2)/(2*v)).sum(-1);b.contour(gx,gy,pdf,levels=[.1,.35,.7],colors=[GRAY,TEAL,BLUE],linewidths=.6)
 for j in range(0,96,3):b.plot(path[:,j,0],path[:,j,1],c=mode_colors[final_mode[j]],alpha=.65,lw=.6)
 b.scatter(path[-1,:,0],path[-1,:,1],c=mode_colors[final_mode],s=3,alpha=.5,lw=0);b.set(xlim=(-3.6,3.6),ylim=(-3.6,3.6),aspect='equal',xlabel='x₁',ylabel='x₂')
 c=f.add_subplot(g[1,2:]);panel(c,'c','Numerical convergence at equal score-call budget')
 for k,name in enumerate(names):
  q=np.quantile(errors[k],[.25,.5,.75],axis=1);c.fill_between(budgets,q[0],q[2],color=COL[k],alpha=.12);c.plot(budgets,q[1],c=COL[k],marker=['o','s','^'][k],ms=3,lw=1.2,label=name)
 c.set(xscale='log',yscale='log',xlabel='Score evaluations (NFE)',ylabel='Endpoint L2 error');c.legend(frameon=False,ncol=3,fontsize=6)
 d=f.add_subplot(g[2,2]);panel(d,'d','Distance to mode centre · NFE 8');count=np.array([np.bincount(np.linalg.norm(v[:,None,:]-CENTRES[None,:,:],axis=-1).argmin(1),minlength=8) for v in outputs[:,2]]);residual=np.array([np.linalg.norm(v[:,None,:]-CENTRES[None,:,:],axis=-1).min(1) for v in outputs[:,0]])
 for k in range(3):
  parts=d.violinplot(residual[k],positions=[k],widths=.7,showextrema=False)
  for body in parts['bodies']:body.set_facecolor(COL[k]);body.set_alpha(.35);body.set_edgecolor('none')
  d.scatter(k,np.median(residual[k]),c=COL[k],s=10)
 d.set(xticks=range(3),xticklabels=names,ylabel='Nearest-centre L2 distance');d.tick_params(axis='x',labelsize=5)
 e=f.add_subplot(g[2,3]);panel(e,'e','Endpoint error tails · NFE 32')
 for k in range(3):vv=np.sort(errors[k,2]);e.step(vv,np.arange(1,n+1)/n,c=COL[k],lw=1.1,where='post')
 e.set(xscale='log',xlabel='Endpoint L2 error',ylabel='ECDF',ylim=(0,1.02));RAW.update(diffusion_centres=CENTRES,diffusion_initial=x0,diffusion_reference=ref,diffusion_budgets=budgets,diffusion_outputs=outputs,diffusion_errors=errors,diffusion_path=path,diffusion_sigmas=s,diffusion_mode_counts=count,diffusion_mode_residuals=residual);finish(f,out,'diffusion-numerics','COMPUTED TOY DIFFUSION · analytic 8-mode score · reference: 2,048-call Heun · no trained image model')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);theme();plt.rcParams.update({'font.size':7,'axes.labelsize':7,'axes.linewidth':.5,'xtick.labelsize':6,'ytick.labelsize':6});rng=np.random.default_rng(1107);retrieval(a.out,rng);conflict(a.out,rng);diffusion(a.out,rng);np.savez_compressed(a.out/'multimodal-diffusion-inputs.npz',**RAW);(a.out/'provenance.json').write_text(json.dumps({'seed':1107,'multimodal':'All embeddings and logits synthetic; no pretrained models evaluated','diffusion':'VE probability-flow ODE, analytic eight-mode Gaussian mixture score; finite sigma .01 endpoint; starts from exact marginal at sigma 3','diffusion_reference':'Heun, 2048 score calls; error is discretization against same-start reference, not image quality','bootstrap':'2000 pointwise percentile resamples of matched query/case identities','palette':['#4266A0','#328E89','#B9647C','#C69B4B']},indent=2));print(a.out)
if __name__=='__main__':main()
