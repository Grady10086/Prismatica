"""Original synthetic architecture comparison + accuracy/cost evidence.

No author/lab style is claimed. See references/research-patterns.md for sources.
"""
import argparse
import importlib.util
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "paper-colors" / "scripts"))
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
    spec = importlib.util.spec_from_file_location("composition_colors", palette)
    colors = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(colors)
    config = {"font.size": 8, "font.family": "DejaVu Sans", "legend.fontsize": 7,
              "axes.spines.top": False, "axes.spines.right": False,
              "svg.fonttype": "none", "savefig.bbox": None}
    with matplotlib.rc_context(config):
        colors.apply()
        fig, (diagram, evidence) = plt.subplots(1, 2, figsize=(183/25.4, 80/25.4),
                                               layout="constrained", width_ratios=[1.05, 1])
        diagram.set(xlim=(0, 2.8), ylim=(0, 4.7))
        diagram.axis("off")
        diagram.set_title("a  Controlled architectural change", loc="left", fontsize=9, pad=12)
        for x, name, module, role in [(0.15, "Baseline", "Fixed mixer", "base1"),
                                      (1.6, "Variant", "Adaptive mixer", "ours")]:
            diagram.text(x+0.5, 4.35, name, ha="center", fontweight="bold")
            for y, label in [(3.25, "Readout"), (2.15, module), (1.05, "Encoder")]:
                changed = label == module
                fill = colors.RAMP[role][0] if changed else colors.RAMP["neutral"][0]
                edge = colors.C[role] if changed else colors.C["neutral"]
                diagram.add_patch(FancyBboxPatch((x,y),1,0.58,
                    boxstyle="round,pad=0.05,rounding_size=0.06", facecolor=fill,
                    edgecolor=edge, linewidth=1.1 if changed else 0.7))
                diagram.text(x+0.5,y+0.29,label,ha="center",va="center",fontsize=7)
            for y in (1.65,2.75):
                diagram.annotate("",xy=(x+0.5,y+0.45),xytext=(x+0.5,y),
                    arrowprops={"arrowstyle":"->","color":colors.C["neutral"],"lw":0.8})
            diagram.text(x+0.5,0.7,"Same input",ha="center",fontsize=7)
        diagram.text(1.4,0.12,"Encoder and readout held fixed",ha="center",fontsize=7)
        evidence.set_title("b  Accuracy versus inference cost",loc="left",fontsize=9,pad=12)
        # Arrays are constructed for layout demonstration, not measured experiments.
        params = np.array([10, 20, 40])
        for name, role, xs, ys, marker in [
            ("Baseline", "base1", [4,8,14], [73,77,80], "s"),
            ("Variant", "ours", [3,6,11], [75,79,82], "o")]:
            evidence.plot(xs,ys,color=colors.C[role],lw=0.8,alpha=0.6)
            evidence.scatter(xs,ys,s=params*2,color=colors.C[role],marker=marker,
                             edgecolors="black",linewidths=0.4,label=name,zorder=3)
        evidence.set(xlabel="MACs (G, lower is better)",ylabel="Accuracy (%, higher is better)",
                     xlim=(0,17),ylim=(70,85))
        methods = evidence.legend(loc="lower right",frameon=False)
        evidence.add_artist(methods)
        handles = [evidence.scatter([],[],s=p*2,facecolor="none",edgecolor="black",
                    linewidth=0.5,label=f"{p}M") for p in [10,20,40]]
        evidence.legend(handles=handles,title="Parameters (area)",title_fontsize=7,
                        loc="upper left",frameon=False,handletextpad=0.4,labelspacing=0.65)
        fig.savefig(args.out / "research-composition.svg")
        fig.savefig(args.out / "research-composition.png",dpi=300)
        plt.close(fig)
    (args.out / "research-composition-caption.txt").write_text(
        "Original synthetic demonstration only. a, An invented module replacement with "
        "the encoder and readout held fixed. b, Invented accuracy and MACs at three "
        "parameter counts; marker area is linear in parameter count. No uncertainty "
        "or statistical superiority is claimed. Not a reproduction of any cited "
        "paper's architecture or results. Canvas 183 × 80 mm.\n")
    print(f"Wrote original synthetic composition to {args.out}")


if __name__ == "__main__":
    main()
