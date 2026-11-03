"""Build editorial brand banners with an original projected Möbius surface."""
from pathlib import Path
import argparse
import math
import xml.etree.ElementTree as E
import resvg_py
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from build_brand_wordmark import outlined
from build_gallery_cover import tag, subsvg, ROOT


def element(parent, name, **attrs):
    return E.SubElement(parent, tag(name), {k.replace('_', '-'): str(v) for k, v in attrs.items()})


def text(parent, x, y, value, size, color, weight='400'):
    node = element(parent, 'text', x=x, y=y, font_family='DejaVu Sans, sans-serif',
                   font_size=size, fill=color, font_weight=weight)
    node.text = value
    return node


def export(root, out, name):
    raw = E.tostring(root, encoding='unicode')
    (out / f'{name}.svg').write_text(raw + '\n')
    (out / f'{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=raw, width=2400))


def project(u, v):
    radius = 1.55 + v * math.cos(u / 2)
    x, y, z = radius * math.cos(u), radius * math.sin(u), v * math.sin(u / 2)
    # Oblique projection exposes the ribbon's continuous half twist.
    rx, ry, rz = .92, -.48, -.38
    y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
    x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
    x, y = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
    scale = 160 * 4.8 / (4.8 + z)
    return 947 + x * scale, 206 + y * scale, z


def surface(parent, dark):
    colors = ['#55609B', '#AB6690', '#E6A385']
    quads = []
    steps, strips = 144, 18
    for i in range(steps):
        u0, u1 = i * math.tau / steps, (i + 1) * math.tau / steps
        for j in range(strips):
            v0, v1 = -.58 + 1.16 * j / strips, -.58 + 1.16 * (j + 1) / strips
            points = [project(u0, v0), project(u1, v0), project(u1, v1), project(u0, v1)]
            depth = sum(p[2] for p in points) / 4
            color = colors[min(2, int((i / steps) * 3))]
            quads.append((depth, color, points))
    for depth, color, points in sorted(quads, reverse=True):
        light = max(.03, .10 + (1.8 - depth) * .045)
        element(parent, 'path', d='M' + 'L'.join(f'{x:.2f},{y:.2f}' for x, y, _ in points) + 'Z',
                fill=color, fill_opacity=light if dark else light * .8,
                stroke=color, stroke_opacity=.48 if dark else .39, stroke_width=.46)
    for v in [-.58, .58]:
        points = [project(i * math.tau / 300, v) for i in range(301)]
        element(parent, 'path', d='M' + 'L'.join(f'{x:.2f},{y:.2f}' for x, y, _ in points),
                fill='none', stroke='#E6A385' if dark else '#AB6690', stroke_opacity=.65,
                stroke_width=.9)
    # Sparse highlights reveal the surface geometry without adding chart-like claims.
    for i in range(0, 144, 4):
        for j in range(0, 19, 3):
            x, y, z = project(i * math.tau / 144, -.58 + 1.16 * j / 18)
            element(parent, 'circle', cx=f'{x:.2f}', cy=f'{y:.2f}', r=.8,
                    fill=colors[min(2, i // 48)], fill_opacity=.8 if dark else .7)


def build(gallery, out):
    out.mkdir(parents=True, exist_ok=True)
    for dark in [False, True]:
        bg, ink, muted = ('#100F19', '#F4F1EA', '#A29AAC') if dark else ('#F7F5F0', '#333F49', '#7D7688')
        root = E.Element(tag('svg'), {'width': '1200', 'height': '420', 'viewBox': '0 0 1200 420',
                                    'role': 'img', 'aria-label': 'Prismatica — make data matter. Scientific visualization studio.'})
        element(root, 'title').text = 'Prismatica — make data matter.'
        defs = element(root, 'defs')
        gradient = element(defs, 'radialGradient', id='aura')
        element(gradient, 'stop', offset='0', stop_color='#AB6690', stop_opacity='.19' if dark else '.10')
        element(gradient, 'stop', offset='1', stop_color=bg, stop_opacity='0')
        fade = element(defs, 'linearGradient', id='fade')
        element(fade, 'stop', offset='0', stop_color='black')
        element(fade, 'stop', offset='.49', stop_color='black')
        element(fade, 'stop', offset='.64', stop_color='white')
        element(fade, 'stop', offset='1', stop_color='white')
        mask = element(defs, 'mask', id='art-mask')
        element(mask, 'rect', width=1200, height=420, fill='url(#fade)')
        element(root, 'rect', width=1200, height=420, fill=bg)
        element(root, 'ellipse', cx=956, cy=205, rx=430, ry=340, fill='url(#aura)')
        art = element(root, 'g', mask='url(#art-mask)')
        # Fine coordinate dots are a texture, not data.
        for x in range(650, 1200, 24):
            for y in range(30, 420, 24):
                element(art, 'circle', cx=x, cy=y, r=.55, fill=muted, opacity='.20')
        surface(art, dark)
        kicker = text(root, 56, 43, 'THE SCIENTIFIC VISUALIZATION STUDIO', 9, muted, '500')
        kicker.set('letter-spacing', '2.1')
        subsvg(root, ROOT / 'docs/brand' / ('horizontal-dark.svg' if dark else 'horizontal.svg'),
               None, 39, 70, 568, 136, 'brand')
        element(root, 'path', d=outlined(TextPath((0, 0), 'Make data matter.', size=40, prop=FontProperties(family='DejaVu Sans'))), transform='translate(56 262) scale(1 -1)', fill=ink)
        text(root, 58, 294, 'Complex evidence. Clear expression.', 15, muted)
        element(root, 'rect', x=56, y=325, width=230, height=37, rx=19,
                fill=ink, fill_opacity='.055' if dark else '.035', stroke=muted,
                stroke_opacity='.42', stroke_width='.7')
        text(root, 74, 348, 'Explore the interactive studio', 11, ink)
        text(root, 263, 349, '↗', 16, '#E6A385' if dark else '#55609B')
        footer = text(root, 58, 394, 'PLOTS  /  PALETTES  /  PUBLICATION LAYOUTS', 8.5, muted)
        footer.set('letter-spacing', '1.25')
        text(root, 1138, 394, 'FIGURES, REIMAGINED.', 8, muted).set('text-anchor', 'end')
        export(root, out, 'masthead-v2' + ('-dark' if dark else ''))
    print(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--gallery', type=Path, default=ROOT / 'docs/gallery')
    p.add_argument('--out', type=Path, default=ROOT / 'docs/homepage')
    args = p.parse_args()
    build(args.gallery, args.out)


if __name__ == '__main__':
    main()
