import {createPresenter,parseFigure,animateMetrics,animateCards,motionAllowed} from './motion.js';
import {
  studies,
  palettes,
  controls,
  defaults,
  generate,
  csv,
  parseCSV,
  validate,
  schemas,
  simulate
} from './models.js';
import {
  render,
  diffusionExtra
} from './charts.js';
import {
  initHero
} from './hero.js';
const $ = s => document.querySelector(s),
  REPO = 'https://github.com/Grady10086/Prismatica/blob/main/';
let current = studies[0],
  seed = 1107,
  params = defaults(current.family),
  rows = [],
  palette = 'iris',
  simulation, extra, phase = 1,
  timer = null,
  custom = false,
  lang = 'en',
  filter = 'All',
  cache = new Map(),
  editOpen = false,
  renderToken = 0,
  booting = true,
  zoom = 1,
  view = {
    x: 0,
    y: 0,
    w: 1000,
    h: 620
  },
  drag = null;
const presenter = createPresenter($('#chart'));
let canonicalFigure = '', metricSignature = '', pinnedKey = null, pointerStart = null;
let panelSignature = '', cameraRAF = 0;
const panelPicker = document.createElement('select');
panelPicker.id = 'panel-picker';
panelPicker.setAttribute('aria-label', 'Focus a figure panel');
const clearSelection = document.createElement('button');
clearSelection.id = 'clear-selection';
clearSelection.textContent = 'Clear selection ×';
clearSelection.hidden = true;
$('.figure-toolbar>div').prepend(panelPicker, clearSelection);
const selectionStatus = document.createElement('span');
selectionStatus.className = 'sr-only';
selectionStatus.setAttribute('role','status');
$('.canvas-area').append(selectionStatus);
const cardCache = new Map();
const words = {
  contactNav: '联系我们',
  contactEyebrow: '联系我们',
  contactTitle: '聊聊你的想法。',
  contactEmail: '邮箱',
  contactHomepage: '个人主页',
  contactVisit: '访问我的主页',
  collection: '精选图集',
  lab: '交互实验室',
  workflow: '绘图工具',
  eyebrow: '严谨的科学，自由的表达。',
  heroDesc: '把原始结果，变成值得被看见的研究。\n探索数据、组织图形，完成下一张科研作品。',
  enter: '开始创作下一张图',
  sculpture: '探索连续曲面',
  drag: '移动鼠标改变视角，滚动页面感受形变。',
  collectionTitle: '为研究，找到\n新的视角。',
  collectionDesc: '二十四个实时案例，同一种视觉语言。\n选择一种组合，让它成为你的作品。',
  labTitle: '雕琢图形，\n让证据清晰。',
  labDesc: '从参数到面板，从观测到细节。\n让每一次修改，都看得见。',
  newSample: '新样本',
  reset: '重置',
  palette: '配色方案',
  share: '复制链接 ↗',
  hoverHint: '悬停查看数值，各面板共享数据。',
  editData: '打开数据工作室',
  dataTitle: '你的数据，你的图。',
  localData: '数据仅在本地浏览器处理。参数调整会重新生成演示数据；应用 CSV 则替换当前数据。',
  applyData: '应用数据 ↗',
  workflowTitle: '一个工作流。\n无限种可能。',
  workflowDesc: '从交互探索开始。\n背后是完整的科研绘图工具链。',
  planDesc: '让研究问题决定图形，始终保留证据、配对关系与不确定性。',
  composeDesc: '整合数据、图像和方法结构，通过绘图 skill 建立连贯的视觉表达。',
  refineDesc: '用 paper-colors 统一配色，在论文实际尺寸下调整层级、留白和字体。',
  deliverDesc: '在线导出矢量图，继续使用 Python 完成可复现的论文图形。',
  installTitle: '下一张图，从这里开始。',
  closing: '做一张\n值得被看见的图。 ↗'
};

