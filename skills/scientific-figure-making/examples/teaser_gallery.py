"""Original vector teaser studies: scene overview, retrieval mechanism and evidence.

All geometry, curves and values are synthetic. No paper artwork or color-book data
is embedded. Optional --tokens consumes a paper-colors JSON export. PNG rendering
uses resvg-py only when --png is requested; SVG generation is standard-library only.
"""
from __future__ import annotations

import argparse
from html import escape
import json
import math
from pathlib import Path
import random


W, H = 1600, 660
INK, MUTED, RULE = '#26262B', '#707076', '#DADADD'


def tint(color, amount):
    values = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(255+(v-255)*amount):02X}' for v in values)


class Canvas:
    def __init__(self, title, accent, description, secondary):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="183mm" '
                      f'height="75.4875mm" viewBox="0 0 {W} {H}" role="img">',
                      f'<title>{escape(title)}</title><desc>{escape(description)}</desc>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
                      'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                      '<path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="context-stroke" stroke-width="1.3"/>'
                      '</marker></defs>',
                      f'<rect width="{W}" height="{H}" fill="white"/>',
                      '<g font-family="Arial, Helvetica, sans-serif">']
        self.accent = accent
        self.secondary = secondary

    def text(self, x, y, label, size=20, color=INK, weight=400, anchor='start', **attrs):
        extra = ' '.join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k,v in attrs.items())
        self.parts.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}" '
                          f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(label))}</text>')

    def path(self, d, stroke=RULE, width=1.3, fill='none', **attrs):
        extra = ' '.join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k,v in attrs.items())
        self.parts.append(f'<path d="{d}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" {extra}/>')

    def rect(self,x,y,w,h,fill='white',stroke='none',radius=0,**attrs):
        extra=' '.join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k,v in attrs.items())
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                          f'fill="{fill}" stroke="{stroke}" {extra}/>')

    def poly(self,points,fill,stroke='white',width=1,**attrs):
        points = ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
        extra=' '.join(f'{k.replace("_", "-")}="{v}"' for k,v in attrs.items())
        self.parts.append(f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>')

    def circle(self,x,y,r,fill,stroke='none',**attrs):
        extra=' '.join(f'{k.replace("_", "-")}="{v}"' for k,v in attrs.items())
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" {extra}/>')

    def arrow(self,x1,y1,x2,y2,color=MUTED,dashed=False):
        self.path(f'M{x1},{y1} L{x2},{y2}',color,1.6,marker_end='url(#arrow)',
                  **({'stroke_dasharray':'5 5'} if dashed else {}))

    def section(self,x,width,n,title):
        self.text(x,133,n,18,self.accent,600)
        self.text(x+35,133,title,21,INK,600)
        self.path(f'M{x},147 H{x+width}',RULE,1)

    def finish(self):
        self.text(40,635,'SYNTHETIC DESIGN STUDY',15,MUTED,500,letter_spacing='1.4')
        self.text(1560,635,'Original geometry · illustrative results',16,MUTED,anchor='end')
        return ''.join(self.parts)+'</g></svg>'


def header(c,title,subtitle):
    c.text(40,48,title,30,weight=600)
    c.text(40,80,subtitle,18,MUTED)


def scene(c,cx,cy,scale=1,angle=0,highlight=True,points=False):
    """True rotated axonometric projection of the same invented block scene."""
    a=math.radians(angle)
    def p(x,y,z=0):
        u=x*math.cos(a)-y*math.sin(a)
        v=x*math.sin(a)+y*math.cos(a)
        return cx+scale*(u-v)*0.866,cy+scale*(u+v)*0.5-scale*z
    ground=[p(-125,-100),p(125,-100),p(125,100),p(-125,100)]
    c.poly(ground,'#F4F4F5',RULE,0.7)
    for t in range(-100,126,25):
        c.poly([p(t,-100),p(t,100)],'none','#DFDFE2',0.65)
    for t in range(-100,101,25):
        c.poly([p(-125,t),p(125,t)],'none','#DFDFE2',0.65)
    buildings=[(-105,-75,35,36,48),(-50,-75,32,36,72),(5,-75,42,36,42),
               (70,-75,32,36,63),(-105,12,35,36,70),(-45,12,40,36,40),
               (20,12,35,36,85),(78,12,32,36,44)]
    # Order by projected depth, not screen position.
    buildings.sort(key=lambda b: p(b[0]+b[2]/2,b[1]+b[3]/2)[1])
    for i,(x,y,w,d,h) in enumerate(buildings):
        accent=c.accent if highlight and x==20 else (c.secondary if x in (-50,78) else '#87878F')
        strength=1.8 if highlight and x==20 else 1.25
        q=[p(x,y,h),p(x+w,y,h),p(x+w,y+d,h),p(x,y+d,h)]
        c.poly([q[1],q[2],p(x+w,y+d),p(x+w,y)],tint(accent,0.31*strength),'white',0.9)
        c.poly([q[2],q[3],p(x,y+d),p(x+w,y+d)],tint(accent,0.19*strength),'white',0.9)
        c.poly(q,tint(accent,0.10*strength),'white',1)
        # Repeated window bands add geometric detail, not decorative extrusion.
        for z in range(13,int(h),15):
            aa=p(x+3,y+d,z);bb=p(x+w-3,y+d,z)
            c.path(f'M{aa[0]},{aa[1]} L{bb[0]},{bb[1]}',tint(accent,0.45*strength),0.7)
    # Small green-free neutral trees keep the method accent unambiguous.
    for x,y in [(-110,-10),(-72,-8),(60,-8),(115,-9)]:
        xx,yy=p(x,y,12)
        c.path(f'M{xx},{yy} v{scale*12}', '#AAAAAF',1)
        c.circle(xx,yy,5*scale,'#C7C7CB')
    if points:
        rng=random.Random(7)
        for _ in range(110):
            xx,yy=p(rng.uniform(-120,120),rng.uniform(-95,95),rng.uniform(0,30))
            c.circle(xx,yy,1.5,c.accent,opacity='.32')
    return p


def tokens(c,x,y,cols=7,rows=4,step=17,selected=False):
    for j in range(rows):
        for i in range(cols):
            active=(i+j)%4==0 if selected else True
            c.rect(x+i*step,y+j*step,step-4,step-4,
                   tint(c.accent,.55 if active else .07),radius=1)


def camera(c,x,y,size=18,color=MUTED):
    c.rect(x-size/2,y-size*.32,size*.8,size*.64,'white',color,2)
    c.poly([(x+size*.3,y-size*.2),(x+size*.7,y-size*.4),
            (x+size*.7,y+size*.4),(x+size*.3,y+size*.2)],'white',color,1)


def overview(accent,baseline):
    c=Canvas('Scene-first spatial model teaser',accent,'Original synthetic city; observations, memory and novel camera views.',baseline)
    header(c,'From a few observations to a persistent spatial memory',
           'A scene-first overview: what enters the system, what is retained, and what can be queried.')
    c.section(40,380,'01','Observe');c.section(470,590,'02','Represent');c.section(1110,450,'03','Query')
    # Compact, staggered input views.
    scene(c,220,335,.72,-10)
    camera(c,110,432,23)
    c.path('M125,427 L210,360 L260,415 Z',accent,1,fill=tint(accent,.07),stroke_dasharray='4 5')
    c.text(110,490,'Sparse posed observations',20,weight=500)
    c.text(110,519,'Images + camera geometry',18,MUTED)
    c.arrow(395,337,470,337)
    # Largest object is the representation; token bank is a separate abstraction.
    scene(c,746,335,1.05,0,points=True)
    c.path('M578,470 H906',RULE,1)
    tokens(c,648,490,8,2,18,True)
    c.text(720,554,'Shared scene memory',20,weight=500,anchor='middle')
    c.text(720,584,'Spatially indexed features',18,MUTED,anchor='middle')
    c.arrow(1025,337,1090,337)
    for i,ang in enumerate([-24,0,24]):
        x=1160+i*155
        scene(c,x+35,300,.36,ang)
        camera(c,x+34,382,17)
        c.text(x+34,424,f'View {i+1}',18,MUTED,anchor='middle')
    c.text(1127,490,'One scene, multiple viewpoints',20,weight=500)
    c.text(1127,519,'Camera-conditioned outputs',18,MUTED)
    return c.finish()


def retrieval(accent,baseline):
    c=Canvas('Local retrieval mechanism teaser',accent,'Original synthetic geometry demonstrates a camera footprint and memory lookup, not an implemented method.',baseline)
    header(c,'Retrieve locally. Keep the scene consistent.',
           'Mechanism study: a visible spatial query connects a scene region to a compact feature subset.')
    c.section(40,650,'a','Spatial query');c.section(750,810,'b','Memory retrieval')
    p=scene(c,350,355,1.38,-6)
    # Explicit 3D-world footprint, not an invented attention heatmap.
    outline=[p(-15,-40,2),p(90,-40,2),p(90,62,2),p(-15,62,2)]
    c.poly(outline,tint(accent,.08),accent,1.8,stroke_dasharray='6 5',opacity='.8')
    camera(c,165,485,27,accent)
    c.path('M184,478 L330,355 L415,425 Z',accent,1,fill=tint(accent,.10),opacity='.5')
    c.text(125,558,'Query camera',19,weight=500)
    c.path('M500,342 C610,342 625,280 720,280',accent,1.4,stroke_dasharray='4 5')
    c.text(756,207,'Scene-indexed feature bank',20,weight=500)
    tokens(c,756,237,16,5,24,True)
    c.text(756,401,'Select the relevant region',18,MUTED)
    c.arrow(1040,365,1040,425,accent)
    tokens(c,844,449,8,1,25)
    c.arrow(1057,461,1134,461)
    c.rect(1155,432,163,58,tint(accent,.055),tint(accent,.35),5)
    c.text(1236,467,'View decoder',19,anchor='middle',weight=500)
    c.arrow(1334,461,1395,461)
    scene(c,1470,463,.35,12)
    c.text(954,541,'Retrieved tokens',18,MUTED,anchor='middle')
    c.text(1460,541,'Novel view',18,MUTED,anchor='middle')
    return c.finish()


def evidence(accent,baseline):
    c=Canvas('Scene and evidence teaser',accent,'Synthetic scene, invented accuracy-cost curves and an illustrative consistency comparison.',baseline)
    header(c,'A spatial story, supported by focused evidence',
           'Evidence study: large scene context, one controlled detail, and a restrained accuracy–cost plot.')
    c.section(40,670,'a','Scene context');c.section(760,800,'b','Illustrative trade-off')
    scene(c,355,328,1.28,8)
    c.text(80,502,'Same scene · same evaluation view',19,weight=500)
    c.text(80,534,'Use a matched crop to show the claimed difference.',18,MUTED)
    # Plot occupies a precise area, with labels outside the data rectangle.
    x0,y0,pw,ph=850,450,590,245
    for v in [72,76,80,84]:
        yy=y0-(v-70)/15*ph
        c.path(f'M{x0-5},{yy} H{x0}',MUTED,1)
        c.text(x0-16,yy+6,v,17,MUTED,anchor='end')
    for v in [0,4,8,12,16]:
        xx=x0+v/16*pw
        c.path(f'M{xx},{y0} v5',MUTED,1)
        c.text(xx,y0+29,v,17,MUTED,anchor='middle')
    c.path(f'M{x0},{y0-ph} V{y0} H{x0+pw}',MUTED,1.1)
    c.text(x0-52,322,'Accuracy (%)',18,MUTED,anchor='middle',transform=f'rotate(-90 {x0-52} 322)')
    c.text(x0+pw/2,514,'Inference cost (G MACs)',18,MUTED,anchor='middle')
    for label,col,xs,ys in [('Baseline',baseline,[4,8,14],[73,77,80]),
                            ('Variant',accent,[3,6,11],[75,79,82])]:
        coords=[(x0+x/16*pw,y0-(y-70)/15*ph) for x,y in zip(xs,ys)]
        c.path('M'+' L'.join(f'{x},{y}' for x,y in coords),col,2.1)
        for x,y in coords:c.circle(x,y,4.5,col,'white',stroke_width='1')
        x,y=coords[-1]
        c.text(x+13,y+5,label,18,col,500)
    c.text(850,557,'Synthetic values; no measured superiority is claimed.',17,MUTED)
    return c.finish()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--tokens',type=Path,help='paper-colors exported JSON, not a full color-book index')
    parser.add_argument('--png',action='store_true',help='Also render PNG previews (requires resvg-py)')
    args=parser.parse_args()
    if args.tokens:
        data=json.loads(args.tokens.read_text())
        accent=data['hues']['ours']['anchor'];baseline=data['hues']['base1']['anchor']
        source=f'paper-colors theme: {data["theme"]}'
    else:
        # Only two invented fixture values, not Pantone codes or a bundled color book.
        fixture=Path(__file__).resolve().parents[2]/'paper-colors/tests/fixtures/swatches.json'
        data=json.loads(fixture.read_text())
        accent=data['TEST OURS']['hex'];baseline=data['TEST B1']['hex']
        source='Repository synthetic test fixture'
    for value in [accent,baseline]:
        if len(value)!=7 or not value.startswith('#'):
            raise ValueError('Anchor colors must be #RRGGBB')
        int(value[1:],16)
    args.out.mkdir(parents=True,exist_ok=True)
    designs={'spatial-overview':overview(accent,baseline),'local-retrieval':retrieval(accent,baseline),
             'scene-evidence':evidence(accent,baseline)}
    for name,svg in designs.items():
        (args.out/f'{name}.svg').write_text(svg)
        if args.png:
            import resvg_py
            (args.out/f'{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg,width=2000,dpi=96))
    (args.out/'provenance.json').write_text(json.dumps({
        'data':'All geometry, operations, values and results are synthetic design studies.',
        'palette':source,'format':'Editable SVG; preview PNG optional.',
        'scope':'Project teaser studies, not a Nature compliance preset or published model.',
        'limitations':'No real photos, measurements or implemented architecture; replace with actual project evidence.'
    },indent=2)+'\n')
    print(f'Wrote {len(designs)} original vector teaser studies to {args.out}')


if __name__=='__main__':main()
