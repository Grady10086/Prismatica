"""Four image-led editorial studies from credited CC0 microscopy/time-series data."""
import argparse,json,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,ConnectionPatch,Circle
import numpy as np
from skimage import data
from editorial_image_gallery import text,line,save,crop


def scaled(a,limits):
    lo,hi=map(float,limits)
    if not np.isfinite([lo,hi]).all() or hi<=lo:raise ValueError('Finite increasing display limits required')
    return np.clip((np.asarray(a,float)-lo)/(hi-lo),0,1)


def composite(channels,limits,luts):
    a=np.asarray(channels)
    if a.ndim!=3 or a.shape[-1]!=len(limits) or len(luts)!=len(limits):raise ValueError('Channel-last image and one fixed limit/LUT per channel required')
    return np.clip(sum(scaled(a[...,k],limits[k])[...,None]*np.asarray(luts[k]) for k in range(a.shape[-1])),0,1)


def photo(fig,rect,a):
    ax=fig.add_axes(rect);ax.imshow(a,interpolation='nearest');ax.axis('off');return ax


def kidney(out,a):
    if a.ndim!=4 or a.shape[-1]!=3:raise ValueError('Kidney data must be ZYXC with three channels')
    luts=[[.44,.40,1],[.12,.9,.84],[1,.63,.32]];limits=[[0,float(np.quantile(a[...,k],.998))] for k in range(3)];mip=a.max(axis=0);rgb=composite(mip,limits,luts)
    fig=plt.figure(figsize=(10.6,7.7),facecolor='#080F1A');ink='#F4F0EB';muted='#9CA8BC';accent='#85DED0'
    text(fig,.055,.944,'04   /   FLUORESCENCE IN DEPTH',7,color=accent);text(fig,.055,.862,'Light in layers.',29,serif=True,color=ink);text(fig,.058,.817,'Sixteen recorded planes. Three shared channel scales.',8,color=muted);line(fig,([.055,.945],[.786,.786]),color='#243246')
    main=photo(fig,[.055,.16,.59,.59],rgb);bounds=[190,330,160,300];main.add_patch(Rectangle((bounds[0],bounds[2]),140,140,fill=False,ec=accent,lw=.8));main.text(195,150,'ROI',fontsize=6,color=accent)
    waves=[450,515,605]
    for k in range(3):
        channel=np.zeros_like(mip);channel[...,k]=mip[...,k];patch=composite(crop(channel,bounds),limits,luts);y=.59-k*.20;ax=photo(fig,[.755,y,.145,.145],patch);text(fig,.755,y+.16,f'{waves[k]} nm   /   CH {k+1}',6,color=luts[k]);fig.add_artist(ConnectionPatch(xyA=(330,230),coordsA=main.transData,xyB=(0,.5),coordsB=ax.transAxes,color=luts[k],alpha=.25,lw=.5,zorder=0))
    text(fig,.725,.774,'CHANNEL-RESOLVED ROI',6.5,color=ink);text(fig,.725,.09,'Maximum-intensity projection · false color',5.5,color=muted)
    # Voxel dimensions are provided by the dataset metadata.
    main.plot([30,30+100/1.24],[470,470],c='white',lw=1.4);main.text(30,455,'100 μm',color='white',fontsize=6)
    text(fig,.06,.11,'16',20,serif=True,color=accent);text(fig,.12,.113,'z planes',7,color=muted);text(fig,.30,.11,'3',20,serif=True,color='#B5A7FF');text(fig,.34,.113,'channels',7,color=muted);line(fig,([.055,.945],[.074,.074]),color='#243246')
    save(fig,out,'noir-fluorescence','REAL VOLUME · Genevieve Buckley / Monash Micro Imaging, 2018 · CC0 · fixed 0–99.8th-percentile limits per channel')
    return dict(source='kidney',mip_axis=0,limits=limits,luts=luts,crop=bounds,voxel_um=[1.25,1.24,1.24],projection='maximum')


