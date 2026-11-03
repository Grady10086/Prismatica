---
name: prismatica
description: >-
  Unified scientific visualization workflow combining paper-colors with
  scientific-figure-making. Use for research data charts, experimental panels,
  method overviews, teasers, palettes, final-size layout and vector export.
  Coordinates the bundled modules without changing experimental results.
license: MIT
---

# Prismatica

Coordinate the two bundled sibling skills. They are installed together by the
repository installer; do not copy this entrypoint alone. Read only the references
relevant to the requested output.

## Combined workflow

1. Read [scientific-figure-making](../scientific-figure-making/SKILL.md) for the
   common layout, data-integrity and export workflow. Establish the intended
   claim, input data/assets, venue dimensions and deliverable type.
2. Read [paper-colors](../paper-colors/SKILL.md) when choosing, changing or
   checking colors. Reuse the project's registered theme or exported palette;
   color-book data stays in the user's own data directory. Never infer a book
   code from an approximate screenshot or recollection.
3. Choose the composition below. Data experiments use manuscript-sized charts;
   a method overview uses actual components; teasers use actual result assets.
4. Apply colors by semantic role. Preserve run/item pairing, statistical units,
   uncertainty definitions, category order, metric directions and all results.
   A brand palette is not automatically a suitable multi-series data palette.
5. Export editable SVG/PDF plus PNG. Inspect the result at insertion size and
   check grayscale/series distinguishability. Explain remaining limitations.
6. Deliver source code, provenance and the definition of every uncertainty
   interval. Distinguish synthetic fixtures, local demo experiments, published
   numerical redraws and original paper excerpts.

## Composition routes

| Output | Reference |
| --- | --- |
| CS training, alignment, diffusion evaluation | [Paper data](../scientific-figure-making/references/cs-paper-data.md) |
| Ablations, condition conflicts, sampler quality/cost | [Paper comparisons](../scientific-figure-making/references/cs-paper-comparisons.md) |
| All statistical/complex charts: clustering, correlation, Sankey, spatial, survival, ROC/PR | [Full catalog](../scientific-figure-making/references/gallery-catalog.md) |
| Method overview / central loop / mechanism details | [Overview](../scientific-figure-making/references/trinity-overview.md) |
| Benchmark radial bars, iterations and correlation matrices | [Benchmark figures](../scientific-figure-making/references/trinity-paper.md) |
| Model internals and diagnostic compositions | [Analysis](../scientific-figure-making/references/cs-analysis.md), [diagnostics](../scientific-figure-making/references/cs-diagnostics.md) |
| Image-led multimodal, video, 3D and robotics teasers | [CS editorial](../scientific-figure-making/references/cs-editorial.md), [sequences](../scientific-figure-making/references/sequence-teasers.md) |
| Published multimodal and diffusion reference layouts | [Multimodal](../scientific-figure-making/references/multimodal-diffusion.md), [recent](../scientific-figure-making/references/recent-multimodal.md) |
| Optional Nature profile | [Nature](../scientific-figure-making/references/nature.md) |

For existing figures, preserve the project's code-native representation and data
loading. The galleries are reference implementations, not a reason to replace
real inputs with fixture data. Keep original author/source attribution when
using published examples. Never fabricate intermediate frames or significance.

## Color and layout handoff

Keep the sibling folder names unchanged: historical example imports rely on
that layout. `paper-colors` owns color selection/export and `scientific-figure-making`
owns composition/export. Their independent entrypoints remain usable. Refer to
the skill scripts by their resolved installed paths rather than a developer's
local absolute paths.
