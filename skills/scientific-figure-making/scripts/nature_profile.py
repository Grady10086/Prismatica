"""Opt-in Nature main-figure typography; no palette, backend or data changes.

Sources and scope: ../references/nature.md. Not a submission compliance validator.
"""
from __future__ import annotations

import math
import string
import warnings

import matplotlib as mpl
from matplotlib import font_manager


def settings(*, font_size=7, family=None):
    """Use a locally installed Arial/Helvetica, or warn and use DejaVu Sans."""
    if not math.isfinite(float(font_size)) or not 5 <= float(font_size) <= 7:
        raise ValueError("Nature ordinary text must be between 5 and 7 pt")
    if family is None:
        available = {f.name for f in font_manager.fontManager.ttflist}
        family = next((f for f in ("Arial", "Helvetica") if f in available), None)
        if family is None:
            family = "DejaVu Sans"
            warnings.warn("Arial/Helvetica unavailable; DejaVu Sans is a preview fallback. "
                          "Check the target journal and final font embedding.", stacklevel=2)
    return {
        "font.family": family, "font.size": font_size,
        "axes.labelsize": font_size, "axes.titlesize": font_size,
        "xtick.labelsize": font_size, "ytick.labelsize": font_size,
        "legend.fontsize": font_size, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "axes.linewidth": 0.6,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.minor.width": 0.4, "ytick.minor.width": 0.4,
        "xtick.direction": "out", "ytick.direction": "out",
        "lines.linewidth": 0.8, "lines.markersize": 3,
        "patch.linewidth": 0.6,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "savefig.dpi": 450,
    }


def apply(**kwargs):
    """Call before constructing artists. Does not change paper-colors roles or cycles."""
    mpl.rcParams.update(settings(**kwargs))


def figure_size(column="single", *, height_mm=60):
    """Nature main-figure canvas; target-specific instructions take precedence."""
    widths = {"single": 89, "double": 183}
    if column not in widths:
        raise ValueError("column must be single or double")
    if not math.isfinite(float(height_mm)) or not 0 < height_mm <= 170:
        raise ValueError("height_mm must be positive and at most 170 mm")
    return widths[column] / 25.4, height_mm / 25.4


def label_panels(axes, *, x=0, y=1.08):
    """Add bold upright lowercase letters in axes coordinates; inspect for clipping.

    Reserve sufficient top/left space. Returns artists, so callers can align or move
    them explicitly. Pass axes in reading order, excluding colorbars and inset axes.
    """
    axes = list(axes)
    if len(axes) > 26:
        raise ValueError("At most 26 panels are supported")
    return [ax.text(x, y, letter, transform=ax.transAxes, fontsize=8,
                    fontweight="bold", fontstyle="normal", ha="left", va="bottom",
                    clip_on=False, color="black")
            for ax, letter in zip(axes, string.ascii_lowercase)]