def material(out,a):
    if a.ndim!=3 or len(a)<11:raise ValueError('At least 11 grayscale frames required')
    lim=[float(np.quantile(a,.005)),float(np.quantile(a,.995))];frames=[0,2,4,6,8,10];hero=5;bounds=[[70,198,90,218],[280,408,180,308]];fig=plt.figure(figsize=(10.6,7.7),facecolor='#F4F3F0');ink='#282B30';muted='#7E8085';accent='#536A8B'
    text(fig,.055,.944,'05   /   MATERIALS IN MOTION',7,color=accent);text(fig,.055,.862,'The shape of change.',29,serif=True);text(fig,.058,.817,'Synchrotron radiography. One continuous record.',8,color=muted);line(fig,([.055,.945],[.786,.786]),color='#D9DBDD')
    def render(v):
        f=scaled(v,lim);return np.repeat(f[...,None],3,axis=-1)
    main=photo(fig,[.055,.34,.59,.41],render(a[hero]));text(fig,.06,.752,'FRAME 05   /   FULL FIELD',6,color=accent)
    for k,b in enumerate(bounds):
        main.add_patch(Rectangle((b[0],b[2]),128,128,fill=False,ec='#A4B9D9',lw=.8));ax=photo(fig,[.725+k*.115,.43,.105,.20],render(crop(a[hero],b)));text(fig,.725+k*.115,.659,f'DETAIL {"AB"[k]}',5.5,color=accent);fig.add_artist(ConnectionPatch(xyA=(b[1],b[2]),coordsA=main.transData,xyB=(0,.5),coordsB=ax.transAxes,color=accent,alpha=.3,lw=.5,zorder=0))
    text(fig,.725,.365,'11',24,serif=True,color=accent);text(fig,.795,.367,'recorded frames',7,color=muted)
    for j,index in enumerate(frames):
        x=.055+j*.15;photo(fig,[x,.13,.135,.15],render(a[index]));text(fig,x,.297,f'{index:02}',8,serif=True,color=accent)
    line(fig,([.055,.94],[.106,.106]),color='#AAB3BF');text(fig,.055,.081,'Source order preserved · one global grayscale mapping · selected frame indices, not inferred timestamps',5.5,color=muted)
    save(fig,out,'silver-solidification','REAL X-RAY SEQUENCE · C. Gus Becker / CSM, UCSB / APS–ANL, 2019 · CC0 · display limits shared across all frames')
    return dict(source='nickel_solidification',display_limits=lim,hero_frame=hero,filmstrip_indices=frames,crops=bounds)


def transport(out,a):
    if a.ndim!=4 or a.shape[1]!=2 or len(a)<15:raise ValueError('Protein sequence must be TCYX with two channels and 15 frames')
    limits=[[0,float(np.quantile(a[:,k],.998))] for k in range(2)];luts=[[.35,.70,1],[1,.64,.35]];indices=[0,7,14];fig=plt.figure(figsize=(10.6,7.7),facecolor='#0C1119');ink='#F3EEE7';muted='#9BA6B6';accent='#9DC9F4'
    text(fig,.055,.944,'06   /   A RECORDED TRANSITION',7,color=accent);text(fig,.055,.862,'Time, made visible.',29,serif=True,color=ink);text(fig,.058,.817,'Two measured channels. Fifteen original frames.',8,color=muted);line(fig,([.055,.945],[.786,.786]),color='#273041')
    means=[]
    for j,index in enumerate(indices):
        x=.055+j*.31;y=.40-j*.075;raw=np.moveaxis(a[index],0,-1);rgb=composite(raw,limits,luts);photo(fig,[x,y,.27,.33],rgb);text(fig,x,y+.345,f'FRAME {index:02}',7,color=accent);text(fig,x+.245,y+.345,f'{j+1:02}',9,serif=True,color='#D5A270',ha='right')
    text(fig,.055,.316,'CHANNEL 1',6,color=luts[0]);text(fig,.055,.29,'CHANNEL 2',6,color=luts[1]);text(fig,.055,.25,'Shared limits across time.\nNo generated intermediate frames.',6,color=muted,linespacing=1.6)
    # An unobtrusive index axis conveys ordering without invented physical time.
    line(fig,([.07,.92],[.16,.16]),color='#485568')
    for x,index in zip([.07,.495,.92],indices):line(fig,([x,x],[.154,.166]),color=accent,lw=1);text(fig,x,.123,f'{index:02}',8,color=accent,serif=True,ha='center')
    text(fig,.495,.085,'FRAME INDEX  /  temporal sampling interval not assigned',5.5,color=muted,ha='center')
    save(fig,out,'kinetic-protein','REAL LIVE-CELL SEQUENCE · Andrea Boni & Jan Ellenberg / EMBL · CC0 · fixed per-channel LUTs; no motion interpolation')
    return dict(source='protein_transport',display_limits=limits,luts=luts,frame_indices=indices,channel_means=a.mean(axis=(2,3)).tolist())



