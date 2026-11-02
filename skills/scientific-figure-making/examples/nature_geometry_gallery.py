"""Three original Nature-informed geometric compositions. Synthetic data only."""
import argparse,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,ConnectionPatch
from scipy.integrate import solve_ivp
import numpy as np
from nature_data_gallery import load_colors
from nature_complex_gallery import heading,finish
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import nature_profile as nature
from geometry_charts import ternary_xy,field,crop_mask


def triangle(ax):
    h=np.sqrt(3)/2;ax.plot([0,1,.5,0],[0,0,h,0],c='#555555',lw=.8)
    for v in [.2,.4,.6,.8]:
        for fixed in range(3):
            p=np.zeros((2,3));p[:,fixed]=v;others=[i for i in range(3) if i!=fixed];p[0,others[0]]=1-v;p[1,others[1]]=1-v;q=ternary_xy(p);ax.plot(*q.T,c='#DDDFE5',lw=.4,zorder=0)
    for x,y,label in [(0,-.045,'A = 100%'),(1,-.045,'B = 100%'),(.5,h+.045,'C = 100%')]:ax.text(x,y,label,ha='center',va='center',fontsize=6)
    ax.set(xlim=(-.12,1.12),ylim=(-.12,h+.12));ax.set_aspect('equal');ax.axis('off')


def ternary(out,c):
    rng=np.random.default_rng(821);groups=np.repeat(np.arange(3),35);a=np.vstack([rng.dirichlet(v,35) for v in [[7,2,3],[2,7,3],[3,3,7]]]);b=a*np.exp(rng.normal(np.log([.8,1.35,1.]),.08,(105,3)));b/=b.sum(axis=1,keepdims=True);pa,pb=ternary_xy(a),ternary_xy(b);cols=[c.style(k)['color'] for k in range(3)]
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=135));heading(fig,'o','Composition shifts on a common simplex','105 synthetic matched units · three predefined cohorts · A + B + C = 1 at both observations')
    g=fig.add_gridspec(2,3,left=.07,right=.94,bottom=.17,top=.82,width_ratios=[1,1,.95],height_ratios=[1,.75],wspace=.65,hspace=.7);ax=fig.add_subplot(g[:,:2]);triangle(ax)
    for k in range(3):
        m=groups==k;ax.scatter(*pb[m].T,s=9,c=cols[k],alpha=.7,lw=0,label=f'Cohort {k+1}')
        center=b[m].mean(axis=0);q=ternary_xy(center[None,:])[0];ax.scatter(*q,s=55,marker='D',c=cols[k],edgecolors='white',lw=.7,zorder=4)
    for i in np.r_[0:4,35:39,70:74]:
        ax.annotate('',xy=pb[i],xytext=pa[i],arrowprops=dict(arrowstyle='->',lw=.6,color='#666666'));ax.scatter(*pa[i],s=8,facecolors='white',edgecolors='#666666',lw=.4)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.02),ncol=3,fontsize=5);ax.set_title('Final compositions · diamonds are cohort means',loc='left',fontsize=7,fontweight='bold')
    ratio=fig.add_subplot(g[0,2]);old=np.log2(a[:,1]/a[:,0]);new=np.log2(b[:,1]/b[:,0]);ratio.scatter(old,new,c=[cols[k] for k in groups],s=7,alpha=.6,lw=0);lo=min(old.min(),new.min())-.2;hi=max(old.max(),new.max())+.2;ratio.plot([lo,hi],[lo,hi],c='#999999',ls=':',lw=.6);ratio.set(xlabel='Initial log2(B/A)',ylabel='Final log2(B/A)',xlim=(lo,hi),ylim=(lo,hi));ratio.set_title('Matched ratio change',loc='left',fontsize=6)
    delta=fig.add_subplot(g[1,2]);change=b-a
    for k in range(3):
        vals=np.sort(change[:,k]);delta.step(vals,np.arange(1,106)/105,where='post',c=cols[k],label='ABC'[k])
    delta.axvline(0,c='#AAAAAA',ls=':',lw=.6);delta.set(xlabel='Component change (fraction)',ylabel='Empirical CDF',ylim=(0,1));delta.legend(title='Component',fontsize=5,title_fontsize=5);delta.set_title('All units · component changes',loc='left',fontsize=6)
    fig.text(.08,.075,'Grid: 20 percentage points · arrows: first four matched units per cohort · all 105 final units shown',fontsize=5.5)
    finish(fig,out,'ternary-compositions');return dict(initial=a.tolist(),final=b.tolist(),cohort=groups.tolist(),displayed_arrow_ids=np.r_[0:4,35:39,70:74].astype(int).tolist())


