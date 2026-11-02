"""Six image-dense teaser compositions for video, 3D and manipulation results.

Run beside result_teasers.py. Frames are ordered source samples, not a claim of
contiguous video frames or equal time intervals. Labels and layout remain SVG text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from result_teasers import Board, INK, MUTED

ACCENT = '#332288'


def canvas(m, height):
    b = Board(m['title'], height, reuse_images=True)
    b.text(40, 45, m['category'], 16, ACCENT, 600)
    b.text(40, 98, m['title'], 38, weight=600)
    return b


def photo(b, m, ref, x, y, w, h):
    b.image(m['assets'][ref['asset']], x, y, w, h, ref.get('crop'), background='white')


def ordinal(b, x, y, number):
    b.rect(x, y, 37, 28, '#202126')
    b.text(x + 18.5, y + 20, f'{number:02}', 16, 'white', anchor='middle')


def cinema(m):
    b = canvas(m, 1050)
    b.text(40, 132, 'SELECTED OUTPUT', 16, MUTED)
    photo(b, m, m['frames'][-1], 40, 148, 1000, 562.5)
    b.text(1080, 132, 'CONDITIONING IMAGE', 16, MUTED)
    photo(b, m, m['input'], 1080, 148, 480, 270)
    b.text(1080, 449, 'OUTPUT DETAIL', 16, MUTED)
    photo(b, m, m['detail'], 1080, 465, 480, 245.5)
    b.text(40, 748, 'ORDERED OUTPUT SAMPLES', 16, MUTED)
    for i, ref in enumerate(m['frames']):
        x = 40 + i * 383
        photo(b, m, ref, x, 765, 371, 208.7)
        ordinal(b, x, 765, i + 1)
    return b.finish(m['source_label'], m['kind'])


def proofsheet(m):
    b = canvas(m, 1000)
    for i, row in enumerate(m['rows']):
        y = 144 + i * 260
        b.text(40, y, row['label'], 23, ACCENT if row.get('highlight') else INK, 600)
        for j, ref in enumerate(row['frames']):
            x = 40 + j * 383
            photo(b, m, ref, x, y + 19, 371, 208.7)
            ordinal(b, x, y + 19, j + 1)
    return b.finish(m['source_label'], m['kind'])


def object_stage(m):
    b = canvas(m, 1180)
    b.text(40, 151, 'INPUT', 16, MUTED)
    photo(b, m, m['input'], 40, 172, 280, 280)
    b.text(40, 520, 'RECONSTRUCTED GEOMETRY', 16, MUTED)
    photo(b, m, m['geometry'], 40, 541, 280, 280)
    b.text(405, 151, 'TEXTURED MESH', 16, ACCENT, 600)
    photo(b, m, m['hero'], 365, 172, 740, 650)
    b.text(1140, 151, 'NORMALS', 16, MUTED)
    b.text(1140, 507, 'COLOR VIEWS', 16, MUTED)
    for i, ref in enumerate(m['normals']):
        photo(b, m, ref, 1140 + i * 215, 177, 205, 270)
    for i, ref in enumerate(m['colors']):
        photo(b, m, ref, 1140 + i * 215, 533, 205, 270)
    b.rule(40, 861, 1560, 861)
    b.text(40, 893, 'MORE RECONSTRUCTIONS', 16, MUTED)
    for i, ref in enumerate(m['gallery']):
        photo(b, m, ref, 40 + i * 383, 912, 371, 186)
    return b.finish(m['source_label'], m['kind'])


def geometry_comparison(m):
    b = canvas(m, 1100)
    for j, label in enumerate(m['columns']):
        center = 40 + 1520*m['column_centers'][j] if 'overview' in m else 40 + j*308 + 144
        b.text(center, 148, label, 21, ACCENT if j == 1 else INK,
               600, anchor='middle')
    if 'overview' in m:
        photo(b, m, m['overview'], 40, 172, 1520, 812)
        return b.finish(m['source_label'], m['kind'])
    for i, row in enumerate(m['objects']):
        y = 177 + i * 279
        for j, ref in enumerate(row['images']):
            photo(b, m, ref, 40 + j * 308, y, 288, 246)
        b.text(40, y + 267, row['label'], 17, MUTED)
    return b.finish(m['source_label'], m['kind'])


def robot_diptych(m):
    b = canvas(m, 930)
    for i, task in enumerate(m['tasks']):
        x = 40 + i * 780
        b.text(x, 151, task['label'], 25, weight=600)
        photo(b, m, task['frames'][-1], x, 175, 740, 470)
        b.text(x, 674, 'LAST SHOWN FRAME', 16, MUTED)
        for j, ref in enumerate(task['frames'][:-1]):
            xx = x + j * 187
            photo(b, m, ref, xx, 702, 179, 132)
            ordinal(b, xx, 702, j + 1)
    return b.finish(m['source_label'], m['kind'])


def task_mosaic(m):
    b = canvas(m, 1060)
    for i, task in enumerate(m['tasks']):
        x = 40 + (i % 2) * 780
        y = 150 + (i // 2) * 422
        b.text(x, y, task['label'], 25, weight=600)
        for j, ref in enumerate([task['frames'][0], task['frames'][-1]]):
            photo(b, m, ref, x + j * 376, y + 23, 364, 295)
            b.text(x + j * 376, y + 344, 'First shown' if j == 0 else 'Last shown', 17, MUTED)
    return b.finish(m['source_label'], m['kind'])


LAYOUTS = {'video-cinema': cinema, 'video-proofsheet': proofsheet,
           'object-stage': object_stage, 'geometry-comparison': geometry_comparison,
           'robot-diptych': robot_diptych, 'task-mosaic': task_mosaic}


def validate_refs(m):
    """Validate every visual reference before creating an output directory."""
    def walk(value):
        if isinstance(value, dict):
            if 'asset' in value:
                if value['asset'] not in m['assets']:
                    raise ValueError(f"Unknown asset: {value['asset']}")
                a = m['assets'][value['asset']]
                crop = value.get('crop', [0, 0, *a['size']])
                if (len(crop) != 4 or not all(isinstance(n, (int, float)) and math.isfinite(n) for n in crop)):
                    raise ValueError('Crop must have four finite coordinates')
                x, y, w, h = crop
                if min(x, y) < 0 or min(w, h) <= 0 or x + w > a['size'][0] or y + h > a['size'][1]:
                    raise ValueError('Crop outside image')
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk({k: v for k, v in m.items() if k != 'assets'})
    layout = m['layout']
    if layout == 'video-cinema' and len(m['frames']) != 4:
        raise ValueError('Cinema needs four ordered samples')
    if layout == 'video-proofsheet' and (len(m['rows']) != 3 or any(len(r['frames']) != 4 for r in m['rows'])):
        raise ValueError('Proofsheet needs three methods with four samples each')
    if layout == 'object-stage' and (len(m['normals']) != 2 or len(m['colors']) != 2 or len(m['gallery']) != 4):
        raise ValueError('Object stage needs two normal views, two color views and four gallery assets')
    if layout == 'geometry-comparison' and 'overview' not in m and (len(m['columns']) != 5 or len(m['objects']) != 3 or any(len(r['images']) != 5 for r in m['objects'])):
        raise ValueError('Geometry comparison needs three objects and five matching columns')
    if layout == 'geometry-comparison' and 'overview' in m:
        if len(m['columns']) != 5 or len(m['column_centers']) != 5 or any(not 0 <= x <= 1 for x in m['column_centers']):
            raise ValueError('Overview needs five columns and normalized column centers')
    if layout in {'robot-diptych', 'task-mosaic'}:
        count = 2 if layout == 'robot-diptych' else 4
        if len(m['tasks']) != count or any(len(t['frames']) != 5 for t in m['tasks']):
            raise ValueError(f'{layout} needs {count} tasks with five ordered samples each')


def main():
    global ACCENT
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--png', action='store_true')
    p.add_argument('--tokens', type=Path, help='paper-colors JSON; annotation accent only')
    args = p.parse_args()
    m = json.loads(args.manifest.read_text())
    if m.get('layout') not in LAYOUTS: raise ValueError('Unknown layout')
    if m.get('kind') not in {'PUBLISHED REFERENCE STUDY', 'PROJECT RESULTS'}:
        raise ValueError('Declare published reference or project results')
    for field in ['source_label', 'source_url', 'title', 'category']:
        if not m.get(field): raise ValueError(f'Missing {field}')
    if args.tokens:
        palette = json.loads(args.tokens.read_text())
        color = palette['hues']['ours']['anchor']
        if not isinstance(color, str) or len(color) != 7 or not color.startswith('#'):
            raise ValueError('Accent must be #RRGGBB')
        int(color[1:], 16)
        ACCENT = color
    else:
        ACCENT = '#332288'
    audit = json.loads(json.dumps(m))
    for key, a in m['assets'].items():
        path = Path(a['file']).expanduser()
        if not path.is_absolute(): path = args.manifest.resolve().parent / path
        if not path.is_file(): raise ValueError(f'Missing local asset: {path}')
        size = a['size']
        if len(size) != 2 or not all(isinstance(n, (int, float)) and math.isfinite(n) and n > 0 for n in size):
            raise ValueError('Supply finite positive image dimensions')
        a['path'] = path
        audit['assets'][key]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    validate_refs(m)
    svg = LAYOUTS[m['layout']](m)
    png = None
    if args.png:
        import resvg_py
        png = resvg_py.svg_to_bytes(svg_string=svg, width=2000, dpi=96)
    args.out.mkdir(parents=True, exist_ok=True)
    stem = args.out / m['layout']
    stem.with_suffix('.svg').write_text(svg)
    if png: stem.with_suffix('.png').write_bytes(png)
    audit['annotation_accent'] = ACCENT
    audit['transformations'] = 'Layout, aspect-preserving scaling and declared SVG crops; embedded raster bytes unchanged.'
    stem.with_name(stem.name + '-provenance.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(f'Wrote {stem}')


if __name__ == '__main__': main()
