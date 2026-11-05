"""Headless tests of the actual browser model and SVG modules, without a Node toolchain.
Run: uv run --with quickjs python scripts/test_web_models.py
"""
from pathlib import Path
import json
import math
import re
import xml.etree.ElementTree as ET
import quickjs

ROOT=Path(__file__).resolve().parents[1]
ctx=quickjs.Context()
# QuickJS's JS standard library lacks this modern browser method.
ctx.eval('Array.prototype.at=function(i){return this[i<0?this.length+i:i]}')
for name,obj in [('bio','Bio'),('models','Models'),('charts','Charts'),('hero','Hero'),('motion','Motion')]:
    raw=(ROOT/'site'/f'{name}.js').read_text()
    exported=re.findall(r'export (?:const|function) (\w+)',raw)
    imports=re.findall(r"import \{([^}]+)\} from '(\./[^']+)'",raw,re.S)
    objects={'./bio.js':'Bio','./models.js':'Models'}
    prefix=''.join('const {'+names+'}='+objects[target]+';' for names,target in imports)
    source=re.sub(r'^import\b[\s\S]*?;\n','',raw,flags=re.M)
    source=re.sub(r'\bexport\s+','',source)
    ctx.eval('globalThis.'+obj+'=(()=>{'+prefix+source+';return {'+','.join(exported)+'}})()')

def js(source):
    return json.loads(ctx.eval('JSON.stringify((()=>{'+source+'})())'))

for script in (ROOT/'site').glob('*.js'):
    source=re.sub(r'^import\b[\s\S]*?;\n','',script.read_text(),flags=re.M)
    source=re.sub(r'\bexport\s+','',source)
    ctx.eval('(function(){'+source+'})')

count=0
study_count=js("return Models.studies.length;")
assert study_count==32
assert js("return Models.studies.filter(s=>s.category==='Bioinformatics').length===5;")
assert js("return ['Multimodal','Generative','Model analysis'].every(c=>Models.studies.filter(s=>s.category===c).length===6)&&Models.studies.filter(s=>s.category==='Statistical').length===9;")
for index in range(study_count):
    for variant in ['default','min','max']:
        result=js(f"""const study=Models.studies[{index}],p=Models.defaults(study.family);
        for(const c of Models.controls(study.family)){{if(!c.options&&'{variant}'!=='default')p[c.key]=c['{variant}'];}}
        const rows=Models.generate(study,p,1107);Models.validate(rows,study.family);
        const result=Charts.render(study,rows,p,Models.palettes.mineral);
        if(/NaN|Infinity/.test(result.svg))throw Error('non-finite SVG: '+study.id);
        return {{id:study.id,svg:result.svg,metrics:result.metrics}};""")
        figure=ET.fromstring(result['svg'])
        panels=[node for node in figure.iter() if 'data-panel-box' in node.attrib]
        assert panels, result['id']
        for panel in panels:
            x,y,w,h=map(float,panel.attrib['data-panel-box'].split())
            assert 0<=x<x+w<=1000 and 0<=y<y+h<=620
            assert panel.attrib['data-panel-label']

        assert len(result['metrics'])==4
        count+=1

# Presentation palettes must not change derived results or produce invalid vectors.
for palette in ['tide','ember']:
    for index in range(study_count):
        result=js(f"""const study=Models.studies[{index}],p=Models.defaults(study.family),rows=Models.generate(study,p,1107);
        const before=JSON.stringify(rows),reference=Charts.render(study,rows,p,Models.palettes.iris),result=Charts.render(study,rows,p,Models.palettes['{palette}']);
        if(before!==JSON.stringify(rows))throw Error('palette mutated inputs');
        if(JSON.stringify(reference.metrics)!==JSON.stringify(result.metrics))throw Error('palette changed results');
        return {{svg:result.svg}};""")
        ET.fromstring(result['svg'])
        assert not re.search(r'NaN|Infinity',result['svg'])
print('64 additional palette renders passed; source observations and derived metrics unchanged.')