def flow(out,c):
    x=np.linspace(0,2,121);y=np.linspace(0,1,71);xx,yy=np.meshgrid(x,y);u,v=field(xx,yy);speed=np.hypot(u,v);paths=[]
    def end(t,p):return 2-p[0]
    end.terminal=True;end.direction=-1
    for start_y in [.12,.3,.5,.7,.88]:
        sol=solve_ivp(lambda t,p:field(p[0],p[1]),(0,18),[.05,start_y],events=end,rtol=1e-8,atol=1e-10,max_step=.04);paths.append(sol)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=145));heading(fig,'p','A steady vector field from geometry to trajectories','Analytic synthetic incompressible field · position (mm) · velocity (mm/s) · no measured fluid data')
    g=fig.add_gridspec(2,3,left=.09,right=.93,bottom=.17,top=.83,height_ratios=[1.35,1],wspace=.65,hspace=.7);ax=fig.add_subplot(g[0,:]);im=ax.pcolormesh(x,y,speed,cmap=c.cmap('sequential'),vmin=0,vmax=.4,shading='auto',rasterized=True);ax.streamplot(x,y,u,v,color='#444444',density=1.2,linewidth=.45,arrowsize=.55);ax.set(xlim=(0,2),ylim=(0,1),xlabel='x (mm)',ylabel='y (mm)',aspect='equal');ax.set_title('Instantaneous speed and streamlines',loc='left',fontsize=7,fontweight='bold');fig.colorbar(im,ax=ax,pad=.025,fraction=.035,label='Speed (mm/s)',ticks=[0,.2,.4])
    sample=fig.add_axes([.09,.57,.23,.23]);qx,qy=np.meshgrid(np.linspace(.1,1.9,7),np.linspace(.1,.9,4));qu,qv=field(qx,qy);ar=sample.quiver(qx,qy,qu,qv,angles='xy',scale_units='xy',scale=1,color='#555555',width=.008);sample.quiverkey(ar,.5,1.1,.2,'0.2 mm/s',labelpos='N',fontproperties={'size':5});sample.set(xlim=(-.1,2.4),ylim=(-.1,1.2),aspect='equal',xticks=[],yticks=[]);sample.set_title('Sampled vectors · actual magnitude',loc='left',fontsize=5.5,pad=32)
    prof=fig.add_subplot(g[1,0]);positions=[.3,1.,1.7]
    for k,px in enumerate(positions):
        pu,pv=field(np.full_like(y,px),y);prof.plot(np.hypot(pu,pv),y,c=c.style(k)['color'],label=f'x = {px:g}')
    prof.set(xlabel='Speed (mm/s)',ylabel='y (mm)',ylim=(0,1));prof.legend(fontsize=5,title='Section (mm)',title_fontsize=5);prof.set_title('Three vertical sections',loc='left',fontsize=6)
    traj=fig.add_subplot(g[1,1]);temporal=fig.add_subplot(g[1,2])
    for k,sol in enumerate(paths):
        col=c.style(k)['color'];traj.plot(*sol.y,c=col,lw=.8);traj.scatter(*sol.y[:,0],s=9,c=col);pu,pv=field(*sol.y);temporal.plot(sol.t,np.hypot(pu,pv),c=col,lw=.8)
    traj.set(xlim=(0,2),ylim=(0,1),xlabel='x (mm)',ylabel='y (mm)');traj.set_title('Five integrated pathlines · dot = start',loc='left',fontsize=5.5);temporal.set(xlabel='Elapsed time (s)',ylabel='Speed (mm/s)',xlim=(0,18));temporal.set_title('Speed along the same paths',loc='left',fontsize=6)
    fig.text(.09,.075,'Streamlines and pathlines coincide here because the field is steady · integration stops at outlet or 18 s',fontsize=5.5)
    finish(fig,out,'flow-field');return dict(x_mm=x.tolist(),y_mm=y.tolist(),u_mm_s=u.tolist(),v_mm_s=v.tolist(),pathlines=[dict(time_s=s.t.tolist(),xy_mm=s.y.T.tolist(),outlet_reached=bool(len(s.t_events[0]))) for s in paths])


