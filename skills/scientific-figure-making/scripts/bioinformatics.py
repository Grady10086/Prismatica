"""Bioinformatics composition helpers for supplied tables (no biological inference).

Render an exported Prismatica CSV with --kind oncoprint/spatial/phylogeny/circos/sashimi.
The CLI exports editable SVG/PDF plus PNG. Spatial images are optional local files.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import csv
from pathlib import Path
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from matplotlib.patches import Rectangle, Wedge, PathPatch
from matplotlib.path import Path as MPath
import numpy as np

COLORS=['#55609B','#AB6690','#E6A385','#758E8B','#8890B9','#C28EAE','#EEC2AD','#9EB1AF']
PAPER='#F8F7F2'
SCHEMAS={'oncoprint':['sample','gene','alteration','cohort'],'spatial':['spot','x','y','cell_type','expression'],'phylogeny':['node','parent','label','length','group','value'],'circos':['kind','chrom','start','end','value','target','target_start','target_end','label'],'sashimi':['kind','sample','start','end','value','label']}
NUMERIC={'oncoprint':[],'spatial':[1,2,4],'phylogeny':[3,5],'circos':[2,3,4,6,7],'sashimi':[2,3,4]}
CMAP=LinearSegmentedColormap.from_list('iris_expression',['#F4E7DF',COLORS[0]])


def unique(values):
    return list(dict.fromkeys(values))


def tree_structure(rows):
    nodes={r[0]:dict(id=r[0],parent=r[1],label=r[2],length=r[3],group=r[4],value=r[5],children=[]) for r in rows}
    roots=[n for n in nodes.values() if not n['parent']]
    if len(nodes)!=len(rows) or len(roots)!=1 or roots[0]['length']!=0:
        raise ValueError('Use unique nodes and one zero-length root.')
    for node in nodes.values():
        if node['parent']:
            if node['parent'] not in nodes or node['parent']==node['id']:
                raise ValueError('Unknown/self parent.')
            nodes[node['parent']]['children'].append(node)
        seen=set(); cursor=node
        while cursor['parent']:
            if cursor['id'] in seen:
                raise ValueError('Cycle in tree.')
            seen.add(cursor['id']); cursor=nodes[cursor['parent']]
    leaves=[]
    def walk(node,distance):
        node['distance']=distance+node['length']
        if not node['children']:
            node['index']=len(leaves);leaves.append(node)
        else:
            for child in node['children']:
                walk(child,node['distance'])
            node['index']=np.mean([c['index'] for c in node['children']])
    walk(roots[0],0)
    if len(leaves)<2 or len(leaves)>64 or any(not n['label'] for n in leaves):
        raise ValueError('Use 2–64 named leaves.')
    if len(unique(n['label'] for n in leaves))!=len(leaves):
        raise ValueError('Duplicate leaf labels.')
    return nodes,leaves


def validate(rows,kind):
    if not 2<=len(rows)<=12000 or any(len(r)!=len(SCHEMAS[kind]) for r in rows):
        raise ValueError('Invalid table dimensions.')
    for row in rows:
        for j,v in enumerate(row):
            if j in NUMERIC[kind]:
                if v is None and ((kind=='phylogeny' and j==5) or (kind=='circos' and j in (6,7))):
                    continue
                if v is None or not math.isfinite(v) or abs(v)>1e12:
                    raise ValueError('Expected finite numeric value.')
            elif not isinstance(v,str) or len(v)>80 or any(ord(c)<32 for c in v):
                raise ValueError('Invalid text identifier.')
    if kind=='oncoprint':
        calls=defaultdict(list); cohorts=defaultdict(set)
        for sample,gene,alt,cohort in rows:
            if not sample or not gene or not cohort or alt not in ('WT','NA','missense','truncating','amplification','deletion'):
                raise ValueError('Invalid call.')
            calls[sample,gene].append(alt);cohorts[sample].add(cohort)
        samples=unique(r[0] for r in rows);genes=unique(r[1] for r in rows)
        if not 2<=len(samples)<=64 or not 2<=len(genes)<=20 or any(len(c)!=1 for c in cohorts.values()):
            raise ValueError('Invalid sample/gene dimensions or inconsistent cohort.')
        for s in samples:
            for g in genes:
                values=calls[s,g]
                if not values or len(set(values))!=len(values) or (len(values)>1 and any(a in ('WT','NA') for a in values)):
                    raise ValueError('Every pair needs explicit non-conflicting calls; no duplicate events.')
    elif kind=='spatial':
        if len(unique(r[0] for r in rows))!=len(rows) or any(not r[0] or not r[3] or r[4]<0 for r in rows) or len(unique(r[3] for r in rows))>8 or len(rows)>3000:
            raise ValueError('Invalid spot IDs/types/expression.')
    elif kind=='phylogeny':
        if any(not r[0] or r[3]<0 or (r[5] is not None and r[5]<0) for r in rows):
            raise ValueError('Invalid branch lengths or annotation values.')
        tree_structure(rows)
    elif kind=='circos':
        chromosomes=[r for r in rows if r[0]=='chromosome']; lengths={r[1]:r[3] for r in chromosomes}
        if not 2<=len(chromosomes)<=12 or len(lengths)!=len(chromosomes) or any(r[2]!=0 for r in chromosomes):
            raise ValueError('Declare 2–12 distinct chromosomes beginning at zero.')
        for r in rows:
            if r[0] not in ('chromosome','gc','density','link') or r[1] not in lengths or not 0<=r[2]<r[3]<=lengths[r[1]] or r[4]<0:
                raise ValueError('Invalid genomic interval/value.')
            if any(v!=int(v) for v in r[2:4]) or (r[0]=='gc' and r[4]>1):
                raise ValueError('Use integer bp and GC fractions in [0,1].')
            if r[0]=='link':
                if r[5] not in lengths or r[6] is None or r[7] is None or not 0<=r[6]<r[7]<=lengths[r[5]] or r[6]!=int(r[6]) or r[7]!=int(r[7]):
                    raise ValueError('Invalid target interval.')
            elif r[5] or r[6] not in (0,None) or r[7] not in (0,None):
                raise ValueError('Only links use target fields.')
        if len({tuple(r[:8]) for r in rows})!=len(rows):raise ValueError('Duplicate genomic rows.')
        for typ in ('gc','density'):
            for chrom in lengths:
                ordered=sorted((r for r in rows if r[0]==typ and r[1]==chrom),key=lambda r:r[2])
                if any(a[3]>b[2] for a,b in zip(ordered,ordered[1:])):
                    raise ValueError('Track windows overlap.')
    elif kind=='sashimi':
        for r in rows:
            if r[0] not in ('exon','coverage','junction') or not r[1] or not 0<=r[2]<r[3] or r[2]!=int(r[2]) or r[3]!=int(r[3]) or r[4]<0:
                raise ValueError('Invalid splice/coverage interval.')
            if r[0]=='junction' and r[4]!=int(r[4]):
                raise ValueError('Junction counts must be integers.')
        samples=unique(r[1] for r in rows if r[0]!='exon')
        junctions=unique((r[2],r[3]) for r in rows if r[0]=='junction')
        if not 1<=len(samples)<=4 or not 1<=len(junctions)<=10 or len([r for r in rows if r[0]=='exon'])<2:
            raise ValueError('Use 1–4 samples, 1–10 junctions, and at least two exons.')
        if len({tuple(r[:4]) for r in rows})!=len(rows):raise ValueError('Duplicate splice rows.')
        if len(unique(r[1] for r in rows if r[0]=='exon'))!=1:raise ValueError('Use one exon annotation per region.')
        for sample in samples:
            for start,end in junctions:
                if not any(r[0]=='junction' and r[1]==sample and r[2]==start and r[3]==end for r in rows):raise ValueError('Each sample–junction pair needs an explicit count.')
            ordered=sorted((r for r in rows if r[0]=='coverage' and r[1]==sample),key=lambda r:r[2])
            if any(a[3]>b[2] for a,b in zip(ordered,ordered[1:])):
                raise ValueError('Coverage windows overlap.')
    return rows


def read_table(path,kind):
    with Path(path).open(newline='',encoding='utf-8-sig') as handle:
        records=list(csv.reader(handle))
    if not records or records[0]!=SCHEMAS[kind]:
        raise ValueError('Expected columns: '+','.join(SCHEMAS[kind]))
    rows=[]
    for record in records[1:]:
        if not record:continue
        rows.append([None if not v.strip() else float(v) if j in NUMERIC[kind] else v.strip()
                     for j,v in enumerate(record)])
        # Blank categorical fields (root parent / absent annotation) stay empty strings.
        rows[-1]=['' if v is None and j not in NUMERIC[kind] else v for j,v in enumerate(rows[-1])]
    return validate(rows,kind)


def oncoprint(fig,rows):
    samples=unique(r[0] for r in rows);genes=unique(r[1] for r in rows);cohorts=unique(r[3] for r in rows)
    calls={(s,g):[r[2] for r in rows if r[0]==s and r[1]==g] for s in samples for g in genes}
    altered=lambda s,g:any(v not in ('WT','NA') for v in calls[s,g])
    burden=lambda s:sum(altered(s,g) for g in genes)
    samples.sort(key=lambda s:(-burden(s),s))
    gs=fig.add_gridspec(3,2,width_ratios=[3,1],height_ratios=[.65,3,.4],hspace=.12,wspace=.24)
    ax=fig.add_subplot(gs[1,0]);top=fig.add_subplot(gs[0,0],sharex=ax);side=fig.add_subplot(gs[1,1],sharey=ax)
    cmap=dict(zip(['missense','truncating','amplification','deletion','WT','NA'],COLORS[:4]+['#ECE8EF','#FFFFFF']))
    for i,s in enumerate(samples):
        for j,g in enumerate(genes):
            values=calls[s,g]
            for k,a in enumerate(values):
                ax.add_patch(Rectangle((i+.06,j+.06+k*.88/len(values)),.88,.88/len(values),fc=cmap[a],ec='#D8D2DE',lw=.3,hatch='//' if a=='NA' else None))
    ax.set(xlim=(0,len(samples)),ylim=(len(genes),0),yticks=np.arange(len(genes))+.5,yticklabels=genes,xticks=np.arange(len(samples))+.5,xticklabels=samples)
    ax.tick_params(axis='x',labelrotation=90,labelsize=6)
    top.bar(np.arange(len(samples))+.5,[burden(s) for s in samples],width=.85,color=COLORS[0]);top.set(ylabel='Altered genes');top.tick_params(labelbottom=False)
    for i,s in enumerate(samples):
        c=next(r[3] for r in rows if r[0]==s);top.scatter(i+.5,-.45,c=COLORS[cohorts.index(c)%8],s=20,marker='s',clip_on=False)
    freq=[]
    for g in genes:
        assayed=[s for s in samples if 'NA' not in calls[s,g]]
        freq.append(sum(altered(s,g) for s in assayed)/len(assayed)*100 if assayed else np.nan)
    side.barh(np.arange(len(genes))+.5,freq,color=COLORS[1]);side.set(xlabel='Altered / assayed (%)');side.tick_params(labelleft=False)
    if all(np.isnan(v) for v in freq):side.set_xlim(0,100)
    for j,v in enumerate(freq):
        if np.isnan(v):side.text(1,j+.5,'not assayed',va='center',fontsize=7)
    legend=fig.add_subplot(gs[2,:]);legend.axis('off')
    for i,c in enumerate(cohorts):
        top.text(i/max(len(cohorts),1),1.06,c,transform=top.transAxes,color=COLORS[i%8],fontsize=8)
    for i,(a,c) in enumerate(cmap.items()):
        legend.add_patch(Rectangle((i/6,.4),.018,.25,transform=legend.transAxes,fc=c,ec='#CCC'));legend.text(i/6+.025,.4,a,transform=legend.transAxes,fontsize=8)


def spatial(fig,rows,image=None):
    gs=fig.add_gridspec(2,2,width_ratios=[1.5,1],hspace=.35,wspace=.25)
    groups=unique(r[3] for r in rows);xy=np.array([[r[1],r[2]] for r in rows]);values=np.array([r[4] for r in rows])
    for mode,position in [('type',gs[:,0]),('expression',gs[0,1])]:
        ax=fig.add_subplot(position)
        if image:
            img=plt.imread(image);h,w=img.shape[:2]
            if np.any(xy<0) or np.any(xy[:,0]>w) or np.any(xy[:,1]>h):raise ValueError('Coordinates outside tissue image.')
            ax.imshow(img,extent=[0,w,h,0],alpha=.7)
        scatter=ax.scatter(xy[:,0],xy[:,1],c=[COLORS[groups.index(r[3])%8] for r in rows] if mode=='type' else values,s=10,alpha=.8,cmap=CMAP if mode!='type' else None)
        ax.set_aspect('equal');
        if not image:ax.invert_yaxis()
        ax.set_title('Cell types' if mode=='type' else 'Supplied expression',loc='left');ax.set(xlabel='Spatial x',ylabel='Spatial y')
        if mode=='expression':fig.colorbar(scatter,ax=ax,shrink=.7,label='Expression')
    ax=fig.add_subplot(gs[1,1]);ax.barh(groups,[sum(r[3]==g for r in rows) for g in groups],color=COLORS[:len(groups)]);ax.set_xlabel('Spots')


def phylogeny(fig,rows):
    nodes,leaves=tree_structure(rows);groups=unique(n['group'] for n in leaves if n['group']);maximum=max(n['distance'] for n in leaves) or 1
    gs=fig.add_gridspec(2,2,width_ratios=[1.7,1],hspace=.35,wspace=.3);ax=fig.add_subplot(gs[:,0],projection='polar')
    theta=lambda n:2*np.pi*(n['index']+.5)/len(leaves)
    for n in nodes.values():
        if not n['parent']:continue
        parent=nodes[n['parent']];t=theta(n);a=theta(parent)
        ts=np.linspace(a,t,32);ax.plot(ts,np.full(32,parent['distance']),c='#82758E',lw=.8);ax.plot([t,t],[parent['distance'],n['distance']],c='#82758E',lw=.8)
    maxvalue=max((n['value'] or 0 for n in leaves),default=1) or 1
    for n in leaves:
        t=theta(n);ax.plot([t,t],[n['distance'],maximum*1.04],c='#D6D0DD',lw=.4,ls=':')
        ax.scatter(t,maximum*1.08,c=COLORS[groups.index(n['group'])%8] if n['group'] else '#DDD7E3',s=15)
        ax.scatter(t,maximum*1.16,c=[CMAP(n['value']/maxvalue) if n['value'] is not None else (.9,.88,.92,1)],s=15)
        ax.text(t,maximum*1.29,n['label'],ha='center',va='center',fontsize=6)
    ax.set(ylim=(0,maximum*1.5),xticks=[],yticks=[]);ax.spines['polar'].set_visible(False);ax.set_title('Branch-length phylogram + annotations',loc='left')
    known=[n for n in leaves if n['value'] is not None];right=fig.add_subplot(gs[0,1]);right.scatter([n['distance'] for n in known],[n['value'] for n in known],c=COLORS[0]);right.set(xlabel='Root distance',ylabel='Annotation value')
    if not known:right.text(.5,.5,'No numeric annotations',transform=right.transAxes,ha='center')
    lower=fig.add_subplot(gs[1,1]);labels=groups+(['Unannotated'] if any(not n['group'] for n in leaves) else []);lower.barh(labels,[sum((n['group'] or 'Unannotated')==g for n in leaves) for g in labels],color=COLORS[:len(labels)]);lower.set_xlabel('Leaves')


def circos(fig,rows):
    chromosomes=[r for r in rows if r[0]=='chromosome'];total=sum(r[3] for r in chromosomes);gap=.04;span=2*np.pi-gap*len(chromosomes);positions={};cursor=np.pi/2
    gs=fig.add_gridspec(2,2,width_ratios=[1.65,1],wspace=.25,hspace=.3);ax=fig.add_subplot(gs[:,0]);maxden=max([r[4] for r in rows if r[0]=='density']+[1])
    for i,r in enumerate(chromosomes):
        end=cursor+r[3]/total*span;positions[r[1]]=(cursor,end,r[3],i);ax.add_patch(Wedge((0,0),1,np.degrees(cursor),np.degrees(end),width=.045,fc=COLORS[i%8]));t=(cursor+end)/2;ax.text(1.12*np.cos(t),1.12*np.sin(t),r[1],ha='center',va='center',fontsize=8);cursor=end+gap
    angle=lambda chrom,pos:positions[chrom][0]+pos/positions[chrom][2]*(positions[chrom][1]-positions[chrom][0])
    for r in rows:
        if r[0] in ('gc','density'):
            base=.7 if r[0]=='gc' else .83;v=r[4] if r[0]=='gc' else r[4]/maxden
            ax.add_patch(Wedge((0,0),base+.08,np.degrees(angle(r[1],r[2])),np.degrees(angle(r[1],r[3])),width=.08,fc='#EAE6EE'))
            ax.add_patch(Wedge((0,0),base+v*.08,np.degrees(angle(r[1],r[2])),np.degrees(angle(r[1],r[3])),width=v*.08,fc=COLORS[3 if r[0]=='gc' else 1],alpha=.8))
        elif r[0]=='link':
            angles=[angle(r[1],r[2]),angle(r[1],r[3]),angle(r[5],r[7]),angle(r[5],r[6])]
            points=[(.64*np.cos(t),.64*np.sin(t)) for t in angles]
            vertices=[points[0],points[1],(0,0),points[2],points[3],(0,0),points[0],points[0]]
            codes=[MPath.MOVETO,MPath.LINETO,MPath.CURVE3,MPath.CURVE3,MPath.LINETO,MPath.CURVE3,MPath.CURVE3,MPath.CLOSEPOLY]
            ax.add_patch(PathPatch(MPath(vertices,codes),fc=COLORS[positions[r[1]][3]%8],ec='none',alpha=.24))
    ax.set(xlim=(-1.25,1.25),ylim=(-1.25,1.25),aspect='equal');ax.axis('off');ax.set_title('Chromosome / density / GC / interval links',loc='left')
    gc=[];weights=[]
    for c in chromosomes:
        track=[r for r in rows if r[0]=='gc' and r[1]==c[1]]
        gc.append(sum(r[4]*(r[3]-r[2]) for r in track)/sum(r[3]-r[2] for r in track) if track else np.nan)
        weights.append(sum(r[4] for r in rows if r[0]=='link' and r[1]==c[1]))
    names=[r[1] for r in chromosomes];a=fig.add_subplot(gs[0,1]);a.barh(names,gc,color=COLORS[:len(names)]);a.set(xlim=(0,1),xlabel='Length-weighted GC fraction')
    a=fig.add_subplot(gs[1,1]);a.barh(names,weights,color=COLORS[:len(names)]);a.set_xlabel('Supplied link weights by source')


def sashimi(fig,rows):
    samples=unique(r[1] for r in rows if r[0]!='exon');exons=[r for r in rows if r[0]=='exon'];junctions=unique((r[2],r[3]) for r in rows if r[0]=='junction');lo=min(r[2] for r in rows);hi=max(r[3] for r in rows)
    gs=fig.add_gridspec(len(samples)+1,2,width_ratios=[2.5,1],height_ratios=[1]*len(samples)+[.35],wspace=.25,hspace=.2);maxcov=max([r[4] for r in rows if r[0]=='coverage']+[1]);maxcount=max([r[4] for r in rows if r[0]=='junction']+[1])
    for i,s in enumerate(samples):
        ax=fig.add_subplot(gs[i,0]);color=COLORS[i]
        for r in rows:
            if r[1]!=s:continue
            if r[0]=='coverage':ax.bar(r[2],r[4]/maxcov,width=r[3]-r[2],align='edge',color=color,alpha=.4)
            elif r[0]=='junction':
                h=1.3+(r[3]-r[2])/(hi-lo);vertices=[(r[2],.45),((r[2]+r[3])/2,h),(r[3],.45)];ax.add_patch(PathPatch(MPath(vertices,[MPath.MOVETO,MPath.CURVE3,MPath.CURVE3]),fill=False,ec=color,lw=.7+2*math.sqrt(r[4]/maxcount)));ax.text((r[2]+r[3])/2,(h+.45)/2,str(int(r[4])),ha='center',fontsize=7,color=color)
        ax.set(xlim=(lo,hi),ylim=(0,2.2),yticks=[],ylabel=s);ax.tick_params(labelbottom=False)
    annotation=fig.add_subplot(gs[-1,0]);annotation.hlines(.5,lo,hi,color='#77808B',lw=.7)
    for r in exons:annotation.add_patch(Rectangle((r[2],.3),r[3]-r[2],.4,fc='#333F49'))
    annotation.set(xlim=(lo,hi),ylim=(0,1),yticks=[],xlabel='Genomic coordinate (bp)')
    a=fig.add_subplot(gs[:,1]);matrix=np.array([[sum(r[4] for r in rows if r[0]=='junction' and r[1]==s and (r[2],r[3])==j) for s in samples] for j in junctions]);im=a.imshow(matrix,aspect='auto',cmap=CMAP,vmin=0,vmax=maxcount)
    a.set(xticks=range(len(samples)),xticklabels=samples,yticks=range(len(junctions)),yticklabels=[f'{int(s)}→{int(e)}' for s,e in junctions],title='Junction-support counts');a.tick_params(axis='x',rotation=45);fig.colorbar(im,ax=a,shrink=.6)


def render(rows,kind,out,image=None,provenance='User-supplied table'):
    validate(rows,kind)
    plt.rcParams.update({'font.size':9,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#C5C9CE','text.color':'#333F49'})
    fig=plt.figure(figsize=(11.6,6.8),facecolor=PAPER,layout='constrained')
    if kind=='spatial':spatial(fig,rows,image)
    else:globals()[kind](fig,rows)
    fig.supxlabel(provenance+' · descriptive views; no biological inference or hypothesis tests',fontsize=8)
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    for extension in ('png','svg','pdf'):fig.savefig(out.with_suffix('.'+extension),dpi=180)
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind',required=True,choices=list(SCHEMAS))
    source=parser.add_mutually_exclusive_group(required=True);source.add_argument('--csv',type=Path);source.add_argument('--demo',action='store_true')
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--image',type=Path)
    args=parser.parse_args();path=Path(__file__).resolve().parents[1]/'assets/bioinformatics'/f'{args.kind}.csv' if args.demo else args.csv
    render(read_table(path,args.kind),args.kind,args.out,args.image,'Synthetic biological fixture' if args.demo else 'User-supplied table')