function tr() {
  document.querySelectorAll('[data-i18n]').forEach(e => {
    if (!e.dataset.en) e.dataset.en = e.innerHTML;
    if (e.dataset.i18n === 'heroTitle') {
      e.innerHTML = lang === 'zh' ? '让发现，<br><em>一眼难忘。</em>' : e.dataset.en;
    } else if (lang === 'zh' && words[e.dataset.i18n]) e.textContent = words[e.dataset.i18n];
    else e.innerHTML = e.dataset.en;
    e.style.whiteSpace = 'pre-line'
  });
  $('#language').textContent = lang === 'en' ? '中文' : 'EN';
  document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN'
}
$('#language').addEventListener('click', () => {
  lang = lang === 'en' ? 'zh' : 'en';
  tr()
});

function toast(s) {
  $('#toast').textContent = s;
  $('#toast').classList.add('visible');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => $('#toast').classList.remove('visible'), 3000)
}
async function copy(s) {
  try {
    await navigator.clipboard.writeText(s);
    return true
  } catch {
    toast('Clipboard unavailable. Select and copy the text manually.');
    return false
  }
}

function blobDownload(content, type, name) {
  const url = URL.createObjectURL(new Blob([content], {
      type
    })),
    a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

function updateURL() {
  const q = new URLSearchParams({
    seed: String(seed),
    palette
  });
  for (const [k, v] of Object.entries(params)) q.set(k, v);
  history.replaceState(null, '', '#lab/' + current.id + '?' + q)
}

function store() {
  cache.set(current.id, {
    seed,
    params: {
      ...params
    },
    rows: rows.map(r => [...r]),
    palette,
    custom
  })
}

function configure() {
  $('#study-title').textContent = current.title;
  $('#study-category').textContent = current.tag;
  $('#study-description').textContent = current.desc;
  $('#study-select').value = current.id;
  $('#figure-source').href = REPO + current.source;
  $('#figure-source').textContent=current.source.includes('interactive-studio')?'Study definitions ↗':'Python figure & definitions ↗';
  $('#schema-help').textContent = 'Columns: ' + schemas[current.family].join(', ') + '. Numeric values only. IDs and paired structures must remain consistent.';
  $('#controls').replaceChildren();
  for (const c of controls(current.family)) {
    const el = document.createElement('div');
    el.className = 'control';
    const label = document.createElement('label');
    label.className = 'control-heading';
    label.htmlFor = 'param-' + c.key;
    const name = document.createElement('span');
    name.textContent = c.label;
    label.append(name);
    let input;
    if (c.options) {
      input = document.createElement('select');
      c.options.forEach(v => {
        const o = document.createElement('option');
        o.value = v;
        o.textContent = v;
        input.append(o)
      });
      input.value = params[c.key]
    } else {
      const output = document.createElement('output');
      output.htmlFor = 'param-' + c.key;
      output.textContent = params[c.key];
      label.append(output);
      input = document.createElement('input');
      input.type = 'range';
      input.min = c.min;
      input.max = c.max;
      input.step = c.step;
      input.value = params[c.key]
    }
    input.id = 'param-' + c.key;
    input.addEventListener(c.options ? 'change' : 'input', () => {
      const n = c.options && typeof c.value === 'string' ? input.value : +input.value;
      params[c.key] = n;
      const output = el.querySelector('output');
      if (output) output.value = n;
      regenerate()
    });
    el.append(label, input);
    $('#controls').append(el)
  }
  if (current.family === 'diffusion') {
    const el = document.createElement('div');
    el.className = 'control';
    el.innerHTML = '<label class="control-heading" for="phase"><span>Trajectory playback</span><output for="phase">100%</output></label><input id="phase" type="range" min="0" max="100" value="100" step="1"><button class="text-button" id="play-sampling" style="font-size:10px;padding:10px 0">▶ Play sampling</button>';
    el.querySelector('input').addEventListener('input', e => {
      stopPlay();
      phase = +e.target.value / 100;
      el.querySelector('output').value = Math.round(phase * 100) + '%';
      paint(false, 'playback')
    });
    el.querySelector('button').addEventListener('click', () => {
      if (timer) {
        stopPlay();
        return
      }
      phase = 0;
      el.querySelector('button').textContent = 'Ⅱ Pause sampling';
      timer = setInterval(() => {
        phase = Math.min(1, phase + .03);
        el.querySelector('input').value = phase * 100;
        el.querySelector('output').value = Math.round(phase * 100) + '%';
        paint(false, 'playback');
        if (phase >= 1) stopPlay()
      }, 100)
    });
    $('#controls').append(el)
  }
  $('#palettes').replaceChildren();
  Object.entries(palettes).forEach(([name, cols]) => {
    const b = document.createElement('button');
    b.className = 'palette-button' + (name === palette ? ' active' : '');
    b.setAttribute('aria-label', name + ' palette');
    b.setAttribute('aria-pressed', name === palette);
    b.title = name;
    cols.forEach(col => {
      let dot = document.createElement('span');
      dot.style.background = col;
      b.append(dot)
    });
    b.addEventListener('click', () => {
      palette = name;
      $('#palettes').querySelectorAll('button').forEach(x => {
        x.classList.toggle('active', x === b);
        x.setAttribute('aria-pressed', x === b)
      });
      paint(false, 'palette');
      store();
      updateURL()
    });
    $('#palettes').append(b)
  });
  tr()
}

function stopPlay() {
  clearInterval(timer);
  timer = null;
  const b = $('#play-sampling');
  if (b) b.textContent = '▶ Play sampling'
}

function paint(recalculate = true, kind = 'data') {
  const begin = performance.now();
  if (recalculate) {
    simulation = simulate(current, rows, params);
    extra = current.family === 'diffusion' ? diffusionExtra(rows, params, simulation) : undefined
  }
  const result = render(current, rows, params, palettes[palette], {
    simulation,
    extra,
    phase,
    custom
  });
  cancelAnimationFrame(cameraRAF);
  clearInspection();
  canonicalFigure = result.svg;
  updatePanelPicker(result.svg);
  presenter.present(result.svg, {kind,animate:!booting});
  applyView();
  const signature = JSON.stringify(result.metrics);
  if (signature !== metricSignature) {
    metricSignature = signature;
    $('#metrics').replaceChildren();
    result.metrics.forEach(m => {
      const e = document.createElement('div'); e.className = 'metric';
      const value = document.createElement('strong'), label = document.createElement('span');
      value.textContent = m.value; label.textContent = m.label;
      e.append(value, label); $('#metrics').append(e);
    });
    if (!booting && kind !== 'playback') animateMetrics($('#metrics'));
  }
  $('#figure-caption').textContent = current.tag + ' / SEED ' + seed;
  $('#compute-time').textContent = Math.round(performance.now() - begin) + ' ms / LOCAL';
  $('#data-badge').textContent = custom ? 'YOUR DATA · LOCAL ONLY' : current.family === 'diffusion' ? 'COMPUTED TOY DIFFUSION' : 'SYNTHETIC DEMONSTRATION';
  $('#data-origin').textContent = current.family === 'diffusion' ? 'Analytic 8-mode score, finite σ=.01. Numerical error vs 512-call Heun; no trained image model.' : custom ? 'Your imported numeric observations. Derived views recomputed locally.' : 'Seeded browser fixtures, not pretrained-model results. Intervals are pointwise normal approximations, not the Python bootstrap intervals.';
  if (editOpen) $('#csv-editor').value = csv(rows, current.family);
  $('#chart').dataset.revision = String(++renderToken);
  document.dispatchEvent(new CustomEvent('prismatica:render', {
    detail: {
      study: current.id,
      rows: rows.length,
      custom
    }
  }))
}

function regenerate() {
  stopPlay();
  phase = 1;
  custom = false;
  rows = generate(current, params, seed);
  paint(true);
  store();
  updateURL();
  $('#data-error').textContent = '';
  const phaseInput = $('#phase');
  if (phaseInput) phaseInput.value = 100
}

function choose(id, fromHash = false) {
  const found = studies.find(s => s.id === id);
  if (!found) return;
  stopPlay();
  zoom = 1;
  view = {
    x: 0,
    y: 0,
    w: 1000,
    h: 620
  };
  current = found;
  const cached = cache.get(id);
  if (cached && !fromHash) {
    ({
      seed,
      params,
      rows,
      palette,
      custom
    } = cached);
    params = {
      ...params
    }
  } else {
    seed = 1107;
    params = defaults(current.family);
    palette = 'iris';
    custom = false;
    if (fromHash) {
      const query = new URLSearchParams(location.hash.split('?')[1] || '');
      const s = Number(query.get('seed'));
      if (Number.isInteger(s) && s > 0 && s < 2 ** 31) seed = s;
      const pal = query.get('palette');
      if (Object.prototype.hasOwnProperty.call(palettes, pal)) palette = pal;
      for (const c of controls(current.family)) {
        let v = query.get(c.key);
        if (v === null) continue;
        if (c.options) {
          let exact = c.options.find(x => String(x) === v);
          if (exact !== undefined) params[c.key] = exact
        } else {
          let n = Number(v);
          if (Number.isFinite(n) && n >= c.min && n <= c.max) params[c.key] = Number((Math.round(n / c.step) * c.step).toFixed(6))
        }
      }
    }
    rows = generate(current, params, seed)
  }
  phase = 1;
  configure();
  paint(true, 'study');
  markSelected();
  if (!booting && motionAllowed()) $('.control-panel').animate([{opacity:.45,transform:'translateX(-4px)'},{opacity:1,transform:'translateX(0)'}],{duration:230,easing:'cubic-bezier(.2,.8,.2,1)'});
  store();
  if (!fromHash && !booting) updateURL()
}
$('#study-select').innerHTML = studies.map(s => `<option value="${s.id}">${s.title}</option>`).join('');
$('#study-select').addEventListener('change', e => choose(e.target.value));
$('#shuffle').addEventListener('click', () => {
  seed = seed >= 2147483646 ? 1 : seed + 1;
  regenerate();
  toast('New deterministic sample · seed ' + seed)
});
$('#reset').addEventListener('click', () => {
  params = defaults(current.family);
  seed = 1107;
  configure();
  regenerate();
  toast('Default data and parameters restored')
});
$('#data-toggle').addEventListener('click', () => {
  editOpen = !editOpen;
  $('#data-editor').hidden = !editOpen;
  $('#data-toggle').setAttribute('aria-expanded', editOpen);
  $('#data-toggle b').textContent = editOpen ? '−' : '＋';
  if (editOpen) $('#csv-editor').value = csv(rows, current.family)
});

function applyText(text) {
  let next;
  if (text.trim().startsWith('{')) {
    let payload;
    try {
      payload = JSON.parse(text)
    } catch {
      throw Error('Invalid JSON. Use an exported Prismatica data file.')
    }
    if (payload.schema?.join(',') !== schemas[current.family].join(',')) throw Error('The JSON schema does not match this study.');
    next = payload.rows;
    validate(next, current.family)
  } else next = parseCSV(text, current.family);
  const backup = rows, wasCustom = custom;
  try {
    rows = next;
    custom = true;
    stopPlay();
    phase = 1;
    paint(true)
  } catch (err) {
    rows = backup;
    custom = wasCustom;
    paint(true);
    throw err
  }
  store();
  $('#data-error').textContent = 'Applied ' + rows.length + ' rows. All views recomputed.';
  toast('Data applied. The figure is now yours.')
}
$('#apply-data').addEventListener('click', () => {
  try {
    applyText($('#csv-editor').value)
  } catch (e) {
    $('#data-error').textContent = e.message
  }
});
$('#data-file').addEventListener('change', async e => {
  const file = e.target.files?.[0];
  if (!file) return;
  if (file.size > 2_000_000) {
    $('#data-error').textContent = 'Please use a file smaller than 2 MB.';
    return
  }
  try {
    const text = await file.text();
    applyText(text);
    $('#csv-editor').value = csv(rows, current.family)
  } catch (err) {
    $('#data-error').textContent = err.message
  }
  e.target.value = ''
});
$('#download-data').addEventListener('click', () => blobDownload(csv(rows, current.family), 'text/csv', current.id + '-data.csv'));
$('#download-json').addEventListener('click', () => blobDownload(JSON.stringify({
  version: 1,
  study: current.id,
  kind: custom ? 'user data' : current.family === 'diffusion' ? 'computed analytic-score fixture' : 'synthetic demonstration',
  seed,
  parameters: params,
  schema: schemas[current.family],
  rows
}, null, 2), 'application/json', current.id + '-data.json'));

function applyView() {
  const svg = $('#chart svg:not(.figure-ghost)');
  if (svg) svg.setAttribute('viewBox', `${view.x} ${view.y} ${view.w} ${view.h}`);
  $('#chart').style.touchAction = zoom > 1 ? 'none' : 'pan-y';
  $('#chart').style.cursor = zoom > 1 ? 'grab' : ''
}
$('#zoom-in').addEventListener('click', () => {
  cancelAnimationFrame(cameraRAF);
  presenter.finish();
  zoom = Math.min(4, zoom * 1.4);
  const w = 1000 / zoom,
    h = 620 / zoom;
  view = {
    x: Math.max(0, Math.min(1000 - w, view.x + view.w / 2 - w / 2)),
    y: Math.max(0, Math.min(620 - h, view.y + view.h / 2 - h / 2)),
    w,
    h
  };
  applyView();
  toast('Drag the figure to pan. Fit restores the full view.')
});
$('#zoom-fit').addEventListener('click', () => {
  cancelAnimationFrame(cameraRAF);
  presenter.finish();
  zoom = 1;
  panelPicker.value = '';
  view = {
    x: 0,
    y: 0,
    w: 1000,
    h: 620
  };
  applyView()
});
$('#chart').addEventListener('pointerdown', e => {
  if (zoom <= 1 || e.target.closest('[data-tip]')) return;
  cancelAnimationFrame(cameraRAF);
  presenter.finish();
  drag = {
    x: e.clientX,
    y: e.clientY,
    v: {
      ...view
    }
  };
  $('#chart').setPointerCapture(e.pointerId);
  tooltip.hidden = true
});
$('#chart').addEventListener('pointerup', () => {
  drag = null
});
$('#chart').addEventListener('pointercancel', () => {
  drag = null
});
$('#expand-figure').addEventListener('click', async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await $('.canvas-area').requestFullscreen()
  } catch {
    toast('Use your browser zoom for a closer look.')
  }
});
$('#export-svg').addEventListener('click', () => {
  const svg = parseFigure(canonicalFigure);
  svg.setAttribute('viewBox', '0 0 1000 620');
  svg.querySelectorAll('.muted,.linked').forEach(e => e.removeAttribute('class'));
  blobDownload(svg.outerHTML, 'image/svg+xml', current.id + '.svg');
  toast('Editable SVG exported')
});
$('#export-png').addEventListener('click', () => {
  const svg = parseFigure(canonicalFigure);
  svg.setAttribute('viewBox', '0 0 1000 620');
  svg.querySelectorAll('.muted,.linked').forEach(e => e.removeAttribute('class'));
  const url = URL.createObjectURL(new Blob([svg.outerHTML], {
      type: 'image/svg+xml'
    })),
    image = new Image();
  image.onload = () => {
    let canvas = document.createElement('canvas');
    canvas.width = 2400;
    canvas.height = 1488;
    canvas.getContext('2d').drawImage(image, 0, 0, 2400, 1488);
    canvas.toBlob(blob => {
      if (blob) {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = current.id + '.png';
        a.click();
        setTimeout(() => URL.revokeObjectURL(a.href), 1000);
        toast('High-resolution PNG exported')
      }
    });
    URL.revokeObjectURL(url)
  };
  image.onerror = () => {
    URL.revokeObjectURL(url);
    toast('PNG export unavailable. Try SVG instead.')
  };
  image.src = url
});
$('#share').addEventListener('click', async () => {
  updateURL();
  if (await copy(location.href)) toast(custom ? 'Link copied. Custom data is not included; export your CSV too.' : 'Reproducible parameter link copied')
});
const install = 'git clone https://github.com/Grady10086/Prismatica.git\ncd Prismatica\npython3 scripts/install_skills.py';
$('#copy-install').addEventListener('click', async () => {
  if (await copy(install)) toast('Installation commands copied')
});
const tooltip = $('#tooltip');
function clearInspection() {
  pinnedKey = null;
  clearSelection.hidden = true;
  selectionStatus.textContent = '';
  $('#tooltip').hidden = true;
  $('#chart').querySelectorAll('.muted,.linked').forEach(x=>x.classList.remove('muted','linked'));
}
function highlight(key) {
  $('#chart').querySelectorAll('[data-key]').forEach(x=>{
    x.classList.toggle('muted',key!==undefined&&x.dataset.key!==key);
    x.classList.toggle('linked',key!==undefined&&x.dataset.key===key);
  });
}
function showTip(el,e) {
  tooltip.textContent = el.dataset.tip;
  tooltip.hidden = false;
  const rect=tooltip.getBoundingClientRect();
  tooltip.style.left=Math.max(8,Math.min(innerWidth-rect.width-12,e.clientX+15))+'px';
  tooltip.style.top=Math.max(8,Math.min(innerHeight-rect.height-12,e.clientY+15))+'px';
}
function updatePanelPicker(source) {
  const svg=parseFigure(source), panels=[...svg.querySelectorAll('[data-panel-box]')];
  const signature=panels.map(p=>p.dataset.panelBox+p.dataset.panelLabel).join('|');
  if(signature===panelSignature)return;
  panelSignature=signature;
  panelPicker.replaceChildren(new Option('All panels', ''));
  panels.forEach(p=>panelPicker.append(new Option(p.dataset.panelLabel,p.dataset.panelBox)));
  panelPicker.value='';
}
panelPicker.addEventListener('change',()=>{
  cancelAnimationFrame(cameraRAF);
  presenter.finish();
  if(!panelPicker.value){$('#zoom-fit').click();return}
  const[x,y,w,h]=panelPicker.value.split(' ').map(Number);
  // Preserve the canvas aspect ratio and keep the entire selected panel visible.
  const width=Math.min(1000,Math.max(w+20,(h+20)*1000/620)),height=width*620/1000;
  const next={x:Math.max(0,Math.min(1000-width,x+w/2-width/2)),y:Math.max(0,Math.min(620-height,y+h/2-height/2)),w:width,h:height};
  const previous={...view};
  let start=null;
  function focus(now){
    if(start===null)start=now;
    const t=motionAllowed()?Math.min(1,(now-start)/280):1,e=1-(1-t)**3;
    for(const key of ['x','y','w','h'])view[key]=previous[key]+(next[key]-previous[key])*e;
    zoom=1000/view.w;
    applyView();
    if(t<1)cameraRAF=requestAnimationFrame(focus);
  }
  cameraRAF=requestAnimationFrame(focus);
});
clearSelection.addEventListener('click',clearInspection);
document.addEventListener('keydown',e=>{if(e.key==='Escape')clearInspection()});
$('#chart').addEventListener('pointerdown',e=>{pointerStart={x:e.clientX,y:e.clientY}});
$('#chart').addEventListener('click',e=>{
  if(pointerStart&&Math.hypot(e.clientX-pointerStart.x,e.clientY-pointerStart.y)>5)return;
  const el=e.target.closest('[data-key][data-tip]');
  if(!el||pinnedKey===el.dataset.key){clearInspection();return}
  pinnedKey=el.dataset.key;
  highlight(pinnedKey);
  showTip(el,e);
  clearSelection.hidden=false;
  selectionStatus.textContent='Observation '+pinnedKey+' selected across linked panels.';
});
$('#chart').addEventListener('pointermove', e => {
  if (drag && zoom > 1) {
    const box = $('#chart').getBoundingClientRect();
    view.x = Math.max(0, Math.min(1000 - view.w, drag.v.x - (e.clientX - drag.x) / box.width * view.w));
    view.y = Math.max(0, Math.min(620 - view.h, drag.v.y - (e.clientY - drag.y) / box.height * view.h));
    applyView();
    return;
  }
  if(pinnedKey!==null)return;
  const el=e.target.closest('[data-tip]');
  if(!el){tooltip.hidden=true;highlight(undefined);return}
  showTip(el,e);
  highlight(el.dataset.key);
});
$('#chart').addEventListener('pointerleave',()=>{
  tooltip.hidden=true;
  if(pinnedKey===null)highlight(undefined);
});

