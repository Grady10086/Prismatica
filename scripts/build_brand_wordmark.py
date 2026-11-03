"""Compose Prismatica's symbol as its initial P, followed by outlined rismatica."""
from pathlib import Path
import xml.etree.ElementTree as ET
from copy import deepcopy
import matplotlib
matplotlib.use('Agg')
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path as MP
ROOT=Path(__file__).resolve().parents[1]
SVG='http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)

def outlined(path):
    result=[]
    for points, code in path.iter_segments(curves=True,simplify=False):
        if code==MP.MOVETO:result.append(f'M{points[0]:.3f},{points[1]:.3f}')
        elif code==MP.LINETO:result.append(f'L{points[0]:.3f},{points[1]:.3f}')
        elif code==MP.CURVE3:result.append(f'Q{points[0]:.3f},{points[1]:.3f} {points[2]:.3f},{points[3]:.3f}')
        elif code==MP.CURVE4:result.append('C'+' '.join(f'{points[i]:.3f},{points[i+1]:.3f}' for i in range(0,6,2)))
        elif code==MP.CLOSEPOLY:result.append('Z')
    return ' '.join(result)

def build():
    font=FontProperties(family='DejaVu Sans',weight='normal')
    suffix=TextPath((0,0),'rismatica',size=96,prop=font)
    cap=TextPath((0,0),'P',size=96,prop=font).get_extents().height
    scale=cap/168
    # Symbol bounds in its native artwork are x=58..198, y=44..212.
    x=24-58*scale;y=106-212*scale
    suffix_x=24+140*scale+6-suffix.get_extents().xmin
    width=suffix_x+suffix.get_extents().xmax+24
    source=ET.parse(ROOT/'docs/brand/symbol.svg').getroot()
    for name,ink in [('horizontal.svg','#333F49'),('horizontal-dark.svg','#F5F5F5')]:
        root=ET.Element(f'{{{SVG}}}svg',{'width':f'{width:.2f}','height':'142','viewBox':f'0 0 {width:.2f} 142','role':'img','aria-label':'Prismatica'})
        ET.SubElement(root,f'{{{SVG}}}title').text='Prismatica — symbol as initial P'
        mark=ET.SubElement(root,f'{{{SVG}}}g',{'id':'initial-p','transform':f'translate({x:.4f} {y:.4f}) scale({scale:.6f})'})
        for child in source:
            if child.tag.endswith('title'):continue
            mark.append(deepcopy(child))
        ET.SubElement(root,f'{{{SVG}}}path',{'id':'suffix-rismatica','fill':ink,'transform':f'translate({suffix_x:.4f} 106) scale(1 -1)','d':outlined(suffix)})
        (ROOT/'docs/brand'/name).write_text(ET.tostring(root,encoding='unicode')+'\n')
    print('Updated integrated wordmarks; original symbol and palette unchanged.')

if __name__=='__main__':build()
