"""Non-city teaser templates: grounded multimodal QA, generation and robot control.

Original synthetic vector illustrations, not reproduced paper figures or results.
Optional local raster assets are embedded in SVG; no network or user registry access.
"""
from __future__ import annotations

import argparse
import base64
from html import escape
import json
from pathlib import Path
import random

from teaser_gallery import Canvas, INK, MUTED, RULE, header, tint, tokens


def ellipse(c,x,y,rx,ry,fill,stroke='none',width=1):
    c.parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')


def mug(c,x,y,s,color,pattern=0):
    """Frontal ceramic cup with a visible rim and handle; x/y is top-left."""
    c.path(f'M{x+57*s},{y+20*s} C{x+96*s},{y+8*s} {x+96*s},{y+72*s} {x+57*s},{y+63*s}',
           tint(color,.7),7*s)
    c.path(f'M{x},{y+11*s} L{x+5*s},{y+78*s} Q{x+30*s},{y+91*s} {x+57*s},{y+78*s} '
           f'L{x+62*s},{y+11*s} Z',tint(color,.75),1.1*s,tint(color,.22))
    ellipse(c,x+31*s,y+11*s,31*s,10*s,tint(color,.09),tint(color,.7),s)
    ellipse(c,x+31*s,y+11*s,23*s,5*s,tint(color,.45))
    if pattern==1:
        for z in [30,45,60]:c.path(f'M{x+4*s},{y+z*s} L{x+58*s},{y+z*s}',color,3*s)
    if pattern==2:
        for i in range(3):
            for j in range(3):c.circle(x+(14+i*15)*s,y+(30+j*16)*s,2.7*s,color)


def tabletop(c,x,y,w,h,highlight=False):
    c.rect(x,y,w,h,'#FAFAFB',RULE,5)
    c.path(f'M{x+12},{y+h*.72} H{x+w-12}',RULE,1)
    s=min(w/250,h/170)
    mx,my=x+w*.18,y+h*.24
    mug(c,mx,my,s,c.secondary)
    bx,by=x+w*.73,y+h*.60
    c.path(f'M{bx-36*s},{by} Q{bx},{by+65*s} {bx+36*s},{by} Z',tint(c.accent,.5),s,tint(c.accent,.13))
    ellipse(c,bx,by,36*s,9*s,tint(c.accent,.08),tint(c.accent,.5),s)
    if highlight:c.rect(mx-7*s,my-4*s,104*s,104*s,'none',c.secondary,3,stroke_width=1.6)


def asset(c,x,y,w,h,key,assets,fallback):
    if key not in assets:
        fallback()
        return False
    path=assets[key]
    data=path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):mime='image/png'
    elif data.startswith(b'\xff\xd8\xff'):mime='image/jpeg'
    elif data.startswith(b'RIFF') and data[8:12]==b'WEBP':mime='image/webp'
    else:raise ValueError(f'{key}: use PNG, JPEG or WebP')
    c.rect(x,y,w,h,'#FAFAFB',RULE,5)
    c.parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" '
                   f'preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{base64.b64encode(data).decode()}"/>')
    return True


def caption(c,x,y,title,note,anchor='start'):
    c.text(x,y,title,20,weight=500,anchor=anchor)
    c.text(x,y+28,note,17,MUTED,anchor=anchor)


