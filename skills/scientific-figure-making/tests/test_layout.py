"""Observable layout/export invariants and compatibility with paper-colors."""
import importlib.util
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from PIL import Image
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "paper-colors" / "scripts"))
import paper_layout as layout
import exporters
import themes


def test_palette_order_independent(tmp_path):
    fixtures = HERE.parents[1] / "paper-colors" / "tests" / "fixtures"
    loaded, _ = themes.load_all(fixtures / "palettes.json", fixtures / "swatches.json")
    theme = loaded["fixture"]
    module = tmp_path / "paper_colors.py"
    module.write_text(exporters.export_python(theme, themes.series_stats(theme)))
    spec = importlib.util.spec_from_file_location("layout_test_colors", module)
    colors = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(colors)
    with matplotlib.rc_context():
        colors.apply()
        expected = matplotlib.rcParams["axes.prop_cycle"]
        cmap = matplotlib.rcParams["image.cmap"]
        layout.apply()
        assert matplotlib.rcParams["axes.prop_cycle"] == expected
        assert matplotlib.rcParams["image.cmap"] == cmap
        colors.apply()
        assert matplotlib.rcParams["axes.prop_cycle"] == expected
        assert matplotlib.rcParams["font.size"] == 8


def test_exact_export_size_despite_tight_default(tmp_path):
    with matplotlib.rc_context({"savefig.bbox": "tight"}):
        fig, ax = plt.subplots(figsize=layout.figure_size(101.6, height_mm=50.8))
        ax.plot([0, 1], [0, 1])
        paths = layout.save(fig, tmp_path / "figure", dpi=100)
        assert matplotlib.rcParams["savefig.bbox"] == "tight"
        plt.close(fig)
    with Image.open(paths[2]) as im:
        assert im.size == (400, 200)
    page = PdfReader(paths[0]).pages[0]
    assert float(page.mediabox.width) == pytest.approx(288)
    assert float(page.mediabox.height) == pytest.approx(144)
    root = ET.parse(paths[1]).getroot()
    assert root.attrib["viewBox"] == "0 0 288 144"


def test_inspect_reports_small_and_outside_text():
    fig, ax = plt.subplots(figsize=(4, 3), layout="constrained")
    ax.plot([1, 2, 4, 8, 16], [70, 76, 80, 83, 85])
    ax.set(xlabel="Time (s)", ylabel="Accuracy (%)")
    assert layout.inspect(fig) == []
    fig.text(1.1, 0.5, "Outside", fontsize=6)
    report = layout.inspect(fig)
    assert any("Small text" in item for item in report)
    assert any("outside canvas" in item for item in report)
    plt.close(fig)


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_invalid_dimensions(value):
    with pytest.raises(ValueError):
        layout.figure_size(value)
    with pytest.raises(ValueError):
        layout.figure_size(height_mm=value)
