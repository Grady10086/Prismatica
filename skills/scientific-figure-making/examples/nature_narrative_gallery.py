"""Evidence-led figures from a trained digits demo model; no invented outcomes."""
import argparse,json,sys
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from nature_data_gallery import load_colors
from nature_complex_gallery import heading
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature
from narrative_data import variant,corrupt


def save(fig,out,name):
    fig.text(.5,.025,'SCIKIT-LEARN DIGITS · real images, demo classifier · artificial variants labelled explicitly',ha='center',fontsize=5,color='#666666')
    fig.savefig(out/(name+'.svg'));fig.savefig(out/(name+'.png'),dpi=230);plt.close(fig)


def setup():
    d=load_digits();train,test=train_test_split(np.arange(len(d.target)),test_size=.30,stratify=d.target,random_state=1021);model=LogisticRegression(C=3,max_iter=2000,random_state=1021).fit(d.data[train]/16,d.target[train]);probs=model.predict_proba(d.data[test]/16);pred=probs.argmax(axis=1);pca=PCA(n_components=2,svd_solver='full').fit(d.data[train]/16);xy=pca.transform(d.data[test]/16)
    return d,train,test,model,probs,pred,pca,xy


def image_card(fig,rect,pixels,title,detail,col):
    ax=fig.add_axes(rect);ax.set_zorder(3);ax.imshow(pixels,cmap='gray_r',vmin=0,vmax=16,interpolation='nearest');ax.set(xticks=[],yticks=[])
    for sp in ax.spines.values():sp.set_visible(True);sp.set_color(col);sp.set_linewidth(.8)
    ax.set_title(title,fontsize=5.5,loc='left',pad=5);ax.text(.5,-.12,detail,transform=ax.transAxes,ha='center',va='top',fontsize=5)
    return ax