def multimodal(accent,secondary,assets):
    c=Canvas('Grounded visual question answering',accent,
             'Original illustration: an input image and a question connect to visual and text tokens, then a grounded answer.',secondary)
    header(c,'Connect what is seen with what is asked.',
           'Multimodal teaser · image evidence, language input and an explicit grounded response')
    c.section(40,425,'01','Image + question');c.section(525,520,'02','Cross-modal reasoning');c.section(1105,455,'03','Grounded response')
    asset(c,55,205,390,245,'multimodal_input',assets,lambda:tabletop(c,55,205,390,245))
    c.rect(55,476,390,66,tint(accent,.04),radius=6)
    c.text(73,503,'Question',16,MUTED,500)
    c.text(73,529,'What is left of the bowl?',21)
    c.arrow(465,325,530,325)
    c.text(550,222,'Visual features',18,MUTED)
    tokens(c,555,242,8,3,24,True)
    c.text(550,408,'Text tokens',18,MUTED)
    for i,label in enumerate(['What','is','left','?']):
        c.rect(555+i*74,430,63,35,tint(secondary,.14),radius=3)
        c.text(586+i*74,453,label,17,anchor='middle')
    # Connectors show a conceptual interface, not measured attention weights.
    for yy in [270,295,442]:
        c.path(f'M850,{yy} C880,{yy} 880,346 907,346',tint(accent,.45),1.2)
    c.rect(910,265,108,162,tint(accent,.07),tint(accent,.4),8)
    c.text(964,338,'Vision–',19,anchor='middle',weight=500)
    c.text(964,366,'language',19,anchor='middle',weight=500)
    c.text(780,515,'Keep image evidence linked',18,MUTED,anchor='middle')
    c.text(780,542,'to the language response.',18,MUTED,anchor='middle')
    c.arrow(1035,345,1090,345)
    custom=asset(c,1125,205,410,245,'multimodal_output',assets,lambda:tabletop(c,1125,205,410,245,True))
    caption(c,1125,495,'Grounded answer' if custom else '“The cup is left of the bowl.”',
            'Replace the example with verified output.' if custom else 'A region mark links the answer to evidence.')
    return c.finish()


def denoising(accent,secondary,assets):
    c=Canvas('Conditional image generation teaser',accent,
             'Synthetic denoising illustration and ceramic-cup samples; not outputs of an actual diffusion model.',secondary)
    header(c,'Turn a condition into a coherent family of images.',
           'Generation teaser · distinguish the condition, the iterative process and the sampled outputs')
    c.section(40,320,'01','Condition');c.section(420,700,'02','Illustrative denoising');c.section(1180,380,'03','Samples')
    c.rect(55,224,285,176,tint(accent,.035),radius=8)
    c.text(79,260,'TEXT PROMPT',16,MUTED,500,letter_spacing='1')
    c.text(79,308,'A ceramic cup',25,weight=500)
    c.text(79,341,'with a curved handle',19)
    c.text(79,377,'Illustrative condition',16,MUTED)
    c.arrow(354,326,407,326)
    for i in range(4):
        x,y=437+i*171,252
        c.rect(x,y,143,143,'#FAFAFB',RULE,4)
        # These are deliberately labelled drawings, not a simulated learned process.
        if i>0:mug(c,x+37,y+32,.92,accent)
        rng=random.Random(21+i)
        count=[160,95,35,0][i]
        for _ in range(count):
            xx=x+rng.uniform(7,136); yy=y+rng.uniform(7,136)
            c.circle(xx,yy,rng.uniform(1.5,3.5),tint(accent,rng.uniform(.1,.55)),opacity=str(.8-i*.15))
        if i<3:c.arrow(x+149,y+71,x+165,y+71)
        c.text(x+71,y+178,['Noise','Coarse form','Refinement','Image'][i],18,MUTED,anchor='middle')
    c.path('M475,492 H1070',RULE,1)
    c.text(770,525,'Denoising order →',19,MUTED,anchor='middle')
    for i in range(2):
        for j in range(2):
            x,y=1195+j*177,217+i*173
            key=f'generated_{i*2+j+1}'
            def draw(x=x,y=y,j=j,i=i):
                c.rect(x,y,156,144,'#FAFAFB',RULE,4)
                mug(c,x+41,y+29,.95,accent if j==0 else secondary,i)
            asset(c,x,y,156,144,key,assets,draw)
    c.text(1360,588,'Fixed prompt · varied samples',17,MUTED,anchor='middle')
    return c.finish()