assert js("const a=Models.random(12),b=Models.random(12);return Array.from({length:100},()=>a()===b()).every(Boolean);")
assert js("const s=Models.studies.find(s=>s.family==='paired'),p=Models.defaults('paired'),a=Models.generate(s,p,4),b=Models.generate(s,{...p,effect:p.effect+4},4);return a.every((r,i)=>Math.abs(b[i][3]-r[3]-4)<1e-10);")
assert js("const r=[[1,1,.9,.1],[1,2,.1,.9],[2,1,.1,.9],[2,2,.9,.1]],d=Models.retrievalData(r);return d.rank[0].every(r=>r===1)&&d.rank[1].every(r=>r===2);")
assert js("const r=[[1,0,2,4],[2,0,3,8]],text=Models.csv(r,'paired');return JSON.stringify(Models.parseCSV(text,'paired'))===JSON.stringify(r);")
assert js("const r=[[1,0,2,4],[2,0,3,8]];try{Models.parseCSV('case,group,before,after\\n1,0,,4\\n2,0,3,8','paired');return false}catch{return true}")
assert js("try{Models.validate([[1,0,2,4],[1,0,3,8]],'paired');return false}catch{return true}")
assert js("try{Models.validate([[0,1,65],[1,2,70]],'factorial');return false}catch{return true}")
assert js("try{Models.validate([[1,1,.5,.6],[2,2,.5,.6]],'retrieval');return false}catch{return true}")
assert js("try{Models.validate([[1,0,1e308,2],[2,0,3,4]],'paired');return false}catch{return true}")
# Independently check JS analytic drift against a central difference of the log marginal.
x=[.3,-.7];sigma=.8;h=1e-5
centres=[[2*math.cos(i*math.pi/4),2*math.sin(i*math.pi/4)] for i in range(8)]
def log_marginal(point):
    return math.log(sum(math.exp(-sum((point[j]-c[j])**2 for j in range(2))/(2*(sigma*sigma+.16**2))) for c in centres))
expected=[]
for j in range(2):
    plus=x.copy();minus=x.copy();plus[j]+=h;minus[j]-=h
    expected.append(-sigma*(log_marginal(plus)-log_marginal(minus))/(2*h))
actual=js('return Models.drift([.3,-.7],.8);')
assert all(abs(a-b)<1e-8 for a,b in zip(actual,expected))
assert js("const s=Models.studies[0],p=Models.defaults('diffusion'),r=Models.generate(s,p,1107),ref=Models.integrate(r,512,'Heun',3).final;const error=n=>Models.mean(Models.integrate(r,n,'Midpoint',3).final.map((x,i)=>Math.hypot(x[0]-ref[i][0],x[1]-ref[i][1])));return error(64)<error(16);")
for family in ['Euler','Heun','Midpoint']:
    result=js(f"return Models.integrate([[1,1,2],[2,-1,.3]],16,'{family}',3).path.length;")
    assert result==(17 if family=='Euler' else 9)

# A Möbius half twist must join u=2π,v to u=0,-v, including during scrolling.
assert js("for(const p of [0,.4,1.15])for(const t of [0,2,9])for(const v of [-1,-.3,0,.7,1]){const a=Hero.mobiusPoint(2*Math.PI,v,p,t),b=Hero.mobiusPoint(0,-v,p,t);if(a.some((x,i)=>Math.abs(x-b[i])>1e-12))return false}return true;")
assert js("const a=Hero.mobiusPoint(.7,.4,0,0),b=Hero.mobiusPoint(.7,.4,.9,0);return Math.hypot(...a.map((x,i)=>x-b[i]))>.01;")

# Attribute transitions end at the exact canonical strings, and never morph incompatible paths.
assert js("const f=Motion.pathInterpolator('M0,0L10,20','M4,8L20,40');return f(1)==='M4,8L20,40'&&f(.5)==='M2.000,4.000L15.000,30.000';")
assert js("return Motion.pathInterpolator('M0,0L1,1','M0,0C1,1 2,2 3,3')===null;")
assert js("const f=Motion.numberInterpolator('1','8.125');return f(1)==='8.125'&&f(0)==='1';")
assert js("return Motion.colorInterpolator('#000000','#ffffff')(.5)==='rgb(128,128,128)';")

