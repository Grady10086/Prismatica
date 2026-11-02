"""Image-led editorial layouts for teasers/talks; not journal-format validation."""
import argparse,json,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,ConnectionPatch,Wedge
from matplotlib.lines import Line2D
import numpy as np
from skimage import data,color,measure
from nature_data_gallery import load_colors


def crop(a,b):
    x0,x1,y0,y1=map(int,b)
    if not (0<=x0<x1<=a.shape[1] and 0<=y0<y1<=a.shape[0]):raise ValueError('Crop must lie within original pixels')
    return a[y0:y1,x0:x1]


def photo(fig,rect,a):
    ax=fig.add_axes(rect);ax.imshow(a,interpolation='nearest');ax.axis('off');return ax


def text(fig,x,y,s,size=7,color='#222222',serif=False,**kwargs):
    return fig.text(x,y,s,fontsize=size,color=color,fontfamily='DejaVu Serif' if serif else 'DejaVu Sans',**kwargs)


def line(fig,xy,color='#DDD8D0',lw=.6):fig.add_artist(Line2D(*xy,transform=fig.transFigure,color=color,lw=lw))


def save(fig,out,name,credit):
    text(fig,.055,.028,credit,5,color='#888888');fig.savefig(out/(name+'.svg'),facecolor=fig.get_facecolor());fig.savefig(out/(name+'.png'),dpi=240,facecolor=fig.get_facecolor());plt.close(fig)


def microscopy(out,c):
    a=data.immunohistochemistry();accent=c.style(0)['color'];rose=c.style(1)['color'];fig=plt.figure(figsize=(10.6,7.7),facecolor='#FBF9F4')
    text(fig,.055,.944,'01   /   SPATIAL OBSERVATORY',7,color=accent);text(fig,.055,.862,'Patterns within.',29,serif=True);text(fig,.058,.816,'One field. Two windows. Every pixel retained.',8,color='#77716C');line(fig,([.055,.945],[.791,.791]))
    main=photo(fig,[.055,.15,.53,.61],a);bounds=[[60,188,70,198],[280,408,280,408]];colors=[accent,rose];patches=[]
    for i,(b,col) in enumerate(zip(bounds,colors)):
        main.add_patch(Rectangle((b[0],b[2]),b[1]-b[0],b[3]-b[2],fill=False,ec=col,lw=1.2));main.text(b[0]+5,b[2]-8,'AB'[i],color=col,fontsize=8,fontweight='bold');p=crop(a,b);patches.append(p)
        right=photo(fig,[.65+i*.155,.47,.14,.25],p);text(fig,.65+i*.155,.734,f'{"AB"[i]}   /   128 × 128 px',6,color=col)
        fig.add_artist(ConnectionPatch(xyA=(b[1],b[2]),coordsA=main.transData,xyB=(0,.5),coordsB=right.transAxes,color=col,alpha=.35,lw=.6,zorder=0))
    text(fig,.65,.412,'THE LOCAL COLOR SIGNATURE',7,color=accent);ax=fig.add_axes([.65,.21,.295,.17],facecolor='#FBF9F4')
    for i,(p,col) in enumerate(zip(patches,colors)):
        v=np.sort(color.rgb2gray(p).ravel());ax.step(v,np.arange(1,len(v)+1)/len(v),where='post',c=col,lw=1.3,label=f'Window {"AB"[i]}')
    ax.set(xlim=(0,1),ylim=(0,1),xlabel='Relative luminance',ylabel='Pixel ECDF');ax.legend(frameon=False,fontsize=5,loc='upper left');ax.tick_params(labelsize=5,length=2);ax.spines[['top','right']].set_visible(False);ax.xaxis.label.set_size(6);ax.yaxis.label.set_size(6)
    text(fig,.06,.112,'512²',19,serif=True,color=accent);text(fig,.15,.115,'original pixels',7,color='#77716C');text(fig,.36,.112,'2',19,serif=True,color=rose);text(fig,.39,.115,'matched regions',7,color='#77716C');line(fig,([.055,.945],[.074,.074]))
    save(fig,out,'ivory-microscopy','REAL SAMPLE IMAGE · CMMI / scikit-image immunohistochemistry · pixel units; no biological inference')
    return dict(source='immunohistochemistry',bounds=bounds,luminance_means=[float(color.rgb2gray(p).mean()) for p in patches])