def controls(accent,secondary,assets):
    c=Canvas('Controlled generation comparison matrix',accent,
             'Original cups in a matched layout. Rows vary finishes; columns vary patterns. All are illustrations.',secondary)
    header(c,'Show control by changing one factor at a time.',
           'Comparison teaser · aligned outputs make the controlled factor visible without a large model diagram')
    c.text(59,153,'Shared condition',20,weight=500)
    c.rect(55,177,275,147,tint(accent,.04),radius=6)
    c.text(77,215,'Same cup geometry',23,weight=500)
    c.text(77,249,'Same viewpoint',19)
    c.text(77,281,'Same framing',19)
    c.text(58,394,'Rows: finish color',19,MUTED)
    c.text(58,427,'Columns: surface pattern',19,MUTED)
    c.text(58,485,'Use a factorial comparison',18,MUTED)
    c.text(58,512,'when both controls are tested.',18,MUTED)
    c.arrow(354,337,414,337)
    for j,label in enumerate(['Plain','Stripes','Dots']):
        c.text(643+j*330,157,label,21,anchor='middle',weight=500)
    for i,label in enumerate(['Finish A','Finish B']):
        y=194+i*194
        c.text(443,y+91,label,18,MUTED,anchor='middle',transform=f'rotate(-90 443 {y+91})')
        for j in range(3):
            x=505+j*330
            def draw(x=x,y=y,i=i,j=j):
                c.rect(x,y,275,168,'#FAFAFB',RULE,5)
                mug(c,x+94,y+27,1.35,accent if i==0 else secondary,j)
            asset(c,x,y,275,168,f'control_{i+1}_{j+1}',assets,draw)
    c.text(983,600,'Matched geometry and camera; only the labelled controls change.',18,MUTED,anchor='middle')
    return c.finish()


def robot(c,x,y,w,h,phase):
    """An explicitly schematic tabletop arm moving one object into a tray."""
    c.rect(x,y,w,h,'#FAFAFB',RULE,5)
    c.path(f'M{x+12},{y+h*.81} H{x+w-12}', '#CCCCD0',1)
    # Object state and end-effector position agree in the three drawings.
    positions=[(.47,.67),(.61,.39),(.79,.67)]
    ox,oy=positions[phase]
    px,py=x+w*ox,y+h*oy
    c.rect(x+w*.70,y+h*.69,w*.23,h*.105,tint(c.secondary,.13),tint(c.secondary,.5),3)
    c.rect(px-11,py-8,22,21,tint(c.secondary,.5),c.secondary,3)
    base=(x+w*.16,y+h*.79);shoulder=(x+w*.21,y+h*.48)
    elbow=(x+w*(.34 if phase==0 else .42),y+h*.24)
    wrist=(px,py-31)
    coords=[base,shoulder,elbow,wrist]
    d='M'+' L'.join(f'{a},{b}' for a,b in coords)
    c.path(d,'#D6D6DC',13,stroke_linecap='round',stroke_linejoin='round')
    c.path(d,c.accent,2.3,stroke_linecap='round',stroke_linejoin='round')
    for a,b in coords[:-1]:c.circle(a,b,6,'white',c.accent,stroke_width=1.7)
    c.path(f'M{px-12},{py-26} v14 h5 M{px+12},{py-26} v14 h-5',c.accent,2.1)
    c.rect(base[0]-21,base[1],43,11,'#D6D6DC',radius=2)


