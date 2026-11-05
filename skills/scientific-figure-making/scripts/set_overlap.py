"""Exact membership summaries and schematic flower / UpSet / Jaccard figures.

Input CSV: item,<2 to 6 set names>; membership cells are 0 or 1.
Item IDs may be strings. One unique item per row; no all-zero rows.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Ellipse, RegularPolygon
import numpy as np

COLORS = ['#55609B', '#AB6690', '#E6A385', '#758E8B', '#8890B9', '#C28EAE']
INK = '#333F49'
PAPER = '#F8F7F2'


def summarize(ids, membership, names):
    """Compute exclusive masks, inclusive pair counts and exact union statistics."""
    if any(not isinstance(name, str) or not name.strip() for name in names):
        raise ValueError('Set names must be non-blank strings.')
    if not 2 <= len(names) <= 6 or len(set(names)) != len(names):
        raise ValueError('Use 2–6 distinct set names.')
    if not ids or any(not str(item).strip() for item in ids) or len(ids) != len(membership) or len(set(ids)) != len(ids):
        raise ValueError('Use one unique item ID per membership row.')
    if any(len(row) != len(names) or any(v not in (0, 1) for v in row) or not any(row)
           for row in membership):
        raise ValueError('Memberships must be binary, rectangular and non-empty per item.')
    a = np.array(membership, dtype=int)
    masks = [sum(int(v) << i for i, v in enumerate(row)) for row in a]
    counts = Counter(masks)
    totals = a.sum(axis=0)
    shared = a.T @ a
    union = totals[:, None] + totals[None, :] - shared
    similarity = np.divide(shared, union, out=np.full(shared.shape, np.nan), where=union > 0)
    return dict(names=list(names), union=len(ids), core=counts.get((1 << len(names))-1, 0),
                totals=totals.tolist(), unique=[counts.get(1 << i, 0) for i in range(len(names))],
                degree=[sum(n for mask, n in counts.items() if mask.bit_count() == k)
                        for k in range(1, len(names)+1)],
                intersections=sorted(counts.items(), key=lambda v: (-v[1], v[0])),
                shared=shared.tolist(), jaccard=similarity.tolist())


def read_memberships(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as handle:
        rows = list(csv.reader(handle))
    if not rows or len(rows[0]) < 3 or rows[0][0].strip() != 'item':
        raise ValueError('Expected item,<set names> header.')
    names = [v.strip() for v in rows[0][1:]]
    if not all(names):
        raise ValueError('Set names cannot be blank.')
    ids, membership = [], []
    for line, row in enumerate(rows[1:], 2):
        if not row:
            continue
        if len(row) != len(names)+1 or not row[0].strip() or any(v.strip() not in ('0', '1') for v in row[1:]):
            raise ValueError(f'Invalid membership row {line}.')
        ids.append(row[0].strip())
        membership.append([int(v.strip()) for v in row[1:]])
    return ids, membership, names


def demo_memberships(n=400, seed=1107):
    rng = random.Random(seed)
    matrix = []
    for _ in range(n):
        row = [1]*6 if rng.random() < .2 else [int(rng.random() < .35) for _ in range(6)]
        if not any(row):
            row[rng.randrange(6)] = 1
        matrix.append(row)
    return [f'item_{i+1}' for i in range(n)], matrix, list('ABCDEF')


def flower(ax, data):
    """Petals are decorative summary glyphs; counts do not determine geometry."""
    n = len(data['names'])
    angles = np.linspace(np.pi/2, np.pi/2-2*np.pi, n, endpoint=False)
    for i, theta in enumerate(angles):
        c, s = np.cos(theta), np.sin(theta)
        ax.add_patch(Ellipse((.33*c, .33*s), 1.28, .73, angle=np.degrees(theta),
                             facecolor=COLORS[i], edgecolor=COLORS[i], alpha=.22, lw=1.4))
    for i, theta in enumerate(angles):
        c, s = np.cos(theta), np.sin(theta)
        ax.text(1.08*c, 1.08*s, data['names'][i], ha='center', va='center', color=COLORS[i], fontsize=12)
        ax.text(.73*c, .73*s+.015, str(data['unique'][i]), ha='center', va='center', color=COLORS[i], fontsize=15)
        ax.text(.73*c, .73*s-.07, 'exclusive', ha='center', va='center', color=INK, fontsize=7)
    ax.add_patch(RegularPolygon((0, 0), n, radius=.35, orientation=np.pi/2,
                                facecolor='#EAE5F2', edgecolor=COLORS[0], lw=1.4))
    ax.text(0, .12, f'ALL {n} SETS', ha='center', fontsize=8, color=COLORS[0])
    ax.text(0, -.025, str(data['core']), ha='center', fontsize=25, color=INK)
    ax.text(0, -.14, f"{data['core']/data['union']:.1%} of union", ha='center', fontsize=8, color=INK)
    ax.set(xlim=(-1.28, 1.28), ylim=(-1.25, 1.25), aspect='equal')
    ax.axis('off')
    ax.set_title('Shared-core summary · schematic petals', loc='left', fontsize=11, color=INK)


def set_sizes(ax, data):
    y = np.arange(len(data['names']))
    ax.barh(y, data['totals'], color=COLORS[:len(y)], alpha=.25, height=.6)
    ax.barh(y, data['unique'], color=COLORS[:len(y)], height=.6)
    for i in y:
        ax.text(data['totals'][i]+max(data['totals'])*.02, i,
                f"{data['totals'][i]} / {data['unique'][i]}", va='center', fontsize=8)
    ax.set(yticks=y, yticklabels=data['names'], xlabel='Items · light: total / dark: exclusive',
           xlim=(0, max(data['totals'])*1.3))
    ax.invert_yaxis()
    ax.set_title('Set sizes and exclusive items', loc='left', fontsize=10)


def upset(ax, data, top=18):
    shown = data['intersections'][:top]
    maximum = max(v for _, v in shown)
    n = len(data['names'])
    for i, (mask, count) in enumerate(shown):
        color = COLORS[0] if mask == (1 << n)-1 else COLORS[(mask.bit_count()-1) % len(COLORS)]
        ax.bar(i, count/maximum, width=.65, color=color)
        ax.text(i, count/maximum+.025, str(count), ha='center', fontsize=8)
        active = [j for j in range(n) if mask & (1 << j)]
        ax.plot([i, i], [-.18-active[0]*.105, -.18-active[-1]*.105], color=color, lw=1.2)
        for j in range(n):
            ax.scatter(i, -.18-j*.105, s=20, color=color if j in active else '#DDD7E3', zorder=3)
    for j, name in enumerate(data['names']):
        ax.text(-.7, -.18-j*.105, name, va='center', ha='right', fontsize=8)
    ax.set(ylim=(-.3-n*.105, 1.17), xlim=(-1, len(shown)), xticks=[], yticks=[0, .5, 1],
           yticklabels=['0', f'{maximum/2:g}', str(maximum)], ylabel='Exclusive intersection size')
    ax.spines['bottom'].set_visible(False)
    omitted = sum(count for _, count in data['intersections'][top:])
    ax.set_title(f'{len(shown)} / {len(data["intersections"])} exact intersections · {omitted} items omitted', loc='left', fontsize=10)


def jaccard(ax, data):
    matrix = np.array(data['jaccard'])
    image = ax.imshow(matrix, vmin=0, vmax=1,
                      cmap=LinearSegmentedColormap.from_list('iris_similarity', ['#F0EBEF', COLORS[0]]))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            value = matrix[i, j]
            ax.text(j, i, '—' if np.isnan(value) else f'{value:.2f}', ha='center', va='center',
                    color='white' if value > .65 else INK, fontsize=9)
    ax.set(xticks=range(len(matrix)), yticks=range(len(matrix)),
           xticklabels=data['names'], yticklabels=data['names'])
    ax.set_title('Pairwise Jaccard · inclusive intersection / union', loc='left', fontsize=10)
    return image


def export_all(data, out, provenance='User-provided memberships', top=18):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'svg.fonttype': 'none', 'pdf.fonttype': 42, 'font.size': 9,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.labelcolor': INK, 'text.color': INK, 'axes.edgecolor': '#C5C9CE'})
    for mode in ['flower', 'upset', 'jaccard']:
        fig = plt.figure(figsize=(11.6, 6.6), facecolor=PAPER, layout='constrained')
        gs = fig.add_gridspec(2, 2, width_ratios=[1.8, 1], hspace=.16)
        main = fig.add_subplot(gs[:, 0])
        if mode == 'flower':
            flower(main, data)
        elif mode == 'upset':
            upset(main, data, top)
        else:
            jaccard(main, data)
        set_sizes(fig.add_subplot(gs[0, 1]), data)
        degree = fig.add_subplot(gs[1, 1])
        degree.bar(np.arange(1, len(data['names'])+1), data['degree'], color=COLORS[:len(data['names'])], width=.65)
        degree.set(xlabel='Number of containing sets', ylabel='Distinct items',
                   xticks=np.arange(1, len(data['names'])+1))
        degree.set_title('Membership degree', loc='left', fontsize=10)
        fig.supxlabel(provenance+' · exact item counts · petal area is schematic, not proportional', fontsize=8)
        for extension in ['png', 'svg', 'pdf']:
            fig.savefig(out/f'set-{mode}.{extension}', dpi=180)
        plt.close(fig)
    with (out/'exact-intersections.csv').open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['mask', 'members', 'exclusive_count'])
        for mask, count in data['intersections']:
            writer.writerow([mask, ' & '.join(name for i, name in enumerate(data['names']) if mask & (1 << i)), count])
    # JSON has no non-standard NaN: two empty sets have undefined Jaccard.
    cleaned = {**data, 'jaccard': [[None if np.isnan(v) else v for v in row] for row in data['jaccard']]}
    (out/'summary.json').write_text(json.dumps({**cleaned, 'provenance': provenance}, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--csv', type=Path)
    source.add_argument('--demo', action='store_true')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--top', type=int, default=18)
    args = parser.parse_args()
    if args.top < 1:
        parser.error('--top must be positive')
    ids, membership, names = demo_memberships() if args.demo else read_memberships(args.csv)
    export_all(summarize(ids, membership, names), args.out,
               'Synthetic membership fixture' if args.demo else 'User-provided memberships', args.top)
    print(args.out)
