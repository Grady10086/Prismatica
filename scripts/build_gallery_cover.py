"""Build a vector README cover from the original synthetic gallery SVGs."""
from pathlib import Path
import argparse
import xml.etree.ElementTree as E
import resvg_py
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg';E.register_namespace('',NS)
def tag(x):return '{'+NS+'}'+x

def subsvg(parent,path,viewbox,x,y,w,h,prefix):
    original=E.parse(path).getroot();ids={e.get('id'):prefix+'-'+e.get('id') for e in original.iter() if e.get('id')}
    for e in original.iter():
        for key,value in list(e.attrib.items()):
            if key=='id':e.set(key,ids[value]);continue
            for old,new in ids.items():
                value=value.replace('url(#'+old+')','url(#'+new+')')
                if value=='#'+old:value='#'+new
            e.set(key,value)
    child=E.SubElement(parent,tag('svg'),{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'viewBox':viewbox or original.get('viewBox'),'preserveAspectRatio':'xMidYMid meet','overflow':'hidden'})
    if viewbox:
        values=viewbox.split();defs=E.SubElement(child,tag('defs'));cp=E.SubElement(defs,tag('clipPath'),{'id':prefix+'-source-crop','clipPathUnits':'userSpaceOnUse'});E.SubElement(cp,tag('rect'),dict(zip(['x','y','width','height'],values)));content=E.SubElement(child,tag('g'),{'clip-path':'url(#'+prefix+'-source-crop)'})
    else:content=child
    for e in original:content.append(e)

def text(parent,x,y,s,size,color,weight='400'):
    el=E.SubElement(parent,tag('text'),{'x':str(x),'y':str(y),'font-family':'DejaVu Sans, sans-serif','font-size':str(size),'font-weight':weight,'fill':color});el.text=s

def build(gallery,out):
    out.mkdir(parents=True,exist_ok=True)
    for dark in [False,True]:
        suffix='-dark' if dark else '';ink='#F3F4F6' if dark else '#333F49';muted='#A5B0C0' if dark else '#75818D'
        root=E.Element(tag('svg'),{'width':'1200','height':'760','viewBox':'0 0 1200 760','role':'img','aria-label':'Prismatica synthetic gallery preview'})
        E.SubElement(root,tag('title')).text='Prismatica — original visualization studies'
        E.SubElement(root,tag('rect'),{'width':'1200','height':'760','fill':'#18212B' if dark else '#F7F6F2'})
        subsvg(root,ROOT/'docs/brand'/('horizontal-dark.svg' if dark else 'horizontal.svg'),None,42,28,530,127,'brand')
        text(root,64,172,'Plots, palettes, publication layouts.',19,ink)
        text(root,64,200,'One coordinated workflow for scientific visualization.',13,muted)
        text(root,910,78,'VISUAL STUDIES',12,muted,'600');text(root,910,103,'Original · reproducible',12,muted)
        cards=[(52,238,466,438),(542,238,606,214),(542,474,606,202)]
        for x,y,w,h in cards:E.SubElement(root,tag('rect'),{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'rx':'17','fill':'#FFFFFF','stroke':'#D9DEE5','stroke-width':'.8'})
        text(root,75,270,'01  /  MULTI-TRACK ATLAS',11,'#55609B','600');text(root,564,269,'02  /  REPRESENTATION LANDSCAPE',11,'#55609B','600');text(root,564,503,'03  /  MATCHED EVALUATION FLOWS',11,'#55609B','600')
        subsvg(root,gallery/'circular-fingerprint.svg','25 45 390 315',68,285,430,355,'atlas')
        subsvg(root,gallery/'representation-landscape.svg','47 68 378 277',560,280,330,164,'representation')
        text(root,906,323,'Shared projection',13,'#333F49','600');text(root,906,346,'Paired vectors',11,'#75818B');text(root,906,365,'Density + dispersion',11,'#75818B')
        subsvg(root,gallery/'evaluation-flow.svg','38 60 460 300',560,512,335,153,'flow')
        text(root,906,553,'Conserved counts',13,'#333F49','600');text(root,906,576,'Visible regressions',11,'#75818B');text(root,906,595,'Paired uncertainty',11,'#75818B')
        text(root,64,714,'Synthetic illustration data · cropped detail previews · full figures and definitions in the gallery',11,muted)
        raw=E.tostring(root,encoding='unicode');(out/('cover'+suffix+'.svg')).write_text(raw+'\n');(out/('cover'+suffix+'.png')).write_bytes(resvg_py.svg_to_bytes(svg_string=raw,width=1800))
    print(out)

def main():
    p=argparse.ArgumentParser();p.add_argument('--gallery',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.gallery,a.out)
if __name__=='__main__':main()
