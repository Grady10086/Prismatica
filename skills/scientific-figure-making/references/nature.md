# Nature figures: sources, scope and practical patterns

Checked 2026-10-26. This is an optional profile for Nature main figures, not an
assertion that every Nature Portfolio journal uses the same specifications.
Check the target journal, article type, submission stage and editor's instructions.
The general scientific-figure-making defaults remain unchanged.

## Official requirements used by the profile

| Property | Nature main-figure guidance | Implementation |
|---|---|---|
| Width | Single 89 mm; double 183 mm | `figure_size(column)` |
| Height | Figure guide gives 170 mm to leave caption room | `height_mm`, capped at 170 |
| Ordinary text | 5–7 pt, sans serif; Arial/Helvetica preferred | Default 7 pt; installed font selection |
| Panel letters | 8 pt, bold, upright lowercase | `label_panels(axes)` |
| Lines | 0.25–1 pt at final size | Defaults 0.6 pt axes, 0.8 pt data |
| Vector text | Editable text, embedded fonts, no outlines | PDF Type 42, SVG text |

Sources: [Nature final submission](https://www.nature.com/nature/for-authors/final-submission),
[figure construction](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/),
[figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/).
The final-submission page's 247 mm is page depth; it is not the ordinary figure
height target. The figure guide recommends 170 mm to reserve caption space.
Neither this profile nor PDF export alone guarantees acceptance or editability
in every production application. Check fonts and the actual exported artifact.

The figure guide favours axes/ticks, labels with parenthesized units, accessible
colors and black text with graphical keys. It discourages grid backgrounds,
decorative effects, busy labels and pattern fills. Keep original scientific images
and image-integrity requirements separate from plot styling. For dense plots,
retain marker/dash redundancy where needed for accessibility; do not introduce
hatches automatically. Do not assume a Pantone theme is automatically color-safe.
Audit the chosen theme using paper-colors.

Main-figure vector exports and Extended Data have different delivery rules.
PDF is a preferred main-figure delivery format; PNG examples here are previews.
The figure guide describes different image-resolution recommendations in its
photography and export sections (300 dpi minimum for photos; 450 dpi for image
export). This profile uses 450 dpi for raster layers/previews, while keeping plot
lines and text vector. Recheck the target's instructions for Extended Data rather
than delivering the preview automatically.

## What we learn from Nature Methods visual examples

These are design recommendations, not additional Nature submission requirements:

- **Layout expresses the comparison.** Group related panels and align repeated
  axes; use equal scales only for equal quantities. Allocate more space to a
  dense panel rather than making all panels equally small. The before/after
  examples in Wong's [Points of review (part 1)](https://www.nature.com/articles/nmeth0211-101)
  make hierarchy and reading order explicit.
- **Show the measured distribution.** For replicate measurements, prefer visible
  observations with a declared summary, or a box plot, over a bar that hides the
  distribution. Preserve paired observations with connecting lines when pairing
  is part of the design. This implements the data/task distinction in Streit and
  Gehlenborg's [Bar charts and box plots](https://doi.org/10.1038/nmeth.2807)
  ([author's article page and figure](https://hidivelab.org/publications/gehlenborg-2014-nature-bar-box/)).
- **Make visual emphasis follow the question.** Use concise labels and aligned
  panels, with the same method color across plots. Avoid automatic thick emphasis
  for ours when using Nature's 1 pt upper line-weight guidance; distinguish it
  with role color, drawing order or markers instead.

The Nature Methods [Points of View collection](https://blogs.nature.com/blog/tag/points-of-view/)
provides further routes for layout, negative space, labels and salience. No
published artwork or measured results are copied into this repository. The
included example uses original synthetic data to demonstrate these choices.

## Using the profile

Copy `scripts/nature_profile.py` and `scripts/paper_layout.py` beside the project's
plotting script. With an existing `paper_colors.py` export:

```python
import matplotlib.pyplot as plt
import nature_profile as nature
import paper_layout as layout
import paper_colors as colors

nature.apply()  # replaces general layout settings; does not call layout.apply()
colors.apply()  # palette only; do not hard-code a new Nature color palette
fig, axes = plt.subplots(1, 2, figsize=nature.figure_size("double", height_mm=65),
                         layout="constrained")
# Plot real data with explicit linewidth <= 1 pt; errorbar widths also need checking.
nature.label_panels(axes)
print(layout.inspect(fig, min_font_size=5))
layout.save(fig, "figures/main", dpi=450)
```

Use the 5 pt check threshold with this profile, not the generic helper's 7 pt
threshold. Panel labels are intentionally larger than ordinary text. Review the
export for maximum text/line size, panel label alignment, overlaps, clipping,
legend contrast and final inclusion width; the inspector does not enforce all
Nature requirements. If Arial/Helvetica is absent, the helper warns and uses
DejaVu Sans for preview; choose an installed journal-approved font for delivery.

Run the synthetic demonstration from the repository root:

```bash
uv run --with matplotlib python skills/scientific-figure-making/examples/nature_panels.py --out /tmp/beautify-nature
```
