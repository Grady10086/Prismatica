"""Image-first teaser layouts driven by local assets and explicit provenance.

No downloads, generated measurements, placeholder drawings or image recoloring.
Each preset has a distinct composition: asymmetric edit atlas, visual case study,
or panoramic robot sequence. Original images are embedded unchanged; zooms are
SVG viewBox crops recorded in the manifest, not altered raster files.
"""
from __future__ import annotations

import argparse
import base64
from html import escape
import json
from pathlib import Path
import textwrap

INK='#202126';MUTED='#71747B';LINE='#DDE0E4';ACCENT='#332288'


class Board:
    def __init__(self,title,height=1000,reuse_images=False):
        self.reuse_images=reuse_images;self._raster_cache={}
        self.h=height;self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="183mm" '
          f'height="{183*height/1600:.4f}mm" viewBox="0 0 1600 {height}" role="img">'
          f'<title>{escape(title)}</title><rect width="1600" height="{height}" fill="white"/>'
          '<g font-family="Arial, Helvetica, sans-serif">']

    def text(self,x,y,text,size=20,color=INK,weight=400,anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
                          f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(text))}</text>')

    def para(self,x,y,text,width,size=20,color=INK,leading=1.4):
        lines=textwrap.wrap(text,width=max(8,int(width/(size*.53))),break_long_words=False)
        for i,line in enumerate(lines):self.text(x,y+i*size*leading,line,size,color)
        return y+len(lines)*size*leading

    def rect(self,x,y,w,h,fill='none',stroke='none',sw=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def rule(self,x1,y1,x2,y2,color=LINE,width=1):
        self.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')

    def image(self,item,x,y,w,h,crop=None,background='#F5F5F6'):
        path=item['path'];iw,ih=item['size']
        crop=crop or item.get('crop',[0,0,iw,ih])
        a,b,c,d=crop
        if min(c,d)<=0 or min(a,b)<0 or a+c>iw+.01 or b+d>ih+.01:
            raise ValueError(f'Crop outside image: {path}')
        key=(str(path.resolve()),iw,ih)
        resource=self._raster_cache.get(key) if self.reuse_images else None
        if resource is None:
            data=path.read_bytes()
            if data.startswith(b'\x89PNG'):mime='image/png'
            elif data.startswith(b'\xff\xd8'):mime='image/jpeg'
            elif data.startswith(b'RIFF') and data[8:12]==b'WEBP':mime='image/webp'
            else:raise ValueError(f'Unsupported raster image: {path}')
            payload=base64.b64encode(data).decode()
            if self.reuse_images:
                resource=f'raster-{len(self._raster_cache)}'
                self._raster_cache[key]=resource
                self.parts.append(f'<defs><image id="{resource}" width="{iw}" height="{ih}" href="data:{mime};base64,{payload}"/></defs>')
        self.rect(x,y,w,h,background)
        clip_id=f'crop-{len(self.parts)}'
        element=(f'<use href="#{resource}" clip-path="url(#{clip_id})"/>' if self.reuse_images else
                 f'<image width="{iw}" height="{ih}" clip-path="url(#{clip_id})" href="data:{mime};base64,{payload}"/>')
        self.parts.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" '
             f'viewBox="{a} {b} {c} {d}" preserveAspectRatio="xMidYMid meet" overflow="hidden">'
             f'<defs><clipPath id="{clip_id}" clipPathUnits="userSpaceOnUse"><rect x="{a}" y="{b}" width="{c}" height="{d}"/></clipPath></defs>'
             f'{element}</svg>')

    def finish(self,source,kind):
        self.rule(40,self.h-64,1560,self.h-64)
        self.text(40,self.h-33,source,16,MUTED)
        self.text(1560,self.h-33,kind,15,MUTED,anchor='end')
        return ''.join(self.parts)+'</g></svg>'


def editing(m):
    b=Board('Asymmetric image editing result atlas')
    a=m['assets'];b.text(40,50,m['eyebrow'],15,ACCENT,600)
    b.text(40,100,m['title'],38,weight=600)
    b.text(40,145,'INPUT',16,MUTED,600);b.text(455,145,'EDITED OUTPUT',16,MUTED,600)
    b.image(a['input'],40,170,365,365)
    b.image(a['output'],455,170,650,650)
    b.text(40,582,'EDIT INSTRUCTION',15,ACCENT,600)
    b.para(40,630,m['instruction'],340,31,INK,1.25)
    b.rule(40,739,390,739)
    b.para(40,780,m['note'],345,19,MUTED)
    b.text(1150,145,'MORE PUBLISHED PAIRS',16,MUTED,600)
    for i,pair in enumerate(m['pairs']):
        y=170+i*335
        height=250 if i==0 else 171
        b.image(a[pair['before']],1150,y,195,height)
        b.image(a[pair['after']],1365,y,195,height)
        b.text(1150,y+height+32,pair['label'],20,weight=500)
        b.text(1150,y+height+59,'Input',16,MUTED);b.text(1365,y+height+59,'Edited',16,MUTED)
    b.text(455,862,m['output_note'],19,MUTED)
    return b.finish(m['source_label'],m['kind'])


