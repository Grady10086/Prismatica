# Data figures informed by Nature Portfolio papers

Checked 2026-10-26. This extends the existing [Nature profile](nature.md) from
canvas/typography to **data presentation**. It is not a universal Nature palette,
a submission-compliance certificate or a requirement for other venues.

Separate three things: the target journal's current production instructions,
statistical meaning, and a paper author's layout choices. A published figure is
not permission to copy every choice. For instance, direct colored labels occur
in some papers, whereas the current Nature figure guide requests black text with
visual keys. Follow the applicable target instructions for delivery.

## Primary-paper casebook: figures visually inspected

| Journal / paper | Inspected panels | What transfers |
| --- | --- | --- |
| Nature — [AlphaFold 3](https://www.nature.com/articles/s41586-024-07487-w) (2024) | Fig. 1c, PDF p. 2; Fig. 2d, p. 3 | Benchmark groups with explicit sample sizes and uncertainty; training trajectories grouped by output type and marked training stages. Structural examples, charts and architecture have distinct panel roles. |
| Nature Methods — [Cellpose3](https://www.nature.com/articles/s41592-025-02595-5) (2025) | Fig. 1d,f,j, PDF p. 2; Fig. 2c,e, p. 3 | Matched per-image comparisons around an identity line; performance versus threshold; common conditions and small multiples placed near qualitative evidence. |
| Nature Machine Intelligence — [Clever Hans effects in unsupervised learning](https://www.nature.com/articles/s42256-025-01000-2) (2025) | Fig. 3, PDF p. 4; Fig. 4, p. 5; Tables 1–2 | Diagnostics connect image evidence and quantitative contributions. A contribution histogram has a different meaning from an uncertainty interval or an accuracy chart. |
| Nature Communications — [Sufficient is better than optimal for training neural networks](https://www.nature.com/articles/s41467-025-66983-3) (volume 17, 271; 2026, first online 2025) | Figs. 1–3, PDF pp. 3–5 | Training behavior, raw observations, ensemble distributions and aggregate performance occupy different panels; observed ensemble members are visually distinguished from an aggregate. |

Important distinctions from these examples:

- AlphaFold 3's benchmark uncertainties vary by task and include binomial and
  bootstrap confidence intervals. Do not restyle them as SD. Its training-curve
  threshold marks are not error bars.
- Cellpose3's Fig. 2 legend specifies SEM for particular image-based comparisons.
  Images are the units in those panels; pixels do not automatically become
  independent replicates.
- Ensemble-member spread, uncertainty of an estimated mean and variability between
  independently trained models answer different questions. The Nature
  Communications comparison motivates showing members and aggregate separately;
  our synthetic SD demonstration is not a reproduction of its ensemble analysis.
- In the NMI case, image explanation overlays are computed scientific results.
  Styling cannot create or repaint them to suggest a different explanation.

The repository contains no extracted publication data or image assets. The
included examples use new, explicitly synthetic data and do not reproduce paper
measurements, significance claims or model performance.

## Production and statistical references

Current [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
cover axis lines/ticks, units, accessible color, standard fonts, editable vector
artwork, ordinary text sizes and panel letters. Use `nature_profile.py` for the
optional 89/183 mm width profile and review the target journal's instructions.

Further statistical reading, separate from this pass's visually inspected research
figures: Nature Methods [Error bars](https://www.nature.com/articles/nmeth.2659),
[Visualizing samples with box plots](https://www.nature.com/articles/nmeth.2813),
and Nature Biomedical Engineering [Show the dots in plots](https://www.nature.com/articles/s41551-017-0079).
These are background references, not a reason to label every interval a CI.

## Six data-chart primitives

Helpers live in `scripts/nature_charts.py`. They draw on an existing matplotlib
axes; the caller controls layout, colors, units and the experimental design.
Apply `nature_profile` before constructing axes, then the existing paper-colors
export. The helpers do not change global rcParams or decide a significance test.

| Helper | Encodes | Required interpretation |
| --- | --- | --- |
| `comparison` | Raw observations, mean ± sample SD | SD uses `ddof=1`; not SEM or a confidence interval. Preserve supplied method order. |
| `training` | Individual unsmoothed runs, mean ± pointwise SD | Arrays are `[independent runs, shared observed steps]`; no inferred alignment, smoothing or missing-step interpolation. |
| `ablation` | Mean paired variant-minus-full differences | Arrays are `[condition, dataset, matched unit]`; zero-centered, fixed symmetric color limits. Missing cells are `NA`, not zero. |
| `distribution` | Raw dots, violin density, median/IQR box | Whiskers use 1.5 IQR; all outliers remain in raw dots. KDE only for nonconstant samples with n ≥ 10; it is not uncertainty. |
| `paired` | Lines linking the same units | Pairing must come from identifiers/design, not array length or sorting. No automatic p-values or causal claim. |
| `pareto` | Observed latency–score operating points | Minimize latency, maximize score. Dashed links are a visual guide, not an interpolated frontier measurement or significance statement. |

The distribution helper uses a display-only fixed jitter seed. It never alters
y-values, deletes points, truncates tails, normalizes measurements or filters
outliers. For nested biological/technical observations, define the independent
unit and appropriate aggregation/model outside these primitives. A count of dots
is not automatically the inferential sample size.

Ablation and Pareto diagrams are our original adaptations for common ML data;
they are not claimed to be exact copies of a cited Nature panel. If a measured
heatmap mean exceeds the requested color limit, the helper stops rather than
silently saturating the result. Use the same limits across comparable heatmaps.
Pareto comparisons require matched hardware, batch size, precision and workload;
record those in the caption or source metadata.

If the user needs SEM, bootstrap intervals or another uncertainty representation,
compute it from the declared experimental design and plot the actual endpoints.
Do not substitute the helpers' default SD or fabricate replicates from an aggregate.

## Reproducible gallery

From the repository root:

```bash
uv run --with matplotlib python skills/scientific-figure-making/examples/nature_data_gallery.py \
  --demo --out /tmp/nature-data
```

This produces six individual **89 × 68 mm** SVG/PNG figures and an original
**183 × 140 mm** six-panel composition, plus `input-data.json`, computed summaries,
statistical captions and the synthetic fixture palette export. Every preview is
visibly marked synthetic. SVG text stays editable; 450 dpi PNGs are review copies.
Do not assume SVG text embeds the font; keep the requested font available.

To render a compatible real-data bundle:

```bash
uv run --with matplotlib python skills/scientific-figure-making/examples/nature_data_gallery.py \
  --data /path/to/project-data.json --colors /path/to/paper_colors.py \
  --out /path/to/figures
```

Start from the demo's `input-data.json` structure, replace all observations and
metadata, and set `kind` to `PROJECT DATA`. This gallery uses percentage scores,
percentage-point differences, steps in thousands and latency in milliseconds.
For other metrics, use the primitives directly and provide correct axis labels;
do not just put arbitrary values into this bundle. The CLI keeps the source JSON
and computed summaries beside the figures.

- `roles` maps method names to paper-colors role numbers; one method keeps the
  same color/marker identity across all panels.
- Comparison, training, distribution, paired and ablation sections each declare
  their observational `unit`.
- `paired.records` contains unique `id`, `before` and `after` fields. Do not pair
  units by sorting outcome values.
- Ablations provide `full_runs[dataset, run]`,
  `variant_runs[condition, dataset, run]` and unique matching `replicate_ids`.
  The gallery computes differences from those observations, not supplied means.
  Use JSON `null` for unmeasured variant cells.
- The demo is opt-in via `--demo`; running without `--demo` or `--data` is rejected.
  The default palette is a synthetic test fixture; use `--colors` for a project
  palette. Neither the style nor the palette implies journal endorsement.

For a single chart, reading a CSV and passing its verified arrays directly is
simpler than assembling all six sections:

```python
import matplotlib.pyplot as plt
import nature_profile as nature
import nature_charts as charts
import paper_colors as colors

nature.apply()
colors.apply()
styles = {'Method A': colors.style(0, redundant=True),
          'Method B': colors.style(1, redundant=True)}
fig, ax = plt.subplots(figsize=nature.figure_size('single', height_mm=65),
                       layout='constrained')
# arrays must be actual independent units from the user's data
summary = charts.comparison(ax, {'Method A': runs_a, 'Method B': runs_b},
                            styles, xlabel='Accuracy (%)')
# Save summary, sample sizes and interval definition beside the plot.
fig.savefig('comparison.svg')
```

Review the exported figure at its intended insertion width: panel alignment,
clipping, text, shared method identity, scale limits and uncertainty semantics.
Multi-panel charts should form an evidence sequence, not a collection of unrelated
plot types. Do not infer scientific validity from a clean visual layout.
