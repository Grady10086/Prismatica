"""Render synthetic examples without accessing ~/.paper-colors."""
import argparse
import importlib.util
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "paper-colors" / "scripts"))
import paper_layout as layout
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
    palette = args.out / "paper_colors.py"
    palette.write_text(exporters.export_python(theme, themes.series_stats(theme)))
    spec = importlib.util.spec_from_file_location("example_colors", palette)
    colors = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(colors)
    layout.apply()
    colors.apply()
    x = [1, 2, 4, 8, 16]
    results = ([70, 76, 80, 83, 85], [68, 72, 76, 79, 80], [65, 70, 73, 75, 77])

    def comparison(ax):
        for i, (name, y) in enumerate(zip(("Ours", "Baseline A", "Baseline B"), results)):
            ax.plot(x, y, label=name, linewidth=2.2 if i == 0 else 1.4,
                    **colors.style(i, redundant=True))
        ax.set(xlabel="Training steps (thousands)", ylabel="Accuracy (%)")

    def output(fig, name):
        findings = layout.inspect(fig)
        if findings:
            raise RuntimeError(f"{name}: {findings}")
        layout.save(fig, args.out / name)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=layout.figure_size("single", aspect=0.78), layout="constrained")
    comparison(ax)
    ax.legend(loc="lower right")
    output(fig, "comparison")

    fig, ax = plt.subplots(figsize=layout.figure_size("single", aspect=0.78), layout="constrained")
    ax.bar(["Core", "+ Adapter", "+ Objective"], [72, 79, 85],
           color=colors.ramp("ours", 3), edgecolor=colors.C["ours"], linewidth=0.8)
    ax.set(ylabel="Accuracy (%)", ylim=(0, 100), xlabel="Cumulative components")
    output(fig, "ablation")

    fig, axes = plt.subplots(1, 2, figsize=layout.figure_size("double", height_mm=65), layout="constrained")
    comparison(axes[0])
    axes[0].set_title("(a) Accuracy")
    axes[0].legend(loc="lower right")
    for i, (name, y) in enumerate(zip(("Ours", "Baseline A", "Baseline B"),
                                      ([6, 8, 12, 20, 36], [7, 10, 16, 28, 52], [9, 14, 24, 44, 84]))):
        axes[1].plot(x, y, label=name, **colors.style(i, redundant=True))
    axes[1].set(xlabel="Training steps (thousands)", ylabel="Latency (ms)", title="(b) Latency")
    output(fig, "panels")
    print(f"Wrote three synthetic figures (PDF/SVG/PNG) to {args.out}")


if __name__ == "__main__":
    main()
