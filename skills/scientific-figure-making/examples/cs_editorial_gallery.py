"""CS image-led editorial compositions from explicit credited local source manifests.
Prepare assets with prepare_sequence_references.py; this script never downloads them.
"""
import argparse,json,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
from matplotlib.lines import Line2D

def text(fig,x,y,s,size=7,color='#222222',serif=False,**kwargs):
    return fig.text(x,y,s,fontsize=size,color=color,fontfamily='DejaVu Serif' if serif else 'DejaVu Sans',**kwargs)

def line(fig,xy,color='#DDD8D0',lw=.6):
    fig.add_artist(Line2D(*xy,transform=fig.transFigure,color=color,lw=lw))


class Assets:
    def __init__(self,root,manifest):
        self.root=Path(root);self.m=json.loads((self.root/manifest).read_text());self.used=[]
    def get(self,ref):
        spec=self.m['assets'][ref['asset']];path=(self.root/spec['file']).resolve()
        if not path.is_relative_to(self.root.resolve()):raise ValueError('Asset must be inside supplied source directory')
        a=plt.imread(path);h,w=a.shape[:2]
        if [w,h]!=spec['size']:raise ValueError('Source dimensions differ from manifest')
        record=dict(asset=ref['asset'],file=spec['file'],source=spec,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        if 'crop' in ref:
            x,y,cw,ch=ref['crop'];x,y,cw,ch=map(int,[x,y,cw,ch])
            if not (x>=0 and y>=0 and cw>0 and ch>0 and x+cw<=w and y+ch<=h):raise ValueError('Invalid source crop')
            a=a[y:y+ch,x:x+cw];record['crop_xywh']=[x,y,cw,ch]
        self.used.append(record);return a


def image(fig,x,y,w,a):
    h=w*fig.get_figwidth()/fig.get_figheight()*a.shape[0]/a.shape[1];ax=fig.add_axes([x,y,w,h]);ax.imshow(a,interpolation='nearest');ax.axis('off');return ax,h


def page(number,category,title,subtitle,dark=False):
    bg='#0C121C' if dark else '#FAF7F1';ink='#F4EFE8' if dark else '#252522';muted='#A0ADBE' if dark else '#7B7972';accent='#C2B7F4' if dark else '#546A62'
    fig=plt.figure(figsize=(10.6,7.7),facecolor=bg);text(fig,.055,.945,f'{number}   /   {category}',7,color=accent);text(fig,.055,.862,title,28,serif=True,color=ink);text(fig,.058,.817,subtitle,8,color=muted);line(fig,([.055,.945],[.790,.790]),color='#283346' if dark else '#DCD9D1')
    return fig,ink,muted,accent


def save(fig,out,name,credit):
    line(fig,([.055,.945],[.065,.065]),color='#788191',lw=.4);text(fig,.055,.025,credit,5,color='#88919B');fig.savefig(out/(name+'.svg'),facecolor=fig.get_facecolor());fig.savefig(out/(name+'.png'),dpi=240,facecolor=fig.get_facecolor());plt.close(fig)


def video(out,root):
    src=Assets(root,'video-cinema.json');m=src.m;frames=[src.get(r) for r in m['frames']];still=src.get(m['input']);detail=src.get(m['detail']);fig,ink,muted,accent=page('08','VIDEO GENERATION','Motion, from one image.','DynamiCrafter · published image-to-video example · original sample order',dark=True)
    main,h=image(fig,.055,.307,.61,frames[-1]);text(fig,.063,.765,'PUBLISHED OUTPUT   /   SAMPLE 04',6,color='#292211')
    ax,h=image(fig,.725,.576,.22,still);text(fig,.725,.761,'INPUT STILL',6,color=accent)
    ax,h=image(fig,.725,.337,.22,detail);text(fig,.725,.510,'DETAIL   /   SAME OUTPUT SAMPLE',5.7,color=accent)
    for i,a in enumerate(frames):
        x=.055+i*.229;image(fig,x,.105,.202,a);text(fig,x,.274,f'{i+1:02}',8,serif=True,color=accent)
    text(fig,.055,.080,'Four published samples · no generated in-between frames · elapsed time not assigned',5.5,color=muted)
    save(fig,out,'cs-video-cinema','REFERENCE LAYOUT STUDY · DynamiCrafter / Xing et al. · ECCV 2024, Fig. 4 · author results, no new model inference')
    return dict(source_manifest='video-cinema.json',source_url=m['source_url'],assets=src.used,frame_order=[r['asset'] for r in m['frames']])


def object3d(out,root):
    src=Assets(root,'object-stage.json');m=src.m;input_image=src.get(m['input']);mesh=src.get(m['geometry']);textured=src.get(m['hero']);normals=[src.get(r) for r in m['normals']];gallery=[src.get(r) for r in m['gallery']];fig,ink,muted,accent=page('09','SINGLE-IMAGE 3D','From pixels to surfaces.','Wonder3D · one object across input, generated normals and reconstructed meshes')
    # Original alpha channels remain intact; no cutout or new render is generated.
    ax,h=image(fig,.305,.26,.38,mesh);text(fig,.338,.765,'RECONSTRUCTED MESH',6,color=accent)
    ia,h=image(fig,.055,.465,.17,input_image);text(fig,.055,.723,'INPUT IMAGE',6,color=accent)
    ta,h=image(fig,.765,.47,.17,textured);text(fig,.765,.723,'TEXTURED MESH',6,color=accent)
    for k,a in enumerate(normals):image(fig,.765+k*.097,.29,.085,a)
    text(fig,.765,.425,'GENERATED NORMAL VIEWS',5.6,color=accent)
    line(fig,([.235,.30],[.55,.55]),color='#B6B4AA');line(fig,([.69,.752],[.55,.55]),color='#B6B4AA')
    text(fig,.055,.218,'MORE PUBLISHED OBJECTS',6,color=accent)
    for i,(a,label) in enumerate(zip(gallery,['Lion','Chair','Burger','Rock'])):
        x=.31+i*.16;image(fig,x,.082,.105,a);text(fig,x,.078,label,5.5,color=muted)
    text(fig,.055,.165,'Same paper.\nSeparate examples.',6,color=muted,linespacing=1.6)
    save(fig,out,'cs-object-stage','REFERENCE LAYOUT STUDY · Wonder3D / Long et al. · CVPR 2024, Fig. 1 · original input / generated outputs; no new 3D inference')
    return dict(source_manifest='object-stage.json',source_url=m['source_url'],assets=src.used,gallery_labels=['Lion','Chair','Burger','Rock'])


def robot(out,root):
    src=Assets(root,'robot-diptych.json');m=src.m;tasks=m['tasks'];shirt=[src.get(r) for r in tasks[0]['frames']];microwave=[src.get(r) for r in tasks[1]['frames']];fig,ink,muted,accent=page('10','ROBOT MANIPULATION','Dexterity, in sequence.','π₀ · published robot observations · two tasks, one image-led composition',dark=True)
    image(fig,.055,.31,.46,shirt[2]);text(fig,.055,.772,tasks[0]['label'].upper(),6,color=accent)
    for k,i in enumerate([0,2,4]):
        image(fig,.775,.60-k*.16,.14,shirt[i]);text(fig,.775,.750-k*.16,f'PUBLISHED SAMPLE {i+1:02}',5.5,color=accent)
    text(fig,.055,.25,tasks[1]['label'].upper(),6,color=accent)
    for i,a in enumerate(microwave):
        x=.055+i*.18;image(fig,x,.105,.165,a);text(fig,x,.231,f'{i+1:02}',7,serif=True,color=accent)
    text(fig,.055,.080,'Original left-to-right sequence · no inferred timestamps, contact labels or task-success scores',5.3,color=muted)
    save(fig,out,'cs-robot-sequence','REFERENCE LAYOUT STUDY · Physical Intelligence / π₀ · original report, Figs. 6 & 10 · paper screenshots; no new robot experiment')
    return dict(source_manifest='robot-diptych.json',source_url=m['source_url'],assets=src.used,tasks=[t['label'] for t in tasks],hero_sample=3,detail_samples=[1,3,5])


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True,help='Directory prepared by prepare_sequence_references.py');p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'svg.fonttype':'none'})
    result=dict(kind='PUBLISHED CS REFERENCE COMPOSITION / NO NEW INFERENCE',video=video(a.out,a.source_dir),object3d=object3d(a.out,a.source_dir),robot=robot(a.out,a.source_dir));(a.out/'source-map.json').write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
