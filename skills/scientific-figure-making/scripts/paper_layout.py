"""Matplotlib layout helpers. Copy next to figure scripts; no palette or data access."""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
from matplotlib.text import Text

WIDTHS_MM = {"single": 85.0, "double": 178.0}


def _positive(value, name):
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def figure_size(width="single", *, height_mm=None, aspect=0.68):
    """Return inches. Numeric widths are millimetres; named widths are starting points."""
    width_mm = WIDTHS_MM[width] if isinstance(width, str) else _positive(width, "width")
    height = (_positive(height_mm, "height_mm") if height_mm is not None
              else width_mm * _positive(aspect, "aspect"))
    return width_mm / 25.4, height / 25.4


def settings(*, font_size=8, family="DejaVu Sans"):
    """Return only layout/font/export rcParams; preserve colors and colormaps."""
    size = _positive(font_size, "font_size")
    return {
        "font.family": family, "font.size": size,
        "axes.labelsize": size, "axes.titlesize": size,
        "xtick.labelsize": size, "ytick.labelsize": size,
        "legend.fontsize": size, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "lines.linewidth": 1.4, "lines.markersize": 3.5,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "savefig.dpi": 300,
    }


def apply(**kwargs):
    """Apply before creating artists; combine with paper_colors.apply() in either order."""
    mpl.rcParams.update(settings(**kwargs))


def inspect(fig, *, min_font_size=7):
    """Advisory checks in points and display coordinates; not an overlap detector."""
    minimum = _positive(min_font_size, "min_font_size")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    findings = []
    # Matplotlib retains visible Text objects for locator ticks beyond the view;
    # Axis.draw filters these ticks, so do not report them as clipped content.
    excluded = set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            low, high = sorted(axis.get_view_interval())
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if not low <= tick.get_loc() <= high:
                    excluded.update((id(tick.label1), id(tick.label2)))
    for artist in fig.findobj(match=Text):
        if id(artist) in excluded or not artist.get_visible() or not artist.get_text().strip():
            continue
        label = artist.get_text()
        if artist.get_fontsize() < minimum:
            findings.append(f"Small text ({artist.get_fontsize():g} pt): {label}")
        box = artist.get_window_extent(renderer)
        if (box.x0 < bounds.x0 - 1 or box.y0 < bounds.y0 - 1
                or box.x1 > bounds.x1 + 1 or box.y1 > bounds.y1 + 1):
            findings.append(f"Text outside canvas: {label}")
    return findings


def save(fig, stem, *, formats=("pdf", "svg", "png"), dpi=300):
    """Save exact canvas size, even if the caller configured savefig.bbox='tight'.

    stem is an extension-free path. PNG is an inspection preview; PDF/SVG retain vectors.
    """
    formats = tuple(formats)
    if not formats or any(f not in {"pdf", "svg", "png"} for f in formats):
        raise ValueError("formats must contain pdf, svg or png")
    dpi = _positive(dpi, "dpi")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = []
    # bbox_inches=None alone inherits the caller's rcParams setting.
    with mpl.rc_context({"savefig.bbox": None}):
        for fmt in formats:
            path = Path(f"{stem}.{fmt}")
            fig.savefig(path, format=fmt, dpi=dpi, bbox_inches=None)
            paths.append(path)
    return paths