function markSelected() {
  cardCache.forEach((card,id)=>{card.classList.toggle('is-selected',id===current.id);if(id===current.id)card.setAttribute('aria-current','true');else card.removeAttribute('aria-current')});
}
function gallery() {
  const search = $('#search').value.toLowerCase();
  const selected = studies.filter(s=>(filter==='All'||s.category===filter)&&(s.title+' '+s.tag+' '+s.desc).toLowerCase().includes(search));
  const before = new Map([...$('#gallery').children].map(node=>[node.dataset.study,node.getBoundingClientRect()]));
  const cards = selected.map(study=>{
    if(cardCache.has(study.id))return cardCache.get(study.id);
    const card=document.createElement('button');card.type='button';card.className='study-card';card.dataset.study=study.id;
    card.setAttribute('aria-label','Explore '+study.title);
    card.innerHTML=`<div class="study-preview"></div><div class="card-topline"><span>${study.category}</span><span>${String(studies.indexOf(study)+1).padStart(2,'0')} / LIVE</span></div><h3>${study.title}<span>↗</span></h3><p>${study.tag}</p>`;
    card.addEventListener('click',()=>{choose(study.id);$('#laboratory').scrollIntoView({behavior:motionAllowed()?'smooth':'instant'})});
    const p=defaults(study.family);
    if(study.family==='retrieval')p.n=12;
    else if(study.family==='diffusion')p.n=32;
    else if(['paired','representation','flow','conflict'].includes(study.family))p.n=32;
    else if(['factorial','performance'].includes(study.family))p.n=6;
    const data=generate(study,p,1107+studies.indexOf(study));
    card.querySelector('.study-preview').innerHTML=render(study,data,p,palettes.iris).svg;
    cardCache.set(study.id,card);return card;
  });
  $('#gallery').classList.toggle('is-filtered',filter!=='All');
  $('#gallery').replaceChildren(...cards);
  $('#empty-gallery').hidden=selected.length>0;
  $('#collection-count').textContent=selected.length+' / '+studies.length+' STUDIES';
  markSelected();
  if(!booting)animateCards($('#gallery'),before);
}
for (const label of ['All', 'Multimodal', 'Generative', 'Model analysis', 'Statistical']) {
  const b = document.createElement('button');
  b.textContent = label;
  b.classList.toggle('active', label === filter);
  b.setAttribute('aria-pressed', label === filter);
  b.addEventListener('click', () => {
    filter = label;
    $('#filters').querySelectorAll('button').forEach(x => {
      x.classList.toggle('active', x === b);
      x.setAttribute('aria-pressed', x === b)
    });
    gallery()
  });
  $('#filters').append(b)
}
$('#search').addEventListener('input', gallery);
let revealObserver;

function observeReveals() {
  if (!revealObserver) {
    revealObserver = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        revealObserver.unobserve(e.target)
      }
    }), {
      threshold: .07
    });
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) document.body.classList.add('js-motion')
  }
  document.querySelectorAll('.reveal:not(.in)').forEach(e => revealObserver.observe(e))
}
window.addEventListener('hashchange', () => {
  if (location.hash.startsWith('#lab/')) {
    choose(location.hash.slice(5).split('?')[0], true);
    $('#laboratory').scrollIntoView()
  }
});
initHero();
gallery();
const hashId = location.hash.startsWith('#lab/') ? location.hash.slice(5).split('?')[0] : null;
choose(hashId && studies.some(s => s.id === hashId) ? hashId : studies[0].id, !!hashId);
booting = false;
if (hashId) setTimeout(() => $('#laboratory').scrollIntoView(), 100);
observeReveals();
