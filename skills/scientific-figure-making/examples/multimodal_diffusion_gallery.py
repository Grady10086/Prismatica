"""Credited reference layouts from user-supplied published PDFs; no inference."""
import argparse,json,hashlib
from pathlib import Path
import pymupdf as fitz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
BG='#FAF7F0';INK='#253142';MUT='#83909F';TEAL='#45998F';GOLD='#D1B979';ROSE='#C77D70'
RECORD=[]
def text(f,x,y,s,size=9,col=INK,**kw):f.text(x,y,s,fontsize=size,color=col,**kw)
def page(tag,title,sub,dark=False):
 f=plt.figure(figsize=(12,8),facecolor='#101B2B' if dark else BG);ink='#F5EFE5' if dark else INK;text(f,.055,.95,tag,8,TEAL);text(f,.055,.875,title,29,ink,fontfamily='DejaVu Serif');text(f,.055,.825,sub,8,MUT);return f,ink

def images(path,page,expected):
 d=fitz.open(path);p=d[page-1];info=sorted(p.get_image_info(xrefs=True),key=lambda v:(round(v['bbox'][1],0),v['bbox'][0]));assert len(info)==expected, 'Wrong PDF edition/image layout'
 arrays=[]
 for v in info:
  pix=fitz.Pixmap(d,v['xref']);raw=pix.tobytes('png');import io
  a=plt.imread(io.BytesIO(raw));arrays.append(a);RECORD.append({'pdf':Path(path).name,'pdf_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'page':page,'xref':v['xref'],'bbox':list(v['bbox']),'size':[v['width'],v['height']]})
 return arrays

def pic(f,x,y,w,a,nearest=False):
 h=w*1.5*a.shape[0]/a.shape[1];ax=f.add_axes([x,y,w,h]);ax.imshow(a,interpolation='nearest' if nearest else 'antialiased');ax.axis('off');return h

def save(f,out,name,credit):
 text(f,.055,.026,'PUBLISHED REFERENCE LAYOUT · '+credit+' · no new inference',6,MUT);f.savefig(out/(name+'.png'),dpi=190);f.savefig(out/(name+'.svg'));plt.close(f)

def vlm(out,path):
 im=images(path,6,1)[0];f,ink=page('07 / MULTIMODAL RESPONSE AUDIT','One image. Different readings.','LLaVA · Table 3 · same published question across four systems · response summaries are paraphrases')
 pic(f,.055,.34,.43,im);text(f,.055,.79,'VISUAL INPUT',8,TEAL);text(f,.055,.23,'What is unusual about this image?',17,INK,fontfamily='DejaVu Serif');text(f,.055,.16,'Compare instruction following, scene description\nand unsupported details separately.',9,MUT,linespacing=1.8)
 responses=[('LLaVA','Describes ironing on a vehicle as an unusual setting.',TEAL),('GPT-4','Identifies an ironing board attached to a moving taxi.',TEAL),('BLIP-2','Describes a man sitting on a yellow cab.',ROSE),('OpenFlamingo','Describes drying clothes on a car hood.',ROSE)]
 for k,(name,summary,col) in enumerate(responses):
  y=.70-k*.145;f.add_artist(Rectangle((.59,y-.075),.35,.115,transform=f.transFigure,facecolor='#EEEDE5',edgecolor='none'));text(f,.61,y+.012,name,13,col,fontfamily='DejaVu Serif');import textwrap
  text(f,.61,y-.044,'\n'.join(textwrap.wrap(summary,46)),8,INK,linespacing=1.6)
 text(f,.59,.085,'Single qualitative example; no aggregate ranking implied.',7,MUT)
 save(f,out,'mllm-response-audit','Liu et al. / Visual Instruction Tuning / Table 3; original photo source in paper')

def guidance(out,path):
 tiles=images(path,5,9);compare=images(path,7,20)[:5];assert all(t.shape[:2]==(512,512) for t in tiles)
 f,ink=page('08 / DIFFUSION CONTROL ATLAS','The edit is a trade-off.','InstructPix2Pix · original guidance sweep and baseline outputs · no synthetic quality scores',True)
 # Large hero and a full two-condition response surface made of real images.
 pic(f,.055,.31,.23,tiles[4]);text(f,.055,.79,'EDIT INSTRUCTION',8,TEAL);text(f,.055,.70,'Turn him into\na cyborg!',22,ink,fontfamily='DejaVu Serif',linespacing=1.25);text(f,.055,.28,'Hero: sI = 1.2 · sT = 7.5',8,MUT)
 text(f,.405,.765,'TEXT GUIDANCE  sT',8,TEAL)
 for c,v in enumerate(['3','7.5','15']):text(f,.465+c*.158,.733,v,9,ink)
 for r,v in enumerate(['1.0','1.2','1.6']):
  text(f,.365,.62-r*.15,v,9,MUT)
  for c in range(3):pic(f,.425+c*.158,.56-r*.15,.09,tiles[r*3+c])
 text(f,.35,.242,'Rows: image guidance sI · Columns: text guidance sT',7,MUT)
 text(f,.055,.225,'SAME EDIT / DIFFERENT METHODS · “make it look like a Dali Painting”',8,TEAL)
 for k,(im,label) in enumerate(zip(compare,['Input','SDEdit · caption','Text2Live','SDEdit · edit','InstructPix2Pix'])):
  x=.055+k*.182;pic(f,x,.07,.093,im);text(f,x+.097,.113,label.replace(' · ','\n'),7,ink)
 save(f,out,'diffusion-control-atlas','Brooks et al. / InstructPix2Pix / Figs. 4 & 9; author outputs')

def process(out,path):
 tiles=images(path,5,16);assert tiles[0].shape[:2]==(274,274);hero=tiles[0];words=tiles[1:7];steps=tiles[7:];assert len(steps)==9
 f,ink=page('09 / GENERATION PROCESS STUDY','A concept takes shape.','Prompt-to-Prompt · published cross-attention over diffusion steps · maps are not denoised image frames')
 pic(f,.055,.325,.27,hero);text(f,.055,.765,'SYNTHESIZED IMAGE',8,TEAL);text(f,.055,.275,'A furry bear watches a bird.',16,INK,fontfamily='DejaVu Serif')
 text(f,.44,.765,'WORD–IMAGE CORRESPONDENCE',8,TEAL)
 for k,(im,label) in enumerate(zip(words,['a','furry','bear','watches','a','bird'])):
  x=.44+(k%3)*.17;y=.535-(k//3)*.215;pic(f,x,y,.112,im,True);text(f,x,y-.025,label,10,INK,fontfamily='DejaVu Serif')
 text(f,.055,.225,'“BEAR” ATTENTION THROUGH GENERATION',8,TEAL)
 for k,im in enumerate(steps):
  x=.055+k*.1;pic(f,x,.075,.083,im,True);text(f,x,.065,f'{k+1:02}',6,MUT)
 text(f,.055,.205,'Original sample order: t = T → t = 1. Published maps retained without recoloring or quantitative rescaling.',7,MUT)
 save(f,out,'diffusion-process-attention','Hertz et al. / Prompt-to-Prompt / Fig. 4; native 16×16 maps')

def main():
 p=argparse.ArgumentParser();p.add_argument('--llava',type=Path,required=True);p.add_argument('--instruct',type=Path,required=True);p.add_argument('--ptp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'});vlm(a.out,a.llava);guidance(a.out,a.instruct);process(a.out,a.ptp);(a.out/'source-record.json').write_text(json.dumps({'kind':'PUBLISHED REFERENCE COMPOSITIONS / NO NEW INFERENCE','sources':['https://arxiv.org/abs/2304.08485','https://arxiv.org/abs/2211.09800','https://prompt-to-prompt.github.io/'],'assets':RECORD},indent=2));print(a.out)
if __name__=='__main__':main()
