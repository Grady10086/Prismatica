"""2025 paper reference studies: recorded denoising states, alignment, failure audit."""
import argparse,hashlib,json,io
from pathlib import Path
import pymupdf as fitz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from multimodal_diffusion_gallery import page,text,pic,save,TEAL,MUT,INK,ROSE
RECORD=[]
URLS={'asced':'https://openaccess.thecvf.com/content/CVPR2025/papers/Cao_Temporal_Score_Analysis_for_Understanding_and_Correcting_Diffusion_Artifacts_CVPR_2025_paper.pdf','mir':'https://openaccess.thecvf.com/content/ICCV2025/papers/Huang_Deciphering_Cross-Modal_Alignment_in_Large_Vision-Language_Models_via_Modality_Integration_ICCV_2025_paper.pdf','flow':'https://openaccess.thecvf.com/content/CVPR2025/papers/Zhang_Cross-modal_Information_Flow_in_Multimodal_Large_Language_Models_CVPR_2025_paper.pdf'}
class Sources:
 def __init__(self,args):
  self.docs={};self.hashes={}
  for name in URLS:
   p=getattr(args,name);self.docs[name]=fitz.open(p);self.hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 def crop(self,name,pn,box,label):
  page=self.docs[name][pn-1];rect=fitz.Rect(box);assert page.rect.contains(rect);raw=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect,alpha=False).tobytes('png');RECORD.append({'source':name,'page':pn,'crop_points':box,'label':label});return plt.imread(io.BytesIO(raw))
 def states(self):
  d=self.docs['asced'];infos=[v for v in d[0].get_image_info(xrefs=True) if v['width']==v['height']==256];assert len(infos)==36
  infos.sort(key=lambda v:(round(v['bbox'][1]/10),v['bbox'][0]));out=[]
  for v in infos:
   RECORD.append({'source':'asced','page':1,'xref':v['xref'],'bbox':v['bbox'],'label':'Fig1 recorded state'});out.append(plt.imread(io.BytesIO(fitz.Pixmap(d,v['xref']).tobytes('png'))))
  return [out[i:i+9] for i in range(0,36,9)]
def rule(f,y):f.add_artist(Line2D([.055,.945],[y,y],transform=f.transFigure,color='#DAD8D0',lw=.5))
def denoise(out,src):
 states=src.states();f,ink=page('10 / DENOISING FIELD NOTES · CVPR 2025','From a face to an artifact.','ASCED · author-recorded generation snapshots · four independent trajectories; no interpolated states')
 pic(f,.055,.38,.25,states[3][-1]);text(f,.055,.77,'FEATURED FINAL STATE',8,TEAL);text(f,.055,.31,'The artifact survives.',18,INK,fontfamily='DejaVu Serif');text(f,.055,.24,'Same source row as trajectory 04.\nThe paper identifies the lower two\nrows as artifact-producing examples.',8,MUT,linespacing=1.7)
 for r,row in enumerate(states):
  y=.625-r*.132;text(f,.35,y+.026,f'{r+1:02}',10,ROSE if r>1 else TEAL)
  for c,a in enumerate(row):pic(f,.39+c*.061,y,.052,a)
 for x,label in [(.39,'PROFILING'),(.573,'MUTATION'),(.756,'REFINEMENT')]:text(f,x,.765,label,8,TEAL)
 text(f,.39,.14,'Within each row: original left-to-right sample order.',8,MUT);text(f,.39,.105,'Phase groups follow Fig. 1; numeric timesteps are not supplied.',7,MUT)
 save(f,out,'recent-denoising-fieldnotes','Cao et al. / Temporal Score Analysis / CVPR 2025 / Fig. 1')