def case_study(m):
    b=Board('Visual evidence spread')
    a=m['assets'];b.text(40,50,m['eyebrow'],15,ACCENT,600)
    b.text(40,100,m['title'],38,weight=600)
    b.image(a['image'],40,165,920,616)
    iw,ih=a['image']['size'];crop=m['detail_crop'];cx,cy,cw,ch=crop
    # Normalized editorial crop coordinates; match the letterboxed image geometry.
    scale=min(920/iw,616/ih);ox=40+(920-iw*scale)/2;oy=165+(616-ih*scale)/2
    b.rect(ox+cx*scale,oy+cy*scale,cw*scale,ch*scale,'none','white',4)
    b.rect(ox+cx*scale,oy+cy*scale,cw*scale,ch*scale,'none',ACCENT,1.5)
    b.text(1010,150,'DETAIL FROM INPUT',15,ACCENT,600)
    b.image(a['image'],1010,165,240,360,crop)
    b.text(1285,192,'Published response',22,weight=600)
    b.para(1285,234,m['response_summary'],270,21)
    b.para(1285,419,'Paraphrased summary; not a new model run.',270,17,MUTED)
    b.text(1010,567,'Editorial crop, not a saliency map.',17,MUTED)
    b.text(40,829,m['question'],29,weight=500)
    b.para(40,872,m['note'],880,19,MUTED)
    b.text(1010,637,m['metric_label'],20,weight=500)
    for i,row in enumerate(m['results']):
        y=683+i*66
        b.text(1010,y,row['name'],18)
        b.rect(1160,y-15,270,13,'#F0F0F3')
        b.rect(1160,y-15,270*row['value']/100,13,ACCENT if i==0 else '#ACADB5')
        b.text(1550,y,f"{row['value']:.1f} ± {row['std']:.1f}",18,anchor='end')
    b.text(1010,888,'Published mean ± std.; relative score, not accuracy.',16,MUTED)
    return b.finish(m['source_label'],m['kind'])


def rollout(m):
    b=Board('Robot task narrative with continuous rollout ribbon',height=1120)
    a=m['assets'];b.text(40,50,m['eyebrow'],15,ACCENT,600)
    b.text(40,100,m['title'],38,weight=600)
    frames=m['frames']
    b.image(a['sequence'],40,150,820,560,frames[0]['crop'])
    b.text(900,172,'TASK',15,ACCENT,600)
    b.text(900,215,m['task'],31,weight=500)
    b.para(900,256,m['description'],630,20,MUTED)
    for i,frame in enumerate([frames[3],frames[4]]):
        x=900+i*335
        b.image(a['sequence'],x,365,300,280,frame['crop'])
        b.text(x,678,frame['label'],19,weight=500)
    b.text(40,754,'ORDERED FRAMES FROM THE PUBLISHED SEQUENCE',15,ACCENT,600)
    for i,frame in enumerate(frames):
        x=40+i*(1520/6)
        b.image(a['sequence'],x,785,1520/6-8,181,frame['crop'])
        b.text(x,999,f"{i+1:02d}  {frame['label']}",17,MUTED)
    return b.finish(m['source_label'],m['kind'])


LAYOUTS={'editing-atlas':editing,'visual-case':case_study,'robot-ribbon':rollout}


def main():
    global ACCENT
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--tokens',type=Path,help='Optional paper-colors JSON export for annotation accent')
    p.add_argument('--png',action='store_true',help='Preview with optional resvg-py')
    args=p.parse_args();m=json.loads(args.manifest.read_text())
    palette='synthetic default accent'
    if args.tokens:
        data=json.loads(args.tokens.read_text());color=data['hues']['ours']['anchor']
        if not isinstance(color,str) or len(color)!=7 or not color.startswith('#'):raise ValueError('Accent must be #RRGGBB')
        int(color[1:],16);ACCENT=color;palette=data['theme']
    if m.get('layout') not in LAYOUTS:raise ValueError('Unknown layout')
    if m.get('kind') not in {'PUBLISHED REFERENCE STUDY','PROJECT RESULTS'}:
        raise ValueError('Declare whether this is a published reference or project results')
    if not m.get('source_label') or not m.get('source_url'):
        raise ValueError('Source label and URL are required')
    for item in m['assets'].values():
        path=Path(item['file']).expanduser()
        if not path.is_absolute():path=args.manifest.resolve().parent/path
        if not path.is_file():raise ValueError(f'Missing local asset: {path}')
        item['path']=path
        if len(item['size'])!=2 or min(item['size'])<=0:raise ValueError('Supply valid image dimensions')
    if m['layout']=='visual-case':
        for row in m['results']:
            if not 0<=row['value']<=100 or row['std']<0:raise ValueError('Invalid relative score')
    svg=LAYOUTS[m['layout']](m)
    args.out.mkdir(parents=True,exist_ok=True)
    name=m['layout'];(args.out/f'{name}.svg').write_text(svg)
    if args.png:
        import resvg_py
        (args.out/f'{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg,width=2000,dpi=96))
    (args.out/f'{name}-provenance.json').write_text(json.dumps({
        'source_label':m['source_label'],'source_url':m['source_url'],'kind':m['kind'],
        'rights_note':m.get('rights_note','Retain asset-specific credit and reuse terms.'),
        'assets':{k:{f:v for f,v in a.items() if f!='path'} for k,a in m['assets'].items()},
        'transformations':'Repositioned original images; labelled SVG detail crops. No image-content edits.',
        'detail_crop':m.get('detail_crop'),'frames':m.get('frames',[]),
        'manifest':args.manifest.name,'annotation_palette':palette},indent=2)+'\n')
    print(f'Wrote {name} to {args.out}')


if __name__=='__main__':main()
