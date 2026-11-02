"""Original synthetic Nature-style comparison, replicates and signed heatmap."""
import argparse
import importlib.util
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "paper-colors" / "scripts"))
import nature_profile as nature
import exporters
import themes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fixtures = HERE.parents[1] / "paper-colors" / "tests" / "fixtures"
    loaded, _ = themes.load_all(fixtures / "palettes.json", fixtures / "swatches.json")
    theme = loaded["fixture"]
    module = args.out / "paper_colors.py"
    module.write_text(exporters.export_python(theme, themes.series_stats(theme)))
    spec = importlib.util.spec_from_file_location("nature_demo_colors", module)
    colors = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(colors)
    nature.apply()
    colors.apply()
    rng = np.random.default_rng(20261026)
    fig, axes = plt.subplots(1, 3, figsize=nature.figure_size("double", height_mm=64),
                             layout="constrained", gridspec_kw={"width_ratios": [1.15, 1, 1]})
    x = np.array([1, 2, 4, 8, 16])
    for i, (name, values) in enumerate(zip(("Ours", "Baseline A", "Baseline B"),
                                          ([70, 76, 80, 83, 85], [68, 72, 76, 79, 80], [65, 70, 73, 75, 77]))):
        axes[0].plot(x, values, label=name, linewidth=0.8,
                     **colors.style(i, redundant=True))
    axes[0].set(xlabel="Training steps (10³)", ylabel="Accuracy (%)")
    axes[0].legend(loc="lower right", handlelength=1.5)
    # Raw synthetic observations; horizontal segment is the median, not an error bar.
    groups = [rng.normal(mean, 2, 12) for mean in [72, 79, 85]]
    for i, observations in enumerate(groups):
        axes[1].scatter(i + rng.uniform(-0.12, 0.12, len(observations)), observations,
                        s=8, color=colors.C["ours"], alpha=0.55, linewidths=0)
        axes[1].plot([i-0.22, i+0.22], [np.median(observations)]*2,
                     color="black", linewidth=0.8)
    axes[1].set(xticks=[0, 1, 2], xticklabels=["Core", "+ Adpt.", "+ Obj."],
                xlabel="Cumulative components", ylabel="Accuracy (%)")
    delta = np.array([[-3, -1, 1, 2], [-2, 0, 3, 4], [-1, 2, 4, 5]])
    im = axes[2].imshow(delta, cmap=colors.cmap("diverging"),
                        norm=TwoSlopeNorm(vmin=-5, vcenter=0, vmax=5), aspect="auto")
    axes[2].set(xlabel="Evaluation condition", ylabel="Model size", xticks=range(4),
                xticklabels=["A", "B", "C", "D"], yticks=range(3), yticklabels=["S", "M", "L"])
    fig.colorbar(im, ax=axes[2], label="Δ accuracy (pp)", ticks=[-5, 0, 5], shrink=0.85)
    nature.label_panels(axes, y=1.03)
    fig.canvas.draw()
    # Preserve exact 183 × 64 mm canvas even under a global tight-crop preference.
    with matplotlib.rc_context({"savefig.bbox": None}):
        for fmt in ("pdf", "svg", "png"):
            fig.savefig(args.out / f"nature-panels.{fmt}", dpi=450, format=fmt)
    plt.close(fig)
    (args.out / "nature-panels-caption.txt").write_text(
        "Synthetic demonstration only; not experimental evidence. "
        "a, Method comparison. b, Twelve independently generated observations per group; "
        "horizontal segments show medians; jitter is for display only. "
        "c, Synthetic signed changes in percentage points with fixed limits ±5. "
        "Panels use the repository's synthetic fixture palette. Canvas: 183 × 64 mm.\n")
    print(f"Wrote Nature-style PDF/SVG/PNG and caption to {args.out}")


if __name__ == "__main__":
    main()