def botanical(out,a):
    if a.ndim!=3 or a.shape[-1]!=4:raise ValueError('Four-channel plant cross-section required')
    luts=[[.28,.55,1],[.95,.30,.68],[.14,.9,.76],[1,.66,.27]];limits=[[0,float(np.quantile(a[...,k],.998))] for k in range(4)];rgb=composite(a,limits,luts);candidates=[]
    for y in range(80,762,140):
        for x in range(80,762,140):
            b=[x,x+160,y,y+160];candidates.append((float(crop(rgb,b).mean()),b))
    selected=[]
    for score,b in sorted(candidates,reverse=True):
        if all(np.linalg.norm(np.array([b[0],b[2]])-np.array([v[0],v[2]]))>200 for v in selected):selected.append(b)
        if len(selected)==3:break
    fig=plt.figure(figsize=(10.6,7.7),facecolor='#F8F5EE');accent='#476F69';muted='#817D74'
    text(fig,.055,.944,'07   /   BOTANICAL MICROSCOPY',7,color=accent);text(fig,.055,.862,'The architecture of tissue.',27,serif=True);text(fig,.058,.817,'A four-channel field, read from whole to detail.',8,color=muted);line(fig,([.055,.945],[.786,.786]),color='#D8D9CE')
    main=photo(fig,[.045,.16,.60,.59],rgb)
    for k,b in enumerate(selected):
        main.add_patch(Rectangle((b[0],b[2]),160,160,fill=False,ec='#E5D8B5',lw=.7));main.text(b[0]+5,b[2]-10,str(k+1),color='white',fontsize=6);y=.59-k*.19;ax=photo(fig,[.755,y,.145,.145],crop(rgb,b));text(fig,.755,y+.16,f'REGION {k+1}   /   160 px',6,color=accent);fig.add_artist(ConnectionPatch(xyA=(b[1],b[2]+80),coordsA=main.transData,xyB=(0,.5),coordsB=ax.transAxes,color=accent,alpha=.3,lw=.5,zorder=0))
    text(fig,.725,.774,'THREE BRIGHT REGIONS',6.5,color=accent);main.plot([40,40+200/1.24],[860,860],c='white',lw=1.4);main.text(40,840,'200 μm',color='white',fontsize=6)
    text(fig,.06,.11,'4',20,serif=True,color=accent);text(fig,.095,.113,'recorded channels',7,color=muted);text(fig,.31,.11,'922²',20,serif=True,color='#9A6F83');text(fig,.42,.113,'source pixels',7,color=muted);text(fig,.725,.10,'Fixed channel LUTs · 0–99.8% limits',5.5,color=muted);line(fig,([.055,.945],[.074,.074]),color='#D8D9CE')
    save(fig,out,'botanical-architecture','REAL PLANT STEM · Genevieve Buckley / Monash Micro Imaging, 2018 · CC0 · false-color composite; exact source crops')
    return dict(source='lily',limits=limits,luts=luts,crops=selected,pixel_um=1.24,selection='largest mean display intensity, 160px tiles, separated >200px')


def main():
    p=argparse.ArgumentParser();p.add_argument('--demo',required=True,action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--asset-dir',type=Path);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'svg.fonttype':'none'})
    samples={}
    for name in ['kidney','nickel_solidification','protein_transport','lily']:
        local=args.asset_dir/(name+'.npy') if args.asset_dir else None;samples[name]=np.load(local,allow_pickle=False) if local and local.exists() else getattr(data,name)()
    result=dict(kind='REAL CC0 SAMPLE DATA / EDITORIAL DISPLAY STUDIES',sources={n:dict(shape=list(v.shape),dtype=str(v.dtype),sha256_pixels=hashlib.sha256(v.tobytes()).hexdigest()) for n,v in samples.items()},fluorescence=kidney(args.out,samples['kidney']),material=material(args.out,samples['nickel_solidification']),transport=transport(args.out,samples['protein_transport']),botanical=botanical(args.out,samples['lily']))
    (args.out/'provenance-and-display.json').write_text(json.dumps(result,indent=2));print(args.out)
if __name__=='__main__':main()