def multiscale(out,c):
    rng=np.random.default_rng(822);centers=rng.uniform(0,200,(120,2));ids=np.repeat(np.arange(120),35);xy=centers[ids]+rng.normal(0,1.5,(4200,2));xy=xy.clip(0,200);classes=np.repeat(rng.integers(0,3,120),35);signal=np.exp(-np.sum((xy-[100,100])**2,axis=1)/1600)+rng.normal(0,.04,len(xy));roi=[65,135,65,135];local=[90,110,90,110];m=crop_mask(xy,roi);fine=crop_mask(xy,local)
    # Guarantee nested examples contain observations by deriving windows around a recorded cluster.
    center=centers[np.argmin(np.linalg.norm(centers-[100,100],axis=1))];local=[center[0]-8,center[0]+8,center[1]-8,center[1]+8];fine=crop_mask(xy,local)
    fig=plt.figure(figsize=nature.figure_size('double',height_mm=145));heading(fig,'q','Spatial evidence at three nested scales','4,200 synthetic localizations · one coordinate system · identical observation IDs across zoom levels')
    g=fig.add_gridspec(2,3,left=.07,right=.94,bottom=.17,top=.83,width_ratios=[1.25,.9,.9],height_ratios=[1,.8],wspace=.65,hspace=.7);full=fig.add_subplot(g[:,0]);mid=fig.add_subplot(g[0,1:]);detail=fig.add_subplot(g[1,1]);profile=fig.add_subplot(g[1,2]);cols=[c.style(k)['color'] for k in range(3)]
    for ax,mask,bounds,length,title in [(full,np.ones(len(xy),bool),[0,200,0,200],50,'Full field · 200 × 200 μm'),(mid,m,roi,20,'Region · 70 × 70 μm'),(detail,fine,local,5,'Local neighborhood · 16 × 16 μm')]:
        ax.scatter(*xy[mask].T,s=2 if ax==full else 5,c=[cols[k] for k in classes[mask]],lw=0,alpha=.65);ax.set(xlim=bounds[:2],ylim=bounds[2:],aspect='equal',xticks=[],yticks=[]);ax.set_title(title,loc='left',fontsize=5.5,fontweight='bold');margin=(bounds[1]-bounds[0])*.07;px=bounds[0]+margin;py=bounds[2]+margin;ax.plot([px,px+length],[py,py],c='black',lw=1.3);ax.text(px+length/2,py+margin/2,f'{length} μm',fontsize=5,ha='center',va='bottom')
    for ax,bounds in [(full,roi),(mid,local)]:ax.add_patch(Rectangle((bounds[0],bounds[2]),bounds[1]-bounds[0],bounds[3]-bounds[2],fill=False,edgecolor='black',lw=.7))
    for source,bounds,target,targetbounds in [(full,roi,mid,roi),(mid,local,detail,local)]:fig.add_artist(ConnectionPatch(xyA=(bounds[1],bounds[3]),coordsA=source.transData,xyB=(targetbounds[0],targetbounds[3]),coordsB=target.transData,color='#888888',ls=':',lw=.5))
    distances=np.linalg.norm(xy[fine]-center,axis=1)
    for k,col in enumerate(cols):
        v=np.sort(distances[classes[fine]==k])
        if len(v):profile.step(v,np.arange(1,len(v)+1)/len(v),where='post',c=col,label=f'C{k+1}, n={len(v)}')
    profile.set(xlabel='Distance to selected centre (μm)',ylabel='Empirical CDF',ylim=(0,1));profile.set_title('Same local observations',loc='left',fontsize=6);profile.legend(fontsize=5)
    handles=[full.scatter([],[],s=10,c=col,lw=0) for col in cols];fig.legend(handles,['Category 1','Category 2','Category 3'],loc='lower left',bbox_to_anchor=(.07,.12),ncol=3,fontsize=5)
    fig.text(.07,.105,f'Shared categorical colors · field n={len(xy)} → region n={m.sum()} → local n={fine.sum()} · no change in coordinate scale units',fontsize=5.5)
    fig.text(.07,.075,'Localizations are clustered observations, not independent biological replicates · no super-resolution claim',fontsize=5)
    finish(fig,out,'multiscale-spatial');return dict(xy_um=xy.tolist(),cluster_id=ids.tolist(),category=classes.tolist(),region_bounds_um=roi,local_bounds_um=local,local_center_um=center.tolist(),region_ids=np.where(m)[0].tolist(),local_ids=np.where(fine)[0].tolist())


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nature.apply(font_size=6);c=load_colors(a.out,a.colors);d=dict(kind='SYNTHETIC DEMONSTRATION',seeds=[821,822],ternary=ternary(a.out,c),flow=flow(a.out,c),spatial=multiscale(a.out,c));(a.out/'data-and-summaries.json').write_text(json.dumps(d,indent=2));print(a.out)
if __name__=='__main__':main()
