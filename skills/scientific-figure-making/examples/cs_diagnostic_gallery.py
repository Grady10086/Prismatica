"""Three image-led diagnostics from a locally trained tiny attention classifier."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

BG='#F9F6EF';INK='#263041';MUT='#7C8492';TEAL='#3C938C';ROSE='#CC776B';GOLD='#C5AA70'
def soft(x):
 e=np.exp(x-x.max(-1,keepdims=True));return e/e.sum(-1,keepdims=True)
def page(tag,title,sub,dark=False):
 bg='#101B2B' if dark else BG;ink='#F6F0E6' if dark else INK;f=plt.figure(figsize=(12,8),facecolor=bg);f.text(.055,.95,tag,fontsize=8,color=TEAL);f.text(.055,.875,title,fontsize=29,fontfamily='DejaVu Serif',color=ink);f.text(.055,.825,sub,fontsize=8,color='#A8B7C8' if dark else MUT);return f,ink
def txt(f,x,y,t,size=9,col=INK,**kw):f.text(x,y,t,fontsize=size,color=col,**kw)
def axis(f,r,dark=False):
 a=f.add_axes(r,facecolor='none');c='#A8B7C8' if dark else MUT;a.tick_params(colors=c,labelsize=7,length=2)
 for s in a.spines.values():s.set_color('#435063' if dark else '#D5D6D0')
 a.spines[['top','right']].set_visible(False);a.xaxis.label.set_color(c);a.yaxis.label.set_color(c);return a
def pic(f,r,img,weight=None):
 a=f.add_axes(r);a.imshow(img,cmap='gray',vmin=0,vmax=16,interpolation='nearest');a.axis('off')
 if weight is not None:a.imshow(np.repeat(np.repeat(weight.reshape(4,4),2,0),2,1),cmap='magma',vmin=0,vmax=1,alpha=.65,interpolation='nearest')
 return a
def save(f,out,name):
 f.text(.055,.027,'REAL DIGITS / LOCAL DEMO MODEL · held-out examples · attention is a model weight, not a causal explanation',fontsize=6,color=MUT);f.savefig(out/(name+'.png'),dpi=190);f.savefig(out/(name+'.svg'));plt.close(f)
def fit():
 d=load_digits();tr,te=train_test_split(np.arange(len(d.target)),test_size=.3,stratify=d.target,random_state=17);x=d.images.reshape(-1,4,2,4,2).transpose(0,1,3,2,4).reshape(-1,16,4)/16
 rng=np.random.default_rng(17);pos=rng.normal(0,.35,(16,16));W=rng.normal(0,.3,(4,16));q=rng.normal(0,.2,16);V=rng.normal(0,.15,(16,10));b=np.zeros(10);hist=[];snaps={};params=[];check=[0,10,40,120,300]
 def forward(xx):
  h=np.tanh(xx@W+pos);att=soft(h@q);z=(h*att[:,:,None]).sum(1);p=soft(z@V+b);return h,att,z,p
 for step in range(301):
  h,a,z,p=forward(x[tr]);yt=d.target[tr];loss=-np.log(p[np.arange(len(tr)),yt]+1e-12).mean();_,at,zt,pt=forward(x[te]);hist.append([step,loss,-np.log(pt[np.arange(len(te)),d.target[te]]+1e-12).mean(),(pt.argmax(1)==d.target[te]).mean()])
  if step in check:snaps[step]={'prob':pt.copy(),'attention':at.copy()};params.append(np.concatenate([W.ravel(),q,V.ravel(),b]))
  if step==300:break
  dp=p.copy();dp[np.arange(len(tr)),yt]-=1;dp/=len(tr);dz=dp@V.T;dv=z.T@dp;db=dp.sum(0);da=(dz[:,None,:]*h).sum(-1);ds=a*(da-(da*a).sum(1,keepdims=True));dh=a[:,:,None]*dz[:,None,:]+ds[:,:,None]*q;dq=np.einsum('nt,ntd->d',ds,h);du=dh*(1-h*h);dw=np.einsum('ntk,ntd->kd',x[tr],du)
  rate=.9;W-=rate*dw;q-=rate*dq;V-=rate*dv;b-=rate*db
 return d,tr,te,np.array(hist),snaps,np.array(params)
def training(out,state):
 d,tr,te,h,s,params=state;f,ink=page('04 / OPTIMIZATION OBSERVATORY','Learning leaves a trail.','Actual full-batch training · 301 evaluated checkpoints · one fixed train / held-out split',True)
 a=axis(f,[.07,.35,.46,.38],True);xy=PCA(n_components=2).fit_transform(params);a.plot(*xy.T,color=TEAL,lw=2)
 for k,step in enumerate(s):a.scatter(*xy[k],s=90,c=[GOLD],edgecolors='#101B2B',zorder=4);a.annotate(str(step),xy[k],xytext=([(-12,20),(14,-4),(14,-5),(8,8),(8,8)][k]),textcoords='offset points',color=ink,fontsize=9)
 a.set(xlabel='Parameter trajectory · PC1',ylabel='PC2');a.set_xticks([]);a.set_yticks([]);txt(f,.07,.765,'a  /  CHECKPOINT GEOMETRY',8,TEAL)
 a=axis(f,[.64,.43,.29,.29],True);a.plot(h[:,0],h[:,1],color=GOLD,label='Train');a.plot(h[:,0],h[:,2],color=ROSE,label='Held out');a.set(xlabel='Gradient step',ylabel='Cross-entropy');a.legend(frameon=False,labelcolor=ink,fontsize=8);txt(f,.64,.765,'b  /  LOSS WITHOUT SMOOTHING',8,TEAL)
 # One fixed held-out source is tracked at all checkpoints.
 row=0;txt(f,.07,.255,f'c  /  SAME INPUT THROUGH TRAINING · source #{te[row]} · true digit {d.target[te[row]]}',8,TEAL)
 for k,step in enumerate(s):
  p=s[step]['prob'][row];x=.07+k*.18;pic(f,[x,.09,.075,.11],d.images[te[row]]);txt(f,x+.082,.17,f'{step:03d}',12,ink);txt(f,x+.082,.137,f'pred {p.argmax()}',8,'#A8B7C8');txt(f,x+.082,.107,f'P={p.max():.2f}',7,'#A8B7C8')
 save(f,out,'cs-training-observatory')
def attention(out,state):
 d,tr,te,h,s,params=state;f,ink=page('05 / ATTENTION STUDIO','Where the model looks.','A trained, single-head attention-pooling classifier · 16 image patches · shared attention color limits')
 prob=s[300]['prob'];att=s[300]['attention'];idx=np.argmax(prob.max(1));im=d.images[te[idx]];a=att[idx]
 txt(f,.055,.76,'a  /  INPUT + PATCH ATTENTION',8,TEAL);pic(f,[.055,.32,.33,.43],im,a);txt(f,.055,.275,f'Source #{te[idx]} · true {d.target[te[idx]]} · predicted {prob[idx].argmax()}',9)
 txt(f,.46,.76,'b  /  TOP PATCHES → POOLED REPRESENTATION',8,TEAL)
 # Connections encode actual normalized attention weights; no language tokens invented.
 top=np.argsort(-a)[:5]
 for rank,j in enumerate(top):
  y=.65-rank*.082;patch=im[(j//4)*2:(j//4)*2+2,(j%4)*2:(j%4)*2+2];pic(f,[.46,y,.048,.065],patch);txt(f,.52,y+.022,f'p{j:02d}  {a[j]:.3f}',8)
  f.add_artist(ConnectionPatch((.61,y+.032),(.81,.50),coordsA=f.transFigure,coordsB=f.transFigure,color=TEAL,alpha=.6,lw=.7+8*a[j]))
 txt(f,.81,.51,'POOL',15,TEAL);txt(f,.81,.474,f'pred {prob[idx].argmax()}',9);txt(f,.81,.445,f'remaining mass {1-a[top].sum():.2f}',7,MUT)
 txt(f,.46,.19,'c  /  OTHER HELD-OUT INPUTS · SAME SCALE',8,TEAL)
 rows=[int(np.where(d.target[te]==v)[0][0]) for v in [1,3,5,8]]
 for k,row in enumerate(rows):pic(f,[.46+k*.12,.065,.085,.11],d.images[te[row]],att[row]);txt(f,.46+k*.12,.055,f'ID {te[row]}',6,MUT)
 cbax=f.add_axes([.06,.225,.31,.012]);cb=plt.colorbar(plt.cm.ScalarMappable(norm=matplotlib.colors.Normalize(0,1),cmap='magma'),cax=cbax,orientation='horizontal',ticks=[0,.5,1]);cb.ax.tick_params(labelsize=6,length=2);cb.outline.set_visible(False)
 txt(f,.055,.19,'Weights are not explanations.',15,INK,fontfamily='DejaVu Serif');txt(f,.055,.145,'Overlay range: 0–1 (magma).\nTop five patches shown; others remain in the pool.',8,MUT,linespacing=1.6)
 save(f,out,'cs-attention-studio');return int(te[idx])
def failures(out,state):
 d,tr,te,h,s,params=state;p=s[300]['prob'];pred=p.argmax(1);truth=d.target[te];wrong=np.flatnonzero(pred!=truth);selected=wrong[np.argsort(-p[wrong].max(1),kind='stable')[:4]];f,ink=page('06 / FAILURE CASEBOOK','Confident. And incorrect.','Highest-score held-out errors · selected after evaluation · controls are same-label training images')
 txt(f,.06,.73,f'{len(wrong):03d}',48,ROSE,fontfamily='DejaVu Serif');txt(f,.06,.68,f'errors / {len(te)} held-out inputs',9);txt(f,.06,.58,f'{(pred==truth).mean():.1%}',29,TEAL,fontfamily='DejaVu Serif');txt(f,.06,.54,'held-out accuracy',9)
 txt(f,.06,.41,'Selection rule',13,INK,fontfamily='DejaVu Serif');txt(f,.06,.34,'Four errors with the highest\nmaximum class probability.\nNo inferred failure mechanisms.',8,MUT,linespacing=1.8)
 records=[]
 for k,row in enumerate(selected):
  x=.35+(k%2)*.31;y=.47-(k//2)*.31;source=te[row];correct_train=tr[d.target[tr]==truth[row]];near=correct_train[np.argmin(((d.data[correct_train]-d.data[source])**2).sum(1))]
  txt(f,x,y+.235,f'{truth[row]} → {pred[row]}',22,ROSE,fontfamily='DejaVu Serif');txt(f,x+.12,y+.24,f'P(pred) {p[row].max():.2f}',8,MUT);pic(f,[x,y+.07,.11,.15],d.images[source]);pic(f,[x+.145,y+.07,.11,.15],d.images[near]);txt(f,x,y+.04,f'Error #{source}',7);txt(f,x+.145,y+.04,f'Train control #{near}',7);txt(f,x,y+.012,'Pixel-nearest same-label training example',6,MUT);records.append({'source_id':int(source),'true':int(truth[row]),'pred':int(pred[row]),'max_probability':float(p[row].max()),'control_source_id':int(near)})
 save(f,out,'cs-failure-casebook');return records

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'svg.fonttype':'none'});state=fit();training(a.out,state);source=attention(a.out,state);cases=failures(a.out,state);d,tr,te,h,s,params=state
 meta={'dataset':'sklearn load_digits','model':'tanh patch embedding + fixed random positional vectors + trainable single-query attention pooling + softmax classifier','seed':17,'train_ids':tr.tolist(),'held_out_ids':te.tolist(),'history_columns':['step','train_CE','heldout_CE','heldout_accuracy'],'history':h.tolist(),'checkpoint_predictions':{str(k):v['prob'].tolist() for k,v in s.items()},'final_attention':s[300]['attention'].tolist(),'attention_hero_source':source,'failure_cases':cases,'selection':'post hoc highest maximum probability errors; controls selected from training by raw pixel squared distance'};(a.out/'experiment-record.json').write_text(json.dumps(meta,indent=2));print(h[-1]);print(a.out)
if __name__=='__main__':main()