# No broken local links/assets in the static entrypoint or module graph.
html=(ROOT/'site/index.html').read_text()
for url in re.findall(r'(?:src|href)="([^\"]+)"',html):
    if url.startswith('./'):assert (ROOT/'site'/url[2:]).exists(),url
for p in (ROOT/'site').glob('*.js'):
    for target in re.findall(r"from '(\./[^']+)'",p.read_text()):assert (p.parent/target).exists(),target

# Expanded catalog: independent numerical fixtures, not just render smoke checks.
assert js("return JSON.stringify(Models.matrixRanks([[.9,.8],[.95,.7]]))==='[1,2]'&&JSON.stringify(Models.matrixRanks(Models.transpose([[.9,.8],[.95,.7]])))==='[2,2]';")
assert js("const bb=Models.reliabilityBins([[.8,.1,.1],[.2,.7,.1]],[0,1]);return bb.reduce((s,b)=>s+b.n,0)===2&&bb.find(b=>b.bin===6).accuracy===1&&bb.find(b=>b.bin===5).accuracy===0;")
assert js("const v=Models.brierScores([[.8,.1,.1],[.2,.7,.1]]);return Math.abs(v[0]-.06)<1e-12&&Math.abs(v[1]-1.14)<1e-12;")
assert js("return Models.centres.every((c,i)=>Models.nearestMode(c)===i);")
# A valid imported performance table can contain just one budget.
for variant in ['budget','tails']:
    result=js(f"""const s=Models.studies.find(s=>s.variant==='{variant}'),p=Models.defaults(s.family),r=[];
    for(let m=0;m<3;m++)for(let seed=1;seed<=2;seed++)r.push([m,16,seed,.2+m*.05,.5+seed*.1-m*.05]);
    Models.validate(r,'performance');const out=Charts.render(s,r,p,Models.palettes.iris,{{custom:true}});
    return {{svg:out.svg,metrics:out.metrics}};""")
    assert not re.search('NaN|Infinity',result['svg'])
    ET.fromstring(result['svg'])
    assert result['metrics'][0]['value']==2

# Six-set fixtures verify exclusive vs inclusive intersections and empty-set semantics.
assert js("const d=Models.setSummary([[1,1,0,0,0,0,0],[2,0,1,0,0,0,0],[3,1,1,0,0,0,0],[4,1,1,1,1,1,1]]);return d.union===4&&d.core===1&&d.totals[0]===3&&d.unique[0]===1&&d.degree.join(',')==='2,1,0,0,0,1'&&d.shared[0][1]===2&&d.jaccard[0][1]===.5;")
assert js("const d=Models.setSummary([[1,1,0,0,0,0,0],[2,1,0,0,0,0,0]]);return d.jaccard[0][1]===0&&d.jaccard[1][2]===null;")
assert js("for(const r of [[[1,0,0,0,0,0,0],[2,1,0,0,0,0,0]],[[1,1,.5,0,0,0,0],[2,1,0,0,0,0,0]]]){try{Models.validate(r,'sets');return false}catch{}}return true;")
assert js("const s=Models.studies.find(s=>s.family==='sets'),p=Models.defaults('sets'),rows=Models.generate(s,p,1107),d=Models.setSummary(rows);return d.intersections.reduce((s,v)=>s+v.count,0)===rows.length&&d.degree.reduce((s,v)=>s+v,0)===rows.length&&d.totals.reduce((s,v)=>s+v,0)===d.degree.reduce((s,v,i)=>s+(i+1)*v,0);")

assert js("const rows=Array.from({length:63},(_,i)=>[i+1,...Array.from({length:6},(_,j)=>(i+1)>>j&1)]),d=Models.setSummary(rows);return d.totals.every(v=>v===32)&&d.unique.every(v=>v===1)&&d.core===1&&d.degree.join(',')==='6,15,20,15,6,1'&&Math.abs(d.jaccard[0][1]-1/3)<1e-12;")
for variant in ['flower','upset','similarity']:
    result=js(f"const s=Models.studies.find(s=>s.family==='sets'&&s.variant==='{variant}'),p=Models.defaults('sets');return Charts.render(s,[[1,1,0,0,0,0,0],[2,1,0,0,0,0,0]],p,Models.palettes.iris,{{custom:true}}).svg;")
    assert not re.search('NaN|Infinity',result)
    ET.fromstring(result)