def robotics(accent,secondary,assets):
    c=Canvas('Robot perception-action feedback teaser',accent,
             'Schematic pick-and-place arm, language instruction, action chunk and observation feedback; no executed robot rollout.',secondary)
    header(c,'See, act, and observe again.',
           'Robotics teaser · connect a language goal to a task sequence and an explicit feedback loop')
    c.section(40,345,'01','Observe + instruct');c.section(445,335,'02','Predict actions');c.section(840,720,'03','Execute + reobserve')
    asset(c,55,214,315,228,'robot_observation',assets,lambda:robot(c,55,214,315,228,0))
    c.rect(55,475,315,61,tint(secondary,.09),radius=5)
    c.text(75,510,'“Place the object in the tray.”',20)
    c.arrow(387,331,438,331)
    c.rect(470,239,270,134,tint(accent,.055),tint(accent,.4),7)
    c.text(605,290,'Vision–language',23,anchor='middle',weight=500)
    c.text(605,323,'action policy',23,anchor='middle',weight=500)
    c.arrow(605,388,605,425,accent)
    for i in range(7):c.rect(490+i*32,443,25,29,tint(accent,.75 if i<3 else .12),radius=2)
    c.text(605,512,'Predicted action chunk',18,MUTED,anchor='middle')
    c.text(605,540,'Execute a prefix; replan.',17,MUTED,anchor='middle')
    c.arrow(755,332,825,332)
    for i,label in enumerate(['Approach','Lift','Place']):
        x=850+i*239
        asset(c,x,245,220,182,f'robot_step_{i+1}',assets,lambda x=x,i=i:robot(c,x,245,220,182,i))
        c.text(x+110,462,label,19,anchor='middle',weight=500)
        c.text(x+110,490,f'Stage {i+1}',16,MUTED,anchor='middle')
    # A new observation, rather than an arrow implying training gradients.
    c.path('M1440,514 V573 H210 V554',accent,1.3,stroke_dasharray='6 5',marker_end='url(#arrow)')
    c.rect(855,559,272,28,'white')
    c.text(991,580,'New visual observation',18,accent,anchor='middle')
    return c.finish()


ALLOWED_ASSETS={'multimodal_input','multimodal_output','robot_observation',
                *(f'generated_{i}' for i in range(1,5)),
                *(f'robot_step_{i}' for i in range(1,4)),
                *(f'control_{i}_{j}' for i in range(1,3) for j in range(1,4))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--tokens',type=Path,help='paper-colors JSON export')
    parser.add_argument('--assets',type=Path,help='JSON mapping named slots to local PNG/JPEG/WebP files')
    parser.add_argument('--png',action='store_true',help='Render previews with optional resvg-py')
    args=parser.parse_args()
    if args.tokens:
        data=json.loads(args.tokens.read_text())
        accent=data['hues']['ours']['anchor'];secondary=data['hues']['base1']['anchor']
        theme=data['theme']
    else:
        # Two invented fixture values, not Pantone data; standalone default.
        accent='#332288';secondary='#CC6677';theme='synthetic fixture'
    for value in (accent,secondary):
        if not isinstance(value,str) or len(value)!=7 or not value.startswith('#'):
            raise ValueError('Colors must be #RRGGBB')
        int(value[1:],16)
    assets={}
    if args.assets:
        data=json.loads(args.assets.read_text())
        if not isinstance(data,dict) or set(data)-ALLOWED_ASSETS:
            raise ValueError('Asset manifest contains unsupported slots')
        for key,value in data.items():
            path=Path(value).expanduser()
            if not path.is_absolute():path=args.assets.resolve().parent/path
            if not path.is_file():raise ValueError(f'{key}: missing local file')
            assets[key]=path
    designs={name:fn(accent,secondary,assets) for name,fn in [
        ('multimodal-grounding',multimodal),('conditional-generation',denoising),
        ('controlled-generation',controls),('robot-action-loop',robotics)]}
    args.out.mkdir(parents=True,exist_ok=True)
    for name,svg in designs.items():
        (args.out/f'{name}.svg').write_text(svg)
        if args.png:
            import resvg_py
            (args.out/f'{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg,width=2000,dpi=96))
    (args.out/'provenance.json').write_text(json.dumps({
        'template':'Original domain-specific composition studies; not paper reproductions.',
        'illustrations':'Synthetic vectors except for explicitly supplied local image slots.',
        'palette':theme,'supplied_image_slots':sorted(assets),
        'warning':'Example prompts, actions and labels must be edited to match actual research. '
                  'Drawn noise is not a model trace; a drawn robot sequence is not an executed rollout.'
    },indent=2)+'\n')
    print(f'Wrote {len(designs)} domain teaser templates to {args.out}')


if __name__=='__main__':main()
