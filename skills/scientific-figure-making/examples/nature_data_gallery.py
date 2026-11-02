"""Nature-informed data figures from explicit demo data or a local data JSON.

Outputs editable SVG, PNG, captions, input data and computed summaries. No model
runs, borrowed results, invented significance tests or automatic curve smoothing.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'scripts'))
import nature_profile as nature
import nature_charts as charts


def demo_data():
    rng=np.random.default_rng(20261027)
    names=['Ours','Base A','Base B'];means=[86,81,77]
    groups={n:rng.normal(mu,1.5,8).tolist() for n,mu in zip(names,means)}
    steps=np.linspace(0,100,31)
    runs={}
    for n,mu in zip(names,means):
        runs[n]=[(52+(mu-52)*(1-np.exp(-steps/19))+rng.normal(0,.75,len(steps))).tolist() for _ in range(8)]
    raw={n:rng.normal(mu,3.0,24).tolist() for n,mu in zip(names,means)}
    before=rng.normal(78,3,16);after=before+rng.normal(3.5,2,16)
    full=rng.normal(np.array([80,83,86,81])[:,None],1,(4,8))
    delta=np.array([[-1.5,-2.3,-3.0,-.8],[-3.4,-1.2,-2.6,-3.8],[.4,-1.0,-.7,-1.9]])
    variants=full[None,:,:]+delta[:,:,None]+rng.normal(0,.35,(3,4,8))
    variant_list=variants.tolist();variant_list[2][3]=[None]*8
    return {'kind':'SYNTHETIC DEMONSTRATION','roles':{'Ours':0,'Base A':1,'Base B':2,'Base C':3,
               'Ours-S':0,'Ours-M':0,'Ours-L':0},
       'comparison':{'unit':'independent synthetic run','groups':groups},
       'training':{'unit':'independent synthetic run','steps':steps.tolist(),'runs':runs},
       'distribution':{'unit':'synthetic evaluation case','groups':raw},
       'paired':{'unit':'matched synthetic evaluation case','names':['Base A','Ours'],
          'records':[{'id':f'case-{i+1:02}','before':float(u),'after':float(v)} for i,(u,v) in enumerate(zip(before,after))]},
       'ablation':{'unit':'matched synthetic run','replicate_ids':[f'run-{i+1}' for i in range(8)],
          'rows':['Without A','Without B','Without C'],'columns':['Set 1','Set 2','Set 3','Set 4'],
          'full_runs':full.tolist(),'variant_runs':variant_list,'vlim':5},
       'pareto':{'names':['Ours-S','Ours-M','Ours-L','Base A','Base B','Base C'],
          'latency':[11,24,45,36,59,73],'score':[78,84,87,82,85,79]}}


def load_colors(out,path):
    if path is None:
        sys.path.insert(0,str(HERE.parents[1]/'paper-colors'/'scripts'))
        import exporters,themes
        fixtures=HERE.parents[1]/'paper-colors'/'tests'/'fixtures'
        loaded,_=themes.load_all(fixtures/'palettes.json',fixtures/'swatches.json')
        theme=loaded['fixture'];path=out/'paper_colors.py'
        path.write_text(exporters.export_python(theme,themes.series_stats(theme)))
    spec=importlib.util.spec_from_file_location('nature_gallery_colors',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def validate(data):
    if data.get('kind') not in {'SYNTHETIC DEMONSTRATION','PROJECT DATA'}:
        raise ValueError('Declare SYNTHETIC DEMONSTRATION or PROJECT DATA')
    for section in ['comparison','training','distribution','paired','ablation']:
        if not data[section].get('unit'):raise ValueError(f'Declare observational unit for {section}')
    p=data['paired'];ids=[r['id'] for r in p['records']]
    if len(set(ids))!=len(ids):raise ValueError('Paired unit IDs must be unique')
    before=charts.observations([r['before'] for r in p['records']])
    after=charts.observations([r['after'] for r in p['records']])
    if len(p['names'])!=2:raise ValueError('Two paired condition names are required')
    a=data['ablation'];full=np.asarray(a['full_runs'],float);variant=np.asarray(a['variant_runs'],float)
    if full.ndim!=2 or full.shape[1]<2 or not np.isfinite(full).all():raise ValueError('Full-model runs must be finite [dataset, run >= 2]')
    if variant.shape!=(len(a['rows']),len(a['columns']),full.shape[1]) or full.shape[0]!=len(a['columns']):raise ValueError('Ablations must use matched datasets and run IDs')
    if len(a['replicate_ids'])!=full.shape[1] or len(set(a['replicate_ids']))!=full.shape[1]:raise ValueError('Each ablation replicate needs a unique matching ID')
    if np.isinf(variant).any():raise ValueError('Ablations cannot contain infinity')
    # This gallery's labels declare percentages; other units use the primitives.
    scores=[before,after,full,variant[np.isfinite(variant)],np.asarray(data['pareto']['score'],float)]
    for name in ['comparison','distribution']:
        scores.extend(charts.observations(v) for v in data[name]['groups'].values())
    scores.extend(np.asarray(v,float) for v in data['training']['runs'].values())
    if any(not np.isfinite(a).all() or np.any((a<0)|(a>100)) for a in scores):
        raise ValueError('This gallery expects finite percentage scores in [0,100]; use primitives for other units')
    return before,after,variant-full[None,:,:]


def render(data,colors,out):
    before,after,deltas=validate(data)
    nature.apply();colors.apply()
    styles={name:colors.style(role,redundant=True) for name,role in data['roles'].items()}
    synthetic=data['kind']=='SYNTHETIC DEMONSTRATION'
    footer='Synthetic data · layout example' if synthetic else 'Project data · see source and statistical definitions'
    captions={};summaries={}
    counts={name:len(v) for name,v in data['comparison']['groups'].items()}
    unit=data['comparison']['unit']
    captions['comparison']=f"Raw observations and means ± sample SD (ddof=1); not SEM or confidence intervals. Observational unit: {unit}; n={counts}. Supplied method order retained."
    unit=data['training']['unit'];run_counts={name:len(v) for name,v in data['training']['runs'].items()}
    captions['training']=f"Thin lines: unsmoothed individual runs. Main line and band: pointwise mean ± sample SD across runs; not confidence or prediction intervals. Unit: {unit}; n={run_counts}. All methods share the same observed steps."
    n_cells=np.isfinite(deltas).sum(axis=2).tolist()
    captions['ablation']=f"Paired variant-minus-full score differences in percentage points; means across matched run IDs, per-cell n={n_cells}. NA denotes unmeasured cells, not zero. Shared symmetric color scale. Unit: {data['ablation']['unit']}."
    distribution_counts={name:len(v) for name,v in data['distribution']['groups'].items()}
    captions['distribution']=f"All observations shown. Boxes: median and 25th–75th percentiles; whiskers: most extreme observations within 1.5 IQR. Dots include outliers. Violin is a descriptive KDE when n ≥ 10; not uncertainty. Horizontal jitter changes display position only. Unit: {data['distribution']['unit']}; n={distribution_counts}."
    captions['paired']=f"Each line connects the same unit under both conditions; n={len(before)} matched pairs. Pairing uses explicit IDs. No significance test or causal claim is inferred. Unit: {data['paired']['unit']}."
    captions['pareto']='Each point is one operating point. Dominance minimizes latency and maximizes score. Dashed segments link observed non-dominated points as a visual guide, not measured interpolation or a confidence statement. Latencies must share a hardware/workload protocol.'

    def draw(name,ax,fig):
        if name=='comparison':
            summary=charts.comparison(ax,data['comparison']['groups'],styles)
        elif name=='training':
            s=data['training'];summary=charts.training(ax,s['steps'],s['runs'],styles)
        elif name=='ablation':
            s=data['ablation'];im,summary=charts.ablation(ax,deltas,s['rows'],s['columns'],cmap=colors.cmap('diverging'),vlim=s['vlim'])
            fig.colorbar(im,ax=ax,label='Δ score (pp)',ticks=[-s['vlim'],0,s['vlim']],shrink=.85,pad=.04)
            ax.set(xlabel='Evaluation dataset')
        elif name=='distribution':
            summary=charts.distribution(ax,data['distribution']['groups'],styles)
        elif name=='paired':
            summary=charts.paired(ax,before,after,names=data['paired']['names'],styles=styles)
        else:
            s=data['pareto'];summary=charts.pareto(ax,s['latency'],s['score'],s['names'],styles,
              offsets=[(4,-7),(4,-8),(4,4),(4,-9),(4,4),(-25,4)] if synthetic else None)
        summaries[name]=summary

    for name in captions:
        fig,ax=plt.subplots(figsize=nature.figure_size('single',height_mm=68),layout='constrained')
        draw(name,ax,fig);fig.supxlabel(footer,fontsize=5.5)
        with matplotlib.rc_context({'savefig.bbox':None}):
            fig.savefig(out/(name+'.svg'));fig.savefig(out/(name+'.png'),dpi=450)
        plt.close(fig)
    # Composite follows an evidence progression; panel sizes remain readable.
    fig,axes=plt.subplots(2,3,figsize=nature.figure_size('double',height_mm=140),layout='constrained')
    for ax,name in zip(axes.flat,captions):draw(name,ax,fig)
    nature.label_panels(axes.flat,y=1.035)
    fig.supxlabel(footer+' · SD, distributions, paired units and observed trade-offs',fontsize=5.5)
    with matplotlib.rc_context({'savefig.bbox':None}):
        fig.savefig(out/'nature-data-overview.svg');fig.savefig(out/'nature-data-overview.png',dpi=450)
    plt.close(fig)
    prefix='SYNTHETIC DEMONSTRATION ONLY. ' if synthetic else 'PROJECT DATA. '
    (out/'captions.txt').write_text('Composite: a comparison; b training; c ablation; d distribution; e paired; f Pareto.\n\n'+'\n\n'.join(name+'\n'+prefix+caption for name,caption in captions.items())+'\n')
    def clean(value):
        if isinstance(value,float) and not np.isfinite(value):return None
        if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
        if isinstance(value,list):return [clean(v) for v in value]
        return value
    (out/'computed-summaries.json').write_text(json.dumps(clean(summaries),indent=2,allow_nan=False)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    mode=p.add_mutually_exclusive_group(required=True);mode.add_argument('--demo',action='store_true');mode.add_argument('--data',type=Path)
    p.add_argument('--colors',type=Path,help='Existing paper-colors Python export; otherwise use synthetic fixture palette')
    args=p.parse_args();data=demo_data() if args.demo else json.loads(args.data.read_text())
    validate(data);args.out.mkdir(parents=True,exist_ok=True)
    colors=load_colors(args.out,args.colors)
    render(data,colors,args.out)
    (args.out/'input-data.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print('Wrote six data figures, a composite, editable SVG, PNG, captions and source data:',args.out)


if __name__=='__main__':main()