def alignment(out,src):
 f,ink=page('11 / CROSS-MODAL EVIDENCE BOARD · 2025','Alignment needs evidence.','Two independent published studies · embedding geometry and attention-knockout evidence are kept separate')
 # Keep original legends and axes instead of digitizing source curves.
 scatter=src.crop('mir',2,[52,69,177,163],'Fig2 left tSNE and original labels');gap=src.crop('mir',2,[178,68,294,162],'Fig2 right modality gap');mechanism=src.crop('flow',1,[322,230,566,495],'Fig1 information-flow illustration')
 text(f,.055,.77,'A / DISTRIBUTION GEOMETRY',8,TEAL);pic(f,.055,.395,.32,scatter);text(f,.055,.35,'MIR · ICCV 2025 · Fig. 2',9,INK);text(f,.055,.29,'Visual/text token distributions in LLaVA-v1.5.\nA projection view is not a causal alignment test.',8,MUT,linespacing=1.6)
 pic(f,.055,.082,.16,gap);text(f,.26,.19,'Layer-wise modality gap',11,INK,fontfamily='DejaVu Serif');text(f,.26,.13,'Original axes and legend retained.\nSource plot is rasterized, not re-estimated.',7,MUT,linespacing=1.7)
 text(f,.53,.77,'B / INFORMATION TRANSFER',8,TEAL);pic(f,.53,.29,.27,mechanism);text(f,.53,.24,'Information Flow · CVPR 2025 · Fig. 1',9,INK)
 text(f,.53,.17,'Illustration of the authors’ knockout-based findings:\ngeneral visual transfer → selective transfer → answer.\nNot a measured flow diagram for the example alone.',8,MUT,linespacing=1.7)
 save(f,out,'recent-crossmodal-evidence','Huang et al. / ICCV 2025 Fig. 2 + Zhang et al. / CVPR 2025 Fig. 1; distinct studies')
def failure(out,src):
 f,ink=page('12 / CORRECTION FAILURE ATLAS · CVPR 2025','A correction can go wrong.','ASCED · distinguish unintended edits, missed artifacts and failures of the correction itself',True)
 # Retain source-method labels and source boxes in rendered crops.
 example=src.crop('asced',7,[56,58,224,136],'Fig5 first example with original method labels');fp=src.crop('asced',7,[316,333,398,394],'Fig6 false positives');fn=src.crop('asced',7,[396,333,555,394],'Fig6 false negatives');typical=src.crop('asced',7,[316,395,555,432],'Fig6 bottom typical correction failures')
 text(f,.055,.77,'01 / ORIGINAL AND CORRECTIONS',8,TEAL);pic(f,.055,.40,.43,example);text(f,.055,.34,'Original · SARGD · State Replacement · Ours',8,ink);text(f,.055,.27,'One source example, four published views.\nYellow box and method labels are author annotations.',8,MUT,linespacing=1.8)
 text(f,.56,.77,'02 / DETECTION ERRORS',8,TEAL);pic(f,.56,.56,.125,fp);pic(f,.71,.56,.235,fn);text(f,.56,.52,'False positives',10,ink,fontfamily='DejaVu Serif');text(f,.76,.52,'False negatives',10,ink,fontfamily='DejaVu Serif')
 text(f,.56,.43,'03 / TYPICAL CORRECTION FAILURES',8,TEAL);pic(f,.56,.25,.385,typical);text(f,.56,.19,'A failed edit is not the same as a missed detection.',9,ink);text(f,.055,.09,'Qualitative, author-selected examples · no failure rates or new model judgments inferred from this page.',8,MUT)
 save(f,out,'recent-correction-failures','Cao et al. / Temporal Score Analysis / CVPR 2025 / Figs. 5–6')
def main():
 p=argparse.ArgumentParser()
 for name in URLS:p.add_argument('--'+name,type=Path,required=True)
 p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'});src=Sources(a);denoise(a.out,src);alignment(a.out,src);failure(a.out,src);(a.out/'source-record.json').write_text(json.dumps({'kind':'2025 PUBLISHED REFERENCE LAYOUTS / NO NEW INFERENCE','urls':URLS,'pdf_sha256':src.hashes,'assets':RECORD},indent=2));print(a.out)
if __name__=='__main__':main()
