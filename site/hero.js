const IRIS = ['#55609B', '#AB6690', '#E6A385'];
const TAU = Math.PI * 2;
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

// Periodic color and geometry preserve the half-twist seam of the Möbius strip.
function pigment(u) {
  const t = ((u / TAU) % 1 + 1) % 1 * 3;
  const k = Math.floor(t), f = t - k;
  const a = IRIS[k].slice(1).match(/../g).map(x => parseInt(x, 16));
  const b = IRIS[(k + 1) % 3].slice(1).match(/../g).map(x => parseInt(x, 16));
  return a.map((v, i) => Math.round(v + (b[i] - v) * f));
}

export function mobiusPoint(u, v, progress = 0, time = 0) {
  const width = .58 + progress * .11;
  const radius = 1.55 + .055 * Math.sin(3 * u + time * .32) * progress;
  const vv = v * width;
  return [(radius + vv * Math.cos(u / 2)) * Math.cos(u),
          (radius + vv * Math.cos(u / 2)) * Math.sin(u),
          vv * Math.sin(u / 2) + .11 * progress * Math.sin(2 * u + time * .25)];
}

export function initHero() {
  const hero = document.querySelector('.hero');
  const canvas = document.querySelector('#universe');
  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const motionButton = document.querySelector('#motion-toggle');
  let width = 0, height = 0, dpr = 1, visible = true;
  let paused = media.matches, mode = 0, time = 0, raf = 0, previous = 0;
  let pointer = { x: 0, y: 0 }, tilt = { x: 0, y: 0 };
  let targetProgress = 0, progress = 0;

  function readScroll() {
    targetProgress = clamp(-hero.getBoundingClientRect().top / Math.max(1, hero.offsetHeight), 0, 1.15);
  }

  function resize() {
    const rect = canvas.getBoundingClientRect();
    width = rect.width; height = rect.height;
    dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = width * dpr; canvas.height = height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    readScroll();
    draw();
  }

  function project(point) {
    let [x, y, z] = point;
    const rx = .92 + tilt.y * .42 + progress * .14;
    const ry = -.48 + tilt.x * .5 + progress * .72 + Math.sin(time * .2) * .07;
    const rz = -.38 + progress * .32 + Math.sin(time * .13) * .045;
    [y, z] = [y * Math.cos(rx) - z * Math.sin(rx), y * Math.sin(rx) + z * Math.cos(rx)];
    [x, z] = [x * Math.cos(ry) + z * Math.sin(ry), -x * Math.sin(ry) + z * Math.cos(ry)];
    [x, y] = [x * Math.cos(rz) - y * Math.sin(rz), x * Math.sin(rz) + y * Math.cos(rz)];
    const mobile = width < 760;
    const scale = Math.min(width * (mobile ? .39 : .205), height * .31);
    const perspective = 4.8 / (4.8 + z);
    const cx = width * (mobile ? .79 : .81) + tilt.x * 14;
    const cy = height * (mobile ? .43 : .48) - progress * height * .08;
    return [cx + x * scale * perspective, cy + y * scale * perspective, z];
  }

  function curve(points, color, alpha, lineWidth) {
    if (!points.length) return;
    ctx.beginPath();
    points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
    ctx.strokeStyle = color; ctx.globalAlpha = alpha; ctx.lineWidth = lineWidth; ctx.stroke();
  }

  function draw() {
    if (!width || !height) return;
    ctx.clearRect(0, 0, width, height);
    const mobile = width < 760;
    const segments = mobile ? 72 : 112, strips = mobile ? 12 : 18;
    const vertices = Array.from({ length: segments + 1 }, (_, i) =>
      Array.from({ length: strips + 1 }, (_, j) =>
        project(mobiusPoint(i * TAU / segments, -1 + 2 * j / strips, progress, time))));
    const faces = [];
    for (let i = 0; i < segments; i++) {
      const color = pigment((i + .5) * TAU / segments);
      for (let j = 0; j < strips; j++) {
        const points = [vertices[i][j], vertices[i + 1][j], vertices[i + 1][j + 1], vertices[i][j + 1]];
        faces.push({ points, depth: points.reduce((s, p) => s + p[2], 0) / 4, color });
      }
    }
    faces.sort((a, b) => b.depth - a.depth);
    if (mode !== 2) for (const face of faces) {
      ctx.beginPath();
      face.points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
      ctx.closePath();
      const light = clamp(.09 + (1.5 - face.depth) * .045, .04, .25);
      ctx.fillStyle = `rgb(${face.color.join(',')})`;
      ctx.globalAlpha = mode === 0 ? light : light * .18;
      ctx.fill();
      ctx.strokeStyle = `rgb(${face.color.join(',')})`;
      ctx.globalAlpha = mode === 0 ? .37 : .72;
      ctx.lineWidth = mode === 0 ? .5 : .6;
      ctx.stroke();
    }
    if (mode === 2) {
      for (let j = 0; j <= strips; j += 2) {
        for (let i = 0; i < segments; i++) {
          const rgb = pigment(i * TAU / segments);
          curve([vertices[i][j], vertices[i + 1][j]], `rgb(${rgb.join(',')})`, .76, .9);
        }
      }
      for (let i = 0; i < segments; i += 8) curve(vertices[i], '#AB6690', .2, .5);
    }
    for (const j of [0, strips]) curve(vertices.map(row => row[j]), '#E6A385', .7, .9);
    for (let i = 0; i < segments; i += 5) for (let j = 0; j <= strips; j += 3) {
      const [x, y, z] = vertices[i][j];
      const color = pigment(i * TAU / segments);
      ctx.fillStyle = `rgb(${color.join(',')})`; ctx.globalAlpha = clamp(.62 - z * .1, .3, .9);
      ctx.beginPath(); ctx.arc(x, y, mode === 1 ? 1.4 : .85, 0, TAU); ctx.fill();
    }
    // Fade the art behind the headline, keeping its geometry on the right.
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'destination-in';
    const fade = ctx.createLinearGradient(width * (mobile ? .12 : .42), 0, width * (mobile ? .72 : .63), 0);
    fade.addColorStop(0, 'rgba(0,0,0,0)'); fade.addColorStop(1, 'rgba(0,0,0,1)');
    ctx.fillStyle = fade; ctx.fillRect(0, 0, width, height);
    ctx.globalCompositeOperation = 'source-over';
  }

  function updateMotionButton() {
    motionButton.textContent = paused ? '▶' : 'Ⅱ';
    motionButton.setAttribute('aria-pressed', String(paused));
    motionButton.setAttribute('aria-label', paused ? 'Resume decorative motion' : 'Pause all decorative motion');
    document.body.classList.toggle('no-motion', paused);
  }

  function tick(stamp) {
    if (!previous) previous = stamp;
    const elapsed = stamp - previous;
    // Limit paint rate, and stop rendering when the hero or document is hidden.
    if (elapsed >= 32 && !paused && visible && !document.hidden) {
      const dt = Math.min(elapsed / 1000, .08);
      time += dt; previous = stamp;
      tilt.x += (pointer.x - tilt.x) * .095;
      tilt.y += (pointer.y - tilt.y) * .095;
      progress += (targetProgress - progress) * .09;
      draw();
    } else if (paused || !visible || document.hidden) previous = stamp;
    raf = requestAnimationFrame(tick);
  }

  hero.addEventListener('pointermove', event => {
    const rect = hero.getBoundingClientRect();
    pointer.x = clamp((event.clientX - rect.left) / width - .5, -.5, .5);
    pointer.y = clamp((event.clientY - rect.top) / height - .5, -.5, .5);
  });
  hero.addEventListener('pointerleave', () => { pointer = { x: 0, y: 0 }; });
  window.addEventListener('scroll', readScroll, { passive: true });
  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(canvas);
  const observer = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; });
  observer.observe(hero);
  document.querySelectorAll('[data-shape]').forEach(button => button.addEventListener('click', () => {
    mode = Number(button.dataset.shape);
    document.querySelectorAll('[data-shape]').forEach(item => {
      const selected = item === button;
      item.classList.toggle('active', selected); item.setAttribute('aria-pressed', String(selected));
    });
    draw();
  }));
  motionButton.addEventListener('click', () => { paused = !paused; updateMotionButton(); });
  media.addEventListener('change', event => { paused = event.matches; updateMotionButton(); draw(); });
  updateMotionButton(); resize(); raf = requestAnimationFrame(tick);
  return () => { cancelAnimationFrame(raf); observer.disconnect(); resizeObserver.disconnect(); window.removeEventListener('scroll', readScroll); };
}
