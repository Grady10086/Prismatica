"""Build restrained brand mastheads and vector-based editorial preview boards."""
from pathlib import Path
import argparse
import base64
import xml.etree.ElementTree as E
import resvg_py
from build_gallery_cover import tag,subsvg,text,ROOT

def root(w,h,label,bg):
 r=E.Element(tag('svg'),{'width':str(w),'height':str(h),'viewBox':f'0 0 {w} {h}','role':'img','aria-label':label})
 E.SubElement(r,tag('title')).text=label
 E.SubElement(r,tag('rect'),{'width':str(w),'height':str(h),'fill':bg})
 return r

def export(r,out,name):
 raw=E.tostring(r,encoding='unicode');(out/f'{name}.svg').write_text(raw+'\n');(out/f'{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=raw,width=1800))

def build(gallery,out):
 out.mkdir(parents=True,exist_ok=True)
 for dark in [False,True]:
  ink='#F3F4F6' if dark else '#333F49';muted='#A5B0C0' if dark else '#75818D';r=root(1200,310,'Prismatica — a complete scientific figure workflow','#18212B' if dark else '#F7F6F2')
  subsvg(r,ROOT/'docs/brand'/('horizontal-dark.svg' if dark else 'horizontal.svg'),None,40,26,510,119,'brand')
  text(r,60,182,'From research evidence to publication-ready figures.',23,ink)
  text(r,60,215,'Data plots · model analysis · method diagrams · research teasers',14,muted)
  for i,(label,col) in enumerate([('01  PLAN','#55609B'),('02  COMPOSE','#AB6690'),('03  REFINE','#E6A385'),('04  EXPORT',muted)]):
   x=60+i*285;E.SubElement(r,tag('rect'),{'x':str(x),'y':'261','width':'22','height':'3','fill':col});text(r,x+32,267,label,11,ink,'600')
  export(r,out,'masthead'+('-dark' if dark else ''))
 boards=[('experiments','01  /  EXPERIMENT DESIGN','Ablations, interactions and seed-level evidence.', [('cs-factorial-ablation.svg',40,100,1120,652)],800),('diagnostics','02  /  MODEL EVALUATION','Behavior analysis and performance–cost comparisons.', [('cs-model-analysis.svg',28,104,564,328),('cs-performance-audit.svg',608,104,564,328)],475),('compositions','03  /  COMPLEX COMPOSITIONS','Multi-track profiles and matched evaluation flows.', [('circular-fingerprint.svg',28,104,564,326),('evaluation-flow.svg',608,104,564,326)],475)]
 for name,title,subtitle,items,h in boards:
  r=root(1200,h,title,'#F7F6F2');text(r,40,38,title,12,'#55609B','600');text(r,40,69,subtitle,19,'#333F49')
  for i,(file,x,y,w,hh) in enumerate(items):
   E.SubElement(r,tag('rect'),{'x':str(x-5),'y':str(y-6),'width':str(w+10),'height':str(hh+12),'rx':'10','fill':'white','stroke':'#DFE3E8'})
   data=base64.b64encode((gallery/Path(file).with_suffix('.png')).read_bytes()).decode('ascii')
   E.SubElement(r,tag('image'),{'x':str(x),'y':str(y),'width':str(w),'height':str(hh),'href':'data:image/png;base64,'+data})
  export(r,out,name)
 print(out)

def main():
 p=argparse.ArgumentParser();p.add_argument('--gallery',type=Path,default=ROOT/'docs/gallery');p.add_argument('--out',type=Path,default=ROOT/'docs/homepage');a=p.parse_args();build(a.gallery,a.out)
if __name__=='__main__':main()
