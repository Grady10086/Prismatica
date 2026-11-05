---
name: scientific-figure-making
description: >-
  Create and refine scientific figures with Matplotlib: manuscript data plots,
  experimental composites, method overviews and image-led research teasers.
  Use for final-size typography, uncertainty, panel layout, vector export and
  visual review. Preserve experimental results; use paper-colors for palettes.
license: MIT
---

# Scientific figure making

For the combined palette + composition workflow, use the sibling
[Prismatica entrypoint](../prismatica/SKILL.md). This module remains independently usable.

## Workflow

1. Identify the scientific claim, available data/assets and output venue. For
   manuscript experiments choose compact data plots, not an editorial poster.
2. Preserve values, units, pairing, sample identities and missing observations.
   Define the experimental unit and whether uncertainty is SD, IQR, SEM or CI.
   Synthetic examples are fixtures, never reportable research results.
3. Choose the relevant reference below. For generic manuscripts start at
   85 mm single-column / 178–180 mm double-column and 7–8 pt text, then honor
   the actual venue template. Nature settings are a separate optional profile.
4. Use `scripts/paper_layout.py` for final dimensions, typography, `inspect` and
   PDF/SVG/PNG export. Apply an existing palette; sibling `paper-colors` can
   generate compatible themes. Never shrink text simply to fit more panels.
5. Render and inspect the preview at the final insertion size. Check clipping,
   labels, legends, line/marker distinguishability and linked image crops.
   `inspect` catches some text problems, not all collisions or scientific errors.
6. Deliver the figure, reproducible code, input provenance and statistical
   definitions. Do not invent missing results, significance or model outputs.

## Choose a mode

| Need | Read |
| --- | --- |
| Manuscript CS experiments: training, alignment, reconstruction | [CS paper data](references/cs-paper-data.md) |
| Factorial ablation, modality conflict, sampler cost | [CS paper comparisons](references/cs-paper-comparisons.md) |
| General layout, editable export, final-size review | [Layout](references/layout.md) |
| Atmospheric warm–cool composition, focal detail and asymmetric balance | [Landscape aesthetic reference](references/atmospheric-composition.md) |
| Architectural framing, material contrast and editorial hierarchy | [Architectural aesthetic reference](references/architectural-composition.md) |
| Generative method/teaser aesthetics: state, light, point samples | [Gamma, SKALAR, Pointillisme studies](references/generative-art-studies.md) |
| Nature production profile and source distinctions | [Nature](references/nature.md) |
| Biological data: OncoPrint, spatial omics, annotated trees, genomic Circos, Sashimi | [Bioinformatics](references/bioinformatics.md) |
| Set overlaps, flower/petal summaries, Venn/Euler, UpSet, Jaccard | [Set overlap](references/set-overlap.md) |
| Statistical plot families and complex compositions | [Gallery catalog](references/gallery-catalog.md#rich-statistical-compositions) |
| CS model analysis and diagnostic examples | [Analysis](references/cs-analysis.md), [diagnostics](references/cs-diagnostics.md) |
| Method overview with scope, mechanisms and evidence | [Trinity overview](references/trinity-overview.md) |
| Benchmark-wide iterations, radial bars, correlations | [Trinity data reference](references/trinity-paper.md) |
| Image-first CS teasers with ordered results | [CS editorial](references/cs-editorial.md), [sequences](references/sequence-teasers.md) |
| Quantitative multimodal and diffusion plates | [Computed retrieval, conflict and sampling studies](references/multimodal-quantitative.md) |
| Multimodal / diffusion published reference studies | [Multimodal](references/multimodal-diffusion.md), [recent studies](references/recent-multimodal.md) |
| Curated visual examples with reproducible arrays | `examples/showcase_gallery.py` and `examples/advanced_showcase.py` (multi-track, representation and flow compositions); gallery-sized masters, resize typography for a venue |
| Full example commands and specialized chart references | [Gallery catalog](references/gallery-catalog.md) |

Read only the relevant branch. Scientific data plots take priority over teaser
styling when the user asks for an experimental figure.

## Provenance boundaries

- Original synthetic templates, actual local demo-model results, published-data
  redraws and original-paper excerpts are distinct output types. Label them.
- Paper reference tools accept local source PDFs; do not distribute original
  paper images under this repository's MIT license. Preserve authorship and
  source identifiers. “Ours” inside a source panel means its paper's authors.
- Do not fake denoising by adding noise to final outputs, invent sequence timing,
  or interpret attention/projection geometry as causal evidence.
- Retain split denominators, negative outcomes, retrospective Oracle status and
  per-sample matching. Use a paired or clustered resampling unit when warranted.

## Minimal use

```python
import matplotlib.pyplot as plt
import paper_layout as layout  # copy from this skill's scripts directory

layout.apply(font_size=8)
fig, ax = plt.subplots(figsize=layout.figure_size("single"), layout="constrained")
ax.plot(steps, accuracy, marker="o", label="Method A")  # user's actual arrays
ax.set(xlabel="Training step", ylabel="Accuracy (%)")
ax.legend()
print(layout.inspect(fig))
layout.save(fig, "figures/accuracy")
```

From the repository root, a synthetic fixture smoke run is:

```sh
uv run --extra science python skills/scientific-figure-making/examples/cs_paper_data_gallery.py --out /tmp/paper-data
```

`save` preserves the requested canvas dimensions; avoid subsequent resizing that
silently changes text size. SVG text remains editable; receiving systems need
its fonts. The full package includes optional sibling `paper-colors` so the
historical galleries and tests retain their expected relative imports.
