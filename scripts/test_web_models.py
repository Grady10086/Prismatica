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
for name,obj in [('models','Models'),('charts','Charts'),('hero','Hero')]:
    raw=(ROOT/'site'/f'{name}.js').read_text()
    exported=re.findall(r'export (?:const|function) (\w+)',raw)
    imported=re.search(r'import \{([^}]+)\}',raw)
    prefix='const {'+imported[1]+'}=Models;' if imported else ''
    source=re.sub(r'^import .*?;\n','',raw,flags=re.M)
    source=re.sub(r'\bexport\s+','',source)
    ctx.eval('globalThis.'+obj+'=(()=>{'+prefix+source+';return {'+','.join(exported)+'}})()')

def js(source):
    return json.loads(ctx.eval('JSON.stringify((()=>{'+source+'})())'))

for script in (ROOT/'site').glob('*.js'):
    source=re.sub(r'^import .*?;\n','',script.read_text(),flags=re.M)
    source=re.sub(r'\bexport\s+','',source)
    ctx.eval('(function(){'+source+'})')

count=0
for index in range(15):
    for variant in ['default','min','max']:
        result=js(f"""const study=Models.studies[{index}],p=Models.defaults(study.family);
        for(const c of Models.controls(study.family)){{if(!c.options&&'{variant}'!=='default')p[c.key]=c['{variant}'];}}
        const rows=Models.generate(study,p,1107);Models.validate(rows,study.family);
        const result=Charts.render(study,rows,p,Models.palettes.mineral);
        if(/NaN|Infinity/.test(result.svg))throw Error('non-finite SVG: '+study.id);
        return {{id:study.id,svg:result.svg,metrics:result.metrics}};""")
        ET.fromstring(result['svg'])
        assert len(result['metrics'])==4
        count+=1

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

# No broken local links/assets in the static entrypoint or module graph.
html=(ROOT/'site/index.html').read_text()
for url in re.findall(r'(?:src|href)="([^\"]+)"',html):
    if url.startswith('./'):assert (ROOT/'site'/url[2:]).exists(),url
for p in (ROOT/'site').glob('*.js'):
    for target in re.findall(r"from '(\./[^']+)'",p.read_text()):assert (p.parent/target).exists(),target
print(f'{count} study/boundary renders passed; deterministic data, schema validation, retrieval, paired effects, analytic gradients, solver convergence and Möbius seam continuity verified.')