def failure(out,c,state):
    d,tr,te,model,prob,pred,pca,xy=state;y=d.target[te];wrong=pred!=y;conf=prob.max(axis=1);ids=np.where(wrong)[0];selected=ids[np.argsort(-conf[ids],kind='stable')[:6]]
    if len(selected)<6:raise ValueError('Demo requires six observed errors for the contact sheet')
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=145));heading(fig,'u','Failure atlas: from population to individual evidence',f'Real handwritten digits · held-out n={len(te)} · {wrong.sum()} errors · logistic classifier trained on {len(tr)} images')
    ax=fig.add_axes([.10,.34,.43,.47]);ax.scatter(*xy[~wrong].T,s=5,c='#B8BDC8',alpha=.4,lw=0);ax.scatter(*xy[wrong].T,s=15,c=c.style(1)['color'],alpha=.8,lw=0);ax.set(xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.0%} train variance)',ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.0%})');ax.set_title('All held-out images · errors in rose',loc='left',fontweight='bold',fontsize=6.5)
    for j,i in enumerate(selected):
        col=c.style(j%5)['color'];x=.66+(j%2)*.17;yt=.71-(j//2)*.19
        card=image_card(fig,[x,yt,.115,.115],d.images[te[i]],f'#{te[i]} · {y[i]} → {pred[i]}',f'Max score {conf[i]:.2f}',col);ax.scatter(*xy[i],s=25,facecolors='none',edgecolors=col,lw=.8,zorder=4)
        fig.add_artist(ConnectionPatch(xyA=xy[i],coordsA=ax.transData,xyB=(0,.5),coordsB=card.transAxes,color=col,alpha=.22,lw=.4,zorder=2.5))
    fig.text(.65,.885,'SIX HIGHEST-SCORE ERRORS',fontsize=6,fontweight='bold');fig.text(.65,.86,'Source ID · true label → prediction',fontsize=5,color='#555555')
    density=fig.add_axes([.10,.14,.43,.12])
    for mask,label,col in [(~wrong,'Correct',c.style(0)['color']),(wrong,'Error',c.style(1)['color'])]:
        v=np.sort(conf[mask]);density.step(v,np.arange(1,len(v)+1)/len(v),where='post',c=col,label=f'{label} · n={len(v)}',lw=.9)
    density.set(xlim=(0,1),ylim=(0,1),xlabel='Maximum predicted class score',ylabel='ECDF');density.legend(fontsize=5,loc='upper left')
    pairs=Counter(zip(y[wrong].tolist(),pred[wrong].tolist())).most_common(3)
    for j,((a,b),n) in enumerate(pairs):fig.text(.64+j*.11,.20,f'{a} → {b}',fontsize=12,color=c.style(1)['color'],ha='center');fig.text(.64+j*.11,.16,f'{n} case' + ('' if n==1 else 's'),fontsize=5.5,ha='center')
    fig.text(.58,.26,'MOST FREQUENT ERROR PAIRS',fontsize=5.5,fontweight='bold');fig.text(.10,.075,'PCA fitted on training pixels only · 2D proximity is not a discovered failure mechanism · examples selected after evaluation',fontsize=5)
    save(fig,out,'failure-atlas');return dict(error_test_row_ids=ids.tolist(),displayed_source_ids=te[selected].tolist(),error_pairs=[dict(true=a,predicted=b,n=n) for (a,b),n in pairs])


def branches(out,c,state):
    d,tr,te,model,prob,pred,pca,xy=state;eligible=np.where((d.target[te]==8)&(pred==8))[0];i=eligible[np.argmin(te[eligible])];source=int(te[i]);base=d.images[source];truth=int(d.target[source]);fig=plt.figure(figsize=nature.figure_size('double',height_mm=145));heading(fig,'v','One image, three controlled intervention families',f'Real source image #{source} · original label {truth} · all variants recomputed from the same original pixels')
    root=image_card(fig,[.08,.43,.20,.20],base,'Original input',f'Prediction {pred[i]} · P(original label)={prob[i,truth]:.2f}',c.style(0)['color']);rows=[('occlusion',[.4,1.],['Central mask 40%','Central mask 100%']),('contrast',[.65,.35],['Intensity ×0.65','Intensity ×0.35']),('shift',[1,2],['Shift right +1 px','Shift right +2 px'])];records=[]
    for k,(kind,levels,labels) in enumerate(rows):
        col=c.style(k+1)['color'];last=root
        for j,(level,label) in enumerate(zip(levels,labels)):
            pixels=variant(base,kind,level);p=model.predict_proba(pixels.reshape(1,-1)/16)[0];prediction=int(p.argmax());x=.44+j*.31;y=.70-k*.235
            card=image_card(fig,[x,y,.145,.145],pixels,label,f'Predict {prediction} · P({truth})={p[truth]:.2f}',col)
            fig.add_artist(ConnectionPatch(xyA=(1,.5),coordsA=last.transAxes,xyB=(0,.5),coordsB=card.transAxes,color=col,lw=1,arrowstyle='->',mutation_scale=7));last=card
            records.append(dict(kind=kind,amount=level,pixels=pixels.tolist(),predicted=prediction,probabilities=p.tolist()))
    fig.text(.08,.31,'Same model\nSame class-score scale\nNo retraining',fontsize=6,linespacing=1.7);fig.text(.08,.12,'Controlled sensitivity study: branch edges order severity, not temporal or causal transitions.',fontsize=5.5)
    fig.text(.08,.075,'Variants can change digit identity or become out of distribution · original-label probability is not a correctness guarantee',fontsize=5)
    save(fig,out,'input-branches');return dict(source_id=source,source_label=truth,original_pixels=base.tolist(),variants=records)


def boundary(out,c,state):
    d,tr,te,model,prob,pred,pca,xy=state;images=d.images[te];y=d.target[te];rng=np.random.default_rng(1022);noise=rng.normal(size=images.shape);sigmas=np.linspace(0,6,13);occlusions=np.linspace(0,1,11);accuracy=np.zeros((11,13));correct=np.zeros((11,13),int)
    for r,o in enumerate(occlusions):
        for j,s in enumerate(sigmas):
            changed=corrupt(images,noise,s,o);predicted=model.predict(changed.reshape(len(te),-1)/16);correct[r,j]=np.sum(predicted==y);accuracy[r,j]=correct[r,j]/len(te)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=150));heading(fig,'w','Capability landscape measured on a condition grid',f'{len(te)} held-out source images per cell · 13 noise levels × 11 mask strengths · one fixed trained classifier')
    ax=fig.add_axes([.05,.35,.61,.50],projection='3d');xx,yy=np.meshgrid(sigmas,occlusions);ax.plot_surface(xx,yy,accuracy,cmap=c.cmap('sequential'),vmin=0,vmax=1,linewidth=.25,edgecolor=(1,1,1,.35),alpha=.95,antialiased=True);ax.scatter(xx.ravel(),yy.ravel(),accuracy.ravel(),s=1.5,c='#444444',alpha=.5);ax.set(xlabel='Noise SD (pixel units)',ylabel='Mask strength',zlabel='Original-label accuracy',zlim=(0,1));ax.view_init(elev=28,azim=-55);ax.grid(False)
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:axis.set_pane_color((1,1,1,0))
    ax.tick_params(labelsize=5);ax.set_title('Observed grid values · connected surface',loc='left',fontsize=6.5,fontweight='bold',pad=12)
    source=int(min(te[np.where((d.target[te]==8)&(pred==8))[0]]));source_row=int(np.where(te==source)[0][0]);conditions=[(0,0),(6,5),(12,10)]
    fig.text(.72,.855,f'SOURCE #{source}, THREE CONDITIONS',fontsize=5.5,fontweight='bold')
    for k,(j,r) in enumerate(conditions):
        pixels=corrupt(images[source_row:source_row+1],noise[source_row:source_row+1],sigmas[j],occlusions[r])[0];p=model.predict_proba(pixels.reshape(1,-1)/16)[0]
        image_card(fig,[.76,.67-k*.17,.115,.115],pixels,f'σ={sigmas[j]:g} · mask={occlusions[r]:.1f}',f'Prediction {p.argmax()} · cell accuracy {accuracy[r,j]:.1%}',c.style(k)['color'])
    safe=fig.add_axes([.10,.14,.30,.15]);safe.contourf(xx,yy,accuracy>=.9,levels=[-.5,.5,1.5],colors=['#EEF0F5',c.style(0)['color']],alpha=.7);safe.scatter(xx,yy,s=1,c='#666666',alpha=.4);safe.contour(xx,yy,accuracy,levels=[.9],colors=['black'],linewidths=.7);safe.set(xlabel='Noise SD',ylabel='Mask strength',xlim=(0,6),ylim=(0,1));safe.set_title('90% criterion · interpolation between tested cells',loc='left',fontsize=5.5)
    curve=fig.add_axes([.51,.14,.38,.15]);
    for k,r in enumerate([0,5,10]):curve.plot(sigmas,accuracy[r],c=c.style(k)['color'],marker='o',ms=2,lw=.9,label=f'Mask {occlusions[r]:.1f}')
    curve.axhline(.9,c='#999999',ls=':',lw=.6);curve.set(xlabel='Noise SD (pixel units)',ylabel='Original-label accuracy',ylim=(0,1));curve.legend(fontsize=5,loc='lower left');curve.set_title('Three observed sections',loc='left',fontsize=6)
    fig.text(.10,.075,'Artificial corruption benchmark · shared noise draws across conditions · 90% is illustrative, not a validated safety boundary',fontsize=5)
    save(fig,out,'capability-landscape');return dict(noise_seed=1022,noise_sd=sigmas.tolist(),mask_strength=occlusions.tolist(),correct_counts=correct.tolist(),n_per_cell=len(te),accuracy=accuracy.tolist(),example_source_id=source)


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors);state=setup();d,tr,te,model,prob,pred,pca,xy=state
    result=dict(kind='REAL DIGITS / DEMO MODEL / ARTIFICIAL INPUT VARIANTS',sklearn_version=sklearn.__version__,test_pixels=d.images[te].tolist(),train_ids=tr.tolist(),test_ids=te.tolist(),true_labels=d.target[te].tolist(),predicted_labels=pred.tolist(),probabilities=prob.tolist(),pca_xy=xy.tolist(),model_coefficients=model.coef_.tolist(),model_intercept=model.intercept_.tolist(),failure=failure(a.out,c,state),branches=branches(a.out,c,state),boundary=boundary(a.out,c,state));(a.out/'evidence.json').write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