def deepfield(out,c):
    a=data.hubble_deep_field();lum=color.rgb2gray(a);labels=measure.label(lum>.32);regions=[r for r in measure.regionprops(labels,intensity_image=lum) if r.area>=12];regions=sorted(regions,key=lambda r:-r.area);chosen=[]
    for r in regions:
        yy,xx=r.centroid
        if xx<45 or xx>a.shape[1]-45 or yy<45 or yy>a.shape[0]-45:continue
        if all(np.linalg.norm(np.array(r.centroid)-np.array(v.centroid))>90 for v in chosen):chosen.append(r)
        if len(chosen)==4:break
    if len(chosen)<4:raise ValueError('Need four separated candidate regions')
    fig=plt.figure(figsize=(10.6,7.7),facecolor='#080D19');white='#F2EEE8';muted='#9AA5BA';accent='#C8B8FF'
    text(fig,.055,.944,'02   /   IMAGE CONSTELLATIONS',7,color=accent);text(fig,.055,.864,'A field of possibilities.',27,color=white,serif=True);text(fig,.058,.817,'Full context, precise apertures, unaltered light.',8,color=muted);line(fig,([.055,.945],[.788,.788]),color='#253047')
    main=photo(fig,[.055,.15,.625,.60],a);saved=[]
    for i,r in enumerate(chosen):
        yy,xx=r.centroid;main.add_patch(Circle((xx,yy),30,fill=False,ec=accent,lw=.7));main.text(xx+34,yy,f'{i+1:02}',fontsize=6,color=white);x=.74+(i%2)*.115;y=.50-(i//2)*.245;b=[int(xx)-40,int(xx)+40,int(yy)-40,int(yy)+40];patch=crop(a,b);right=photo(fig,[x,y,.10,.16],patch)
        text(fig,x,y+.173,f'{i+1:02}   /   APERTURE',5.5,color=accent);text(fig,x,y-.016,f'{int(r.area)} bright pixels',5,color=muted)
        fig.add_artist(ConnectionPatch(xyA=(xx+30,yy),coordsA=main.transData,xyB=(0,.5),coordsB=right.transAxes,color=accent,alpha=.25,lw=.5,zorder=0));saved.append(dict(bounds=b,area=int(r.area),centroid_yx=[float(yy),float(xx)]))
    text(fig,.74,.726,'FOUR LOCAL VIEWS',6.5,color=white);text(fig,.74,.692,'80 × 80 px · shared RGB scale',5.5,color=muted)
    text(fig,.74,.164,f'{len(regions):,}',21,color=accent,serif=True);text(fig,.74,.13,'threshold components ≥12 px',5.5,color=muted);text(fig,.74,.10,'Candidate regions, not galaxy labels.',5.3,color=muted);line(fig,([.055,.945],[.074,.074]),color='#253047')
    save(fig,out,'midnight-deepfield','REAL IMAGE · NASA Hubble eXtreme Deep Field via scikit-image · luminance >0.32; illustrative image analysis')
    return dict(source='hubble_deep_field',threshold=.32,min_area=12,candidate_count=len(regions),selected=saved)


def retina(out,c):
    a=data.retina();h,w=a.shape[:2];center=np.array([(w-1)/2,(h-1)/2]);radius=.36*w;angles=np.linspace(0,2*np.pi,180,endpoint=False);xx=np.rint(center[0]+radius*np.cos(angles)).astype(int);yy=np.rint(center[1]-radius*np.sin(angles)).astype(int);signals=a[yy,xx];cols=[c.style(1)['color'],c.style(2)['color'],c.style(0)['color']]
    fig=plt.figure(figsize=(10.6,7.7),facecolor='#FBF7F0');text(fig,.055,.944,'03   /   ORBITAL EVIDENCE',7,color=cols[0]);text(fig,.055,.864,'The spatial fingerprint.',27,serif=True);text(fig,.058,.817,'A circular field, encircled by measured color.',8,color='#82766E');line(fig,([.055,.945],[.788,.788]),color='#DFD3C8')
    ax=fig.add_axes([.035,.13,.64,.62]);ax.imshow(a,extent=(-1,1,-1,1),interpolation='nearest');ax.set(xlim=(-1.32,1.32),ylim=(-1.32,1.32),aspect='equal');ax.images[0].set_clip_path(Circle((0,0),1,transform=ax.transData));ax.axis('off')
    for k in range(3):
        for j in range(len(angles)):
            # Ring opacity represents an observed byte-channel value, not a decorative synthetic signal.
            deg=np.rad2deg(angles[j]);ax.add_patch(Wedge((0,0),1.06+k*.065,deg,deg+1.7,width=.025,facecolor=cols[k],alpha=.12+.88*signals[j,k]/255,lw=0))
    ax.add_patch(Circle((0,0),1.015,fill=False,ec='#D8C8BC',lw=.5));bounds=[[320,540,620,840],[820,1040,350,570]]
    for k,(b,col) in enumerate(zip(bounds,cols)):
        # Align displayed Cartesian frame with original top-left raster coordinates.
        x0=2*b[0]/w-1;x1=2*b[1]/w-1;y0=1-2*b[2]/h;y1=1-2*b[3]/h;ax.add_patch(Rectangle((x0,y1),x1-x0,y0-y1,fill=False,ec=col,lw=.8))
        p=crop(a,b);right=photo(fig,[.73,.49-k*.25,.19,.19],p);text(fig,.73,.704-k*.25,f'WINDOW {"AB"[k]}   /   220 × 220 px',6,color=col)
    text(fig,.73,.163,'R / G / B',13,serif=True,color='#765B51');text(fig,.73,.128,'Ring opacity = sampled intensity',6,color='#82766E');text(fig,.73,.10,f'180 angles · radius {radius:.0f} px',5.5,color='#82766E')
    for k,col in enumerate(cols):text(fig,.12+k*.145,.105,['R channel','G channel','B channel'][k],6,color=col)
    text(fig,.11,.075,'Original RGB image. Rings use nearest-pixel samples on one fixed-radius circle; not vessel or disease scores.',5,color='#82766E')
    save(fig,out,'orbital-retina','REAL IMAGE · Mikael Häggström / CC0 via scikit-image retina · editorial visual study; no diagnostic inference')
    return dict(source='retina',bounds=bounds,sampling_center_xy=center.tolist(),radius_px=float(radius),angles_rad=angles.tolist(),sample_xy=np.c_[xx,yy].tolist(),rgb_samples=signals.tolist(),ring_alpha_formula='.12 + .88*channel/255')


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--colors',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'svg.fonttype':'none','axes.linewidth':.5,'xtick.major.width':.5,'ytick.major.width':.5});c=load_colors(a.out,a.colors)
    result=dict(kind='REAL SAMPLE IMAGES / EDITORIAL LAYOUT STUDIES',microscopy=microscopy(a.out,c),deepfield=deepfield(a.out,c),retina=retina(a.out,c))
    result['sources']={}
    for name in ['immunohistochemistry','hubble_deep_field','retina']:
        im=getattr(data,name)();result['sources'][name]=dict(shape=list(im.shape),sha256_pixels=hashlib.sha256(im.tobytes()).hexdigest())
    (a.out/'provenance-and-measurements.json').write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