# Specialized biology contracts and independent known-value fixtures.
assert js(r"""const r=Bio.bioParse('sample,gene,alteration,cohort\nP1,G1,WT,A\nP1,G2,NA,A\nP2,G1,missense,B\nP2,G2,amplification,B','oncoprint'),d=Bio.bioSummary('oncoprint',r);return d.burden('P1')===0&&d.burden('P2')===2&&d.get('P1','G2')[0]==='NA';""")
assert js(r"""const rows=Bio.parseNewick("('Leaf A':0.1,('B':0.2,C:0.3):0.4);"),d=Bio.bioSummary('phylogeny',rows);return d.leaves.length===3&&d.leaves.find(n=>n.label==='Leaf A').distance===.1&&Math.abs(d.leaves.find(n=>n.label==='C').distance-.7)<1e-12&&d.leaves.every(n=>n.value===null);""")
assert js("for(const text of ['(A,B:1);','(A:-1,B:1);','(A:1,A:2);','(A:1,B:2) trailing']){try{Bio.parseNewick(text);return false}catch{}}return true;")
assert js("const r=[['r','','',0,'',null],['a','b','A',1,'',null],['b','a','B',1,'',null]];try{Bio.bioValidate(r,'phylogeny');return false}catch{return true};")
assert js("const rows=[['chromosome','chrA',0,100,0,'',0,0,''],['chromosome','chrB',0,200,0,'',0,0,''],['gc','chrA',0,25,.2,'',0,0,''],['gc','chrA',25,100,.6,'',0,0,'']];Bio.bioValidate(rows,'circos');return Math.abs(Bio.bioSummary('circos',rows).weightedGC('chrA')-.5)<1e-12;")
assert js("const r=[['exon','G',0,10,0,'E1'],['exon','G',20,30,0,'E2'],['coverage','S',0,20,3,''],['coverage','S',10,30,4,''],['junction','S',10,20,4,'J']];try{Bio.bioValidate(r,'sashimi');return false}catch{return true};")
for family in ['oncoprint','spatial','phylogeny','circos','sashimi']:
    assert js(f"const f='{family}',p=Object.fromEntries(Bio.bioControls(f).map(c=>[c.key,c.value])),r=Bio.bioGenerate(f,p,1107);return JSON.stringify(Bio.bioParse(Bio.bioCSV(r,f),f))===JSON.stringify(r);")
# Strings with commas and escaped quotes survive the CSV codec.
assert js("const r=[['cell, \"A\"',0,0,'Type A',1],['cell2',1,1,'Type B',2]];return JSON.stringify(Bio.bioParse(Bio.bioCSV(r,'spatial'),'spatial'))===JSON.stringify(r);")
# Valid unassayed cohorts and zero-length branches render without invented numbers.
for family, fixture in [
 ('oncoprint',[['P1','G1','NA','A'],['P1','G2','NA','A'],['P2','G1','NA','B'],['P2','G2','NA','B']]),
 ('phylogeny',[['r','','',0,'',None],['a','r','A',0,'',None],['b','r','B',0,'',None]])]:
    result=js(f"const f='{family}',r={json.dumps(fixture)},s=Models.studies.find(s=>s.family===f);Bio.bioValidate(r,f);return Charts.render(s,r,Models.defaults(f),Models.palettes.iris,{{custom:true}}).svg;")
    ET.fromstring(result)
    assert not re.search('NaN|Infinity',result)

# A partial sample/junction table is missing data, not a zero-support call.
assert js("const r=[['exon','G',0,10,0,'E1'],['exon','G',20,30,0,'E2'],['junction','A',10,20,3,'J'],['coverage','B',0,10,1,'']];try{Bio.bioValidate(r,'sashimi');return false}catch{return true};")

print(f'{count} study/boundary renders passed; deterministic data, schema validation, retrieval, paired effects, analytic gradients, solver convergence and Möbius seam continuity verified.')
