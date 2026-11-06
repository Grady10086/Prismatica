// Small, interruptible transitions. Canonical figure data remains outside animation state.
const NUMBER = /[-+]?(?:\d*\.)?\d+(?:e[-+]?\d+)?/gi;
export const easing = t => 1 - (1 - t) ** 3;
export function numberInterpolator(a, b) {
  if (a === null || b === null || a.trim() === '' || b.trim() === '') return null;
  const x = Number(a), y = Number(b);
  if (!Number.isFinite(x) || !Number.isFinite(y) || x === y) return null;
  return t => t === 1 ? b : String(x + (y - x) * t);
}
export function pathInterpolator(a, b) {
  if (!a || !b || a === b) return null;
  const aa = a.match(NUMBER), bb = b.match(NUMBER);
  if (!aa || !bb || aa.length !== bb.length || a.replace(NUMBER, '#') !== b.replace(NUMBER, '#')) return null;
  const start = aa.map(Number), end = bb.map(Number);
  if ([...start, ...end].some(x => !Number.isFinite(x))) return null;
  return t => {
    if (t === 1) return b;
    let i = 0;
    return b.replace(NUMBER, () => { const value = start[i] + (end[i] - start[i]) * t; i++; return value.toFixed(3); });
  };
}
function rgb(value) {
  if (/^#[\da-f]{6}$/i.test(value || '')) return value.slice(1).match(/../g).map(v => parseInt(v, 16));
  const match = /^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/.exec(value || '');
  return match ? match.slice(1).map(Number) : null;
}
export function colorInterpolator(a, b) {
  const aa = rgb(a), bb = rgb(b);
  if (!aa || !bb || a === b) return null;
  return t => t === 1 ? b : `rgb(${aa.map((v, i) => Math.round(v + (bb[i] - v) * t)).join(',')})`;
}
export function motionAllowed() {
  return !matchMedia('(prefers-reduced-motion: reduce)').matches && !document.body.classList.contains('no-motion');
}
const NUMERIC = new Set(['cx','cy','x','y','r','width','height','opacity','fill-opacity','stroke-opacity','stroke-width']);
export function parseFigure(source) {
  const doc = new DOMParser().parseFromString(source, 'image/svg+xml');
  if (doc.querySelector('parsererror') || doc.documentElement.tagName !== 'svg') throw Error('Invalid figure output.');
  return document.importNode(doc.documentElement, true);
}
// Display-only color transform. Geometry, data and canonical paper exports stay exact.
export function displayColor(value) {
  const neutrals={'#f8f7f2':'#14232b','#fdfcf9':'#182a33','#dae2df':'#30444c',
    '#e2e8e6':'#293d46','#333f49':'#dce5e5','#77808b':'#b0c3ca',
    '#c5c9ce':'#6b8390','#ffffff':'#14232b','#fff':'#14232b',white:'#14232b',black:'#e4eceb'};
  const key=value.toLowerCase();if(neutrals[key])return neutrals[key];
  const a=rgb(value);if(!a)return value;
  const [r,g,b]=a.map(x=>x/255),max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min,l=(max+min)/2;
  if(d<.025){const v=Math.round((.16+.78*(1-l))*255).toString(16).padStart(2,'0');return '#'+v.repeat(3)}
  let h=max===r?((g-b)/d+6)%6:max===g?(b-r)/d+2:(r-g)/d+4;
  h/=6;const sat=Math.min(.82,d/(1-Math.abs(2*l-1))*1.06),light=.16+.78*Math.pow(1-l,.5);
  const c=(1-Math.abs(2*light-1))*sat,x=c*(1-Math.abs((h*6)%2-1)),m=light-c/2;
  const sectors=[[c,x,0],[x,c,0],[0,c,x],[0,x,c],[x,0,c],[c,0,x]];
  return '#'+sectors[Math.min(5,Math.floor(h*6))].map(v=>Math.round((v+m)*255).toString(16).padStart(2,'0')).join('');
}
// Brighten mark paint only; never resize points, widen weighted edges or alter alpha encodings.
export function luminousPaint(value,amount=.2) {
  const color=rgb(value);if(!color)return value;
  const pearl=[235,244,239];
  return '#'+color.map((v,i)=>Math.round(v+(pearl[i]-v)*amount).toString(16).padStart(2,'0')).join('');
}
export function themeFigure(source,dark=true) {
  if(!dark)return source;
  const svg=parseFigure(source);
  svg.setAttribute('data-canvas-theme','dark');
  svg.querySelectorAll('*').forEach(node=>{
    for(const name of ['fill','stroke','stop-color']){
      const color=node.getAttribute(name);
      if(!color)continue;
      let paint=displayColor(color);
      const source=rgb(color),chromatic=source&&Math.max(...source)-Math.min(...source)>18;
      const point=node.tagName==='circle'&&node.getAttribute('data-visual-role')==='point'&&name==='fill';
      const trace=node.tagName==='path'&&node.getAttribute('data-visual-role')==='trace'&&name==='stroke'&&(!node.hasAttribute('fill')||node.getAttribute('fill')==='none');
      if(chromatic&&(point||trace))paint=luminousPaint(paint,point ? .28 : .19);
      node.setAttribute(name,paint);
    }
  });
  return svg.outerHTML;
}

export function createPresenter(stage) {
  let raf = 0, tasks = [], ghosts = [], serial = 0, rootAnimation = null;
  function busy(value) { stage.dataset.transitioning = String(value); stage.setAttribute('aria-busy', String(value)); }
  function cancel(finish = false) {
    cancelAnimationFrame(raf); raf = 0;
    if (finish) tasks.forEach(task => task.node.setAttribute(task.name, task.final));
    tasks = [];
    if (rootAnimation) { rootAnimation.cancel(); rootAnimation = null; }
    ghosts.forEach(node => node.remove()); ghosts = []; busy(false);
  }
  function crossfade(old, next) {
    const ghost = old.cloneNode(true);
    const prefix = 'leaving-' + (++serial) + '-';
    const ids = new Map([...ghost.querySelectorAll('[id]')].map(e => [e.id, prefix + e.id]));
    ghost.querySelectorAll('*').forEach(e => [...e.attributes].forEach(attr => {
      let value = attr.value;
      if (attr.name === 'id') value = ids.get(value) || value;
      else for (const [id, nextId] of ids) value = value.replaceAll('url(#' + id + ')', 'url(#' + nextId + ')');
      e.setAttribute(attr.name, value);
    }));
    ghost.setAttribute('aria-hidden', 'true');
    ghost.classList.add('figure-ghost');
    stage.replaceChildren(next, ghost); ghosts.push(ghost); busy(true);
    ghost.animate([{opacity:1,transform:'translateY(0)'},{opacity:0,transform:'translateY(-5px)'}],{duration:190,easing:'cubic-bezier(.2,.7,.2,1)',fill:'forwards'}).finished.catch(()=>{}).then(()=>ghost.remove());
    rootAnimation = next.animate([{opacity:0,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],{duration:270,easing:'cubic-bezier(.16,1,.3,1)'});
    const animation = rootAnimation;
    animation.finished.catch(()=>{}).then(()=>{if(rootAnimation===animation){rootAnimation=null;busy(false)}});
  }
  function present(source, {kind='data',animate=true}={}) {
    const old = stage.querySelector('svg:not(.figure-ghost)');
    cancel();
    const next = parseFigure(source);
    if (!old || !animate || !motionAllowed() || kind === 'playback' || !stage.getClientRects().length) {
      stage.replaceChildren(next); busy(false); return;
    }
    if (kind === 'study') { crossfade(old,next); return; }
    const previous = [old,...old.querySelectorAll('*')], incoming = [next,...next.querySelectorAll('*')];
    if (previous.length !== incoming.length || previous.some((node,i)=>node.tagName!==incoming[i].tagName||node.getAttribute('data-key')!==incoming[i].getAttribute('data-key'))) {
      crossfade(old,next); return;
    }
    const plans = [], writes = [];
    previous.forEach((node,i)=>{
      const fresh=incoming[i];
      for (const attr of [...node.attributes]) if (!fresh.hasAttribute(attr.name)) writes.push(()=>node.removeAttribute(attr.name));
      for (const attr of [...fresh.attributes]) {
        const start=node.getAttribute(attr.name), end=attr.value;
        if (start===end) continue;
        let tween=null;
        if (NUMERIC.has(attr.name)) tween=numberInterpolator(start,end);
        else if (attr.name==='d') tween=pathInterpolator(start,end);
        else if (attr.name==='fill'||attr.name==='stroke') tween=colorInterpolator(start,end);
        if(tween) plans.push({node,name:attr.name,tween,final:end});
        else writes.push(()=>node.setAttribute(attr.name,end));
      }
      if(!fresh.children.length&&fresh.textContent!==node.textContent)writes.push(()=>{node.textContent=fresh.textContent});
    });
    // Dense heatmaps crossfade rather than scheduling thousands of attribute tweens.
    if(plans.length>420){crossfade(old,next);return}
    writes.forEach(write=>write());
    if(!plans.length){busy(false);return}
    tasks=plans;busy(true);
    let start=null;
    function tick(now){
      if(start===null)start=now;
      const t=Math.min(1,(now-start)/230),e=easing(t);
      tasks.forEach(task=>task.node.setAttribute(task.name,task.tween(e)));
      if(t<1&&motionAllowed())raf=requestAnimationFrame(tick);
      else {tasks.forEach(task=>task.node.setAttribute(task.name,task.final));tasks=[];raf=0;busy(false)}
    }
    raf=requestAnimationFrame(tick);
  }
  return {present,finish:()=>cancel(true),dispose:()=>cancel()};
}
export function animateMetrics(container) {
  if (!motionAllowed()) return;
  [...container.children].forEach((node,i)=>node.animate([{opacity:.35,transform:'translateY(4px)'},{opacity:1,transform:'translateY(0)'}],{duration:200,delay:i*18,easing:'cubic-bezier(.2,.8,.2,1)'}));
}
export function animateCards(container,before) {
  if(!motionAllowed())return;
  [...container.querySelectorAll('.study-card')].forEach((node,i)=>{
    const previous=before.get(node.dataset.study),next=node.getBoundingClientRect();
    if(previous){
      const dx=previous.left-next.left,dy=previous.top-next.top;
      if(Math.abs(dx)+Math.abs(dy)>1)node.animate([{transform:`translate(${dx}px,${dy}px)`},{transform:'translate(0,0)'}],{duration:320,easing:'cubic-bezier(.16,1,.3,1)'});
    }else node.animate([{opacity:0,transform:'translateY(9px)'},{opacity:1,transform:'translateY(0)'}],{duration:280,delay:Math.min(i,5)*22,easing:'cubic-bezier(.16,1,.3,1)'});
  });
}
