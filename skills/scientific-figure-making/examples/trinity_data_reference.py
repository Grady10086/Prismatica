"""Redraw explicit published Trinity Fig.7/Table4 values; requires verified local PDF."""
import argparse,json,re,hashlib
from pathlib import Path
import numpy as np
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cs_paper_data_gallery import setup
URL='https://arxiv.org/pdf/2610.36077'
ROWS=['PST','HCI','CFR','GVT','VEA','VC'];COLS=['Perception','Memory','Inference','Planning','Orchestration','Loop']
R=np.array([[.099,.306,-.266,.065,.068,-.313],[-.183,-.183,.744,-.013,-.124,-.183],[-.290,.131,-.246,.274,.089,-.080],[-.361,.042,.149,-.194,.028,.444],[.347,.082,-.155,-.198,.236,-.183],[.286,.286,-.092,-.229,-.074,-.109]])
METHODS=['Random','Self-routing','+ Capability','+ Memory','Oracle']
VALUES=np.array([[52.74,567.08,46.23,594.25],[65.79,535.53,52.36,582.29],[70.34,510.55,58.27,556.21],[71.27,497.89,60.96,541.28],[73.16,486.53,63.61,528.34]])
def save(f,out,name,note):
 f.text(.11,.025,'REDRAWN PUBLISHED VALUES · The Trinity, arXiv:2610.36077v1 · '+note,fontsize=5,color='#666666')
 for ext in ['png','svg','pdf']:f.savefig(out/(name+'.'+ext),dpi=300)
 plt.close(f)
def main():
 p=argparse.ArgumentParser();p.add_argument('--paper',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);d=pymupdf.open(a.paper);assert 'Capability-Driven Recursive Self-Improvement' in d[0].get_text();t=d[11].get_text();matrix=t[t.index('Cap.\nPercep.'):t.index('Corr.\n-1')];read=np.array([float(v) for v in re.findall(r'-?\d+\.\d{3}',matrix)]);assert read.shape==(36,) and np.allclose(read.reshape(6,6),R), 'Figure 7 values differ; check PDF edition'
 table=t[t.index('Random\n'):t.index('Evaluation.')];vals=np.array([float(v) for v in re.findall(r'\d+\.\d{2}',table)]);assert vals.shape==(20,) and np.allclose(vals.reshape(5,4),VALUES),'Table 4 values differ'
 overview=[v for v in d[0].get_image_info(xrefs=True) if v['width']==4600 and v['height']==2181]
 assert len(overview)==1, 'Figure 1 source asset differs; check PDF edition'
 pymupdf.Pixmap(d,overview[0]['xref']).save(a.out/'trinity-overview-original.png')
 setup();f,ax=plt.subplots(figsize=(180/25.4,91/25.4));f.subplots_adjust(left=.13,right=.92,top=.89,bottom=.28);im=ax.imshow(R,vmin=-1,vmax=1,cmap='RdBu_r',aspect='auto');ax.set(yticks=range(6),yticklabels=ROWS,xticks=range(6),xticklabels=COLS);ax.tick_params(axis='x',rotation=25)
 for i in range(6):
  for j in range(6):ax.text(j,i,f'{R[i,j]:.3f}',ha='center',va='center',fontsize=7,color='white' if abs(R[i,j])>.6 else '#222222')
 ax.set_title('Capability–protocol correlations · Iteration 4',loc='left',pad=9);cb=f.colorbar(im,ax=ax,fraction=.025,pad=.025,ticks=[-1,0,1]);cb.set_label('Correlation');save(f,a.out,'trinity-capability-correlations','Fig. 7; descriptive associations, no significance inferred.')
 f,axs=plt.subplots(1,2,figsize=(180/25.4,90/25.4));f.subplots_adjust(left=.16,right=.97,top=.89,bottom=.24,wspace=.5);colors=['#999999','#8EA9B5','#4F8190','#A52C42','#292D36']
 for k,(ax,title) in enumerate(zip(axs,['Train','Unseen'])):
  x=VALUES[:,1+2*k];y=VALUES[:,2*k];ax.plot(x[:4],y[:4],c='#BFC4C6',lw=.7)
  for i,name in enumerate(METHODS):
   marker='*' if i==4 else 'o';ax.scatter(x[i],y[i],s=50 if i==4 else 18,c=colors[i],marker=marker,zorder=3);ax.annotate(name,(x[i],y[i]),xytext=((-30,11) if i==3 else (4,4 if i%2==0 else -10)),textcoords='offset points',fontsize=5.8)
  ax.set(title=title,xlabel='Total inference tokens (M) ↓',ylabel='Benchmark-equal performance ↑');ax.margins(x=.3,y=.2);ax.text(-.22,1.12,'ab'[k],transform=ax.transAxes,fontweight='bold',fontsize=9)
 save(f,a.out,'trinity-routing-performance-cost','Table 4; Oracle is retrospective, not a deployable router.')
 (a.out/'source-data.json').write_text(json.dumps({'source_url':URL,'version':'v1','pdf_sha256':hashlib.sha256(a.paper.read_bytes()).hexdigest(),'page':12,'overview':{'page':1,'figure':1,'native_size':[4600,2181],'xref':overview[0]['xref'],'bbox':list(overview[0]['bbox']),'kind':'unaltered original raster image extracted from supplied PDF; authors artwork'},'figure7':{'rows':ROWS,'columns':COLS,'coefficients':R.tolist()},'table4':{'methods':METHODS,'columns':['Train','Train inference tokens M','Unseen','Unseen inference tokens M'],'values':VALUES.tolist()},'uncertainty':'No run-level samples or error bars in these source panels; none added'},indent=2));print(a.out)
if __name__=='__main__':main()
