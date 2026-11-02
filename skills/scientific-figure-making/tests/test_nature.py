"""Nature profile preserves palette and encodes scoped physical conventions."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import nature_profile as nature


def test_profile_preserves_palette():
    with matplotlib.rc_context():
        original_cycle = matplotlib.rcParams["axes.prop_cycle"]
        original_cmap = matplotlib.rcParams["image.cmap"]
        nature.apply(family="DejaVu Sans")
        assert matplotlib.rcParams["axes.prop_cycle"] == original_cycle
        assert matplotlib.rcParams["image.cmap"] == original_cmap
        assert matplotlib.rcParams["font.size"] == 7
        assert matplotlib.rcParams["axes.grid"] is False
        assert 0.25 <= matplotlib.rcParams["lines.linewidth"] <= 1


def test_size_and_editable_panel_letters(tmp_path):
    with matplotlib.rc_context(nature.settings(family="DejaVu Sans")):
        fig, axes = plt.subplots(1, 2, figsize=nature.figure_size("double", height_mm=64),
                                 layout="constrained")
        labels = nature.label_panels(axes)
        assert [t.get_text() for t in labels] == ["a", "b"]
        assert all(t.get_fontsize() == 8 and t.get_fontweight() == "bold" for t in labels)
        fig.savefig(tmp_path / "nature.svg")
        plt.close(fig)
    root = ET.parse(tmp_path / "nature.svg").getroot()
    assert list(map(float, root.attrib["viewBox"].split()))[2:] == pytest.approx([183/25.4*72,64/25.4*72])
    assert any(t.text == "a" for t in root.iter("{http://www.w3.org/2000/svg}text"))
    assert nature.figure_size("single")[0] * 25.4 == pytest.approx(89)


@pytest.mark.parametrize("size", [4.9, 7.1, float("nan"), float("inf")])
def test_rejects_outside_ordinary_text_range(size):
    with pytest.raises(ValueError):
        nature.settings(font_size=size)


@pytest.mark.parametrize("height", [0, -1, 171, float("nan")])
def test_rejects_outside_height_range(height):
    with pytest.raises(ValueError):
        nature.figure_size(height_mm=height)
