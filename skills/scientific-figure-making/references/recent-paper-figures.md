# Recent award papers and model-report figures

Verified 2026-10-26. This casebook extends the earlier teaser references with
**2025–2026 conference editions**, not only older model papers. Twelve papers
cover CVPR, ICCV, SIGGRAPH, RSS, CoRL, ICLR, NeurIPS and ICML, plus one selected
video-model report. It is a curated visual reference, not an exhaustive awards
list, a citation ranking, or a claim that awards measure graphic design quality.

Read the actual figure before adapting its layout. The observations below were
checked on rendered PDF pages. Adaptation advice is our editorial interpretation;
it is not a statement by the original authors.

## What was inspected

The [machine-readable catalog](recent-paper-figures.json) contains exact primary
PDF URLs, one-based pages, figure labels, normalized excerpt bounds, official
award sources, visual observations and adaptation limits.

| Paper | Conference edition / status | Inspected visual evidence |
| --- | --- | --- |
| VGGT | CVPR 2025 Best Paper | Fig. 1, p. 1: dominant scene reconstruction with compact matching inputs and diagnostic outputs |
| D4RT | CVPR 2026 Best Paper | Fig. 1, p. 1 and Fig. 4, p. 5: dynamic geometry/trajectory context and aligned reconstruction comparisons |
| Native and Compact Structured Latents for 3D Generation | CVPR 2026 Best Student Paper | Fig. 1, p. 1 and Figs. 5–6, p. 7: geometry/material passes, large assets, smaller views and compact quantitative evidence |
| BrickGPT | ICCV 2025 Best Paper / Marr Prize | Fig. 1, p. 1: construction stages, physical assembly photos and a separate result gallery |
| FEAST | RSS 2025 Outstanding Paper Award | Fig. 1, p. 1: contextual deployment photos alongside a smaller study/design rationale |
| Fabrica | CoRL 2025 Best Paper | Fig. 1, p. 1: ordered real dual-arm assembly samples across three tasks |
| SAM 2 | ICLR 2025 Honorable Mention | Fig. 2, p. 4 and Fig. 4, p. 8: synchronized interaction/correction rows and video masklet examples |
| CAST | SIGGRAPH 2025 Best Paper | Fig. 1, p. 1: varied scenes in a coherent elevated-view gallery |
| TokenVerse | SIGGRAPH 2025 Best Paper | Fig. 1, p. 1: small concept references above larger composed outputs |
| Gated Attention | NeurIPS 2025 Best Paper | Fig. 2, p. 3: summary curves aligned with actual attention matrices |
| Score Matching with Missing Data | ICML 2025 Outstanding Paper | Fig. 1, p. 7: a compact comparison with visible uncertainty intervals |
| Wan | Selected 2025 model report; no award claimed | Fig. 20, p. 29 and Fig. 23, p. 33: ordered output samples across subjects and conditioning tasks |

Awards were checked against the official
[CVPR 2025 announcement](https://cvpr.thecvf.com/Conferences/2025/News/Awards_Press),
[CVPR 2026 announcement](https://cvpr.thecvf.com/Conferences/2026/News/Best_Papers),
[CVF awards list](https://www.thecvf.com/?page_id=413),
[RSS Foundation](https://roboticsfoundation.org/awards/best-paper-award/),
[CoRL 2025 awards](https://2025.corl.org/program/awards),
[ICLR 2025 announcement](https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/),
[SIGGRAPH 2025 announcement](https://blog.siggraph.org/2025/06/siggraph-2025-technical-papers-awards-best-papers-honorable-mentions-and-test-of-time.html/),
[NeurIPS 2025 announcement](https://blog.neurips.cc/2025/11/26/announcing-the-neurips-2025-best-paper-awards/)
and [ICML 2025 awards](https://icml.cc/virtual/2025/awards_detail).
RSS's award listing uses a slightly different FEAST subtitle; the catalog keeps
the title printed in the inspected proceedings PDF.

## Choose a composition by its evidence

| Claim / evidence | Reference | Practical adaptation |
| --- | --- | --- |
| One scene with several spatial predictions | VGGT | Make the actual reconstructed scene dominant; place corresponding input, depth and tracks nearby at smaller scale. Keep connections selective. |
| Geometry plus materials | Native 3D | Match a large textured asset with real normals/material passes and a few alternative views. A small efficiency plot needs actual measurements. |
| Generation physically realized | BrickGPT | Give rendered output and actual fabrication/execution different visual roles. Use short assembly samples and a separate diversity gallery. |
| Real deployment in different contexts | FEAST | Preserve people, surroundings and interaction context. The robot need not occupy every close-up. Retain privacy treatment. |
| Contact-rich manipulation | Fabrica | Select samples that expose grasp, insertion and assembly transitions. Align task rows; do not spend half the strip on idle poses. |
| Several reference concepts combined | TokenVerse | Small conditioning images above large outputs; sparse color cues link concepts to results. Keep the real conditioning relationship intact. |
| Interactive refinement over time | SAM 2 | Align before/after rows to the same shown video positions; explicitly mark prompt/correction locations and preserve identity colors. |
| Diverse generated motions | Wan | Multiple subjects, consistent within-sequence sampling and image-dense strips. Prompt prose can move to the paper caption. |
| Many related scenes | CAST | Consistent view convention supports a scene gallery, but a repeated box-like visual subject is not appropriate to unrelated tasks. |
| Mechanism or quantitative claim | Gated Attention; Score Matching | Use aligned curves/maps or readable uncertainty plots. These are analysis references, not photo-teaser presets. |

These are references for composition decisions, not eleven new hard-coded presets.
The existing [result layouts](result-first-teasers.md) and
[sequence layouts](sequence-teasers.md) cover several nearby structures. Adapt
native SVG when the evidence calls for a different number of rows, a concept rail,
a material breakdown or a contextual deployment collage. Do not force a reference
into the existing three-method proofsheet or reinterpret task rows as methods.

A teaser usually needs one main visual claim. It need not show the full system
architecture. Keep only short task labels, method identities, sequence order,
necessary legends and attribution on the canvas. Put protocols and qualifications
in captions/provenance. Do not remove scientifically necessary legends merely to
reduce text, or add an invented graph to make the composition look balanced.

## Build the local visual atlas

Save the primary PDFs locally using the catalog's `pdf_file` names. No PDF or
publication image is shipped in this repository. Run from the repository root:

```bash
uv run --with pymupdf python skills/scientific-figure-making/examples/build_reference_atlas.py \
  --pdf-dir /path/to/local-pdfs --out /tmp/recent-paper-atlas
```

Open `index.html` in a browser. Search by paper, conference or visual tags, and
switch between teaser/results and quantitative-analysis references. Every card
links the original paper and the official award announcement, and separates
observations from suggested adaptations. Clicking the figure opens its full
excerpt. The generator does not access the network.

The atlas records source PDF hashes, page numbers and crop bounds. Excerpts are
faithful rasterizations of source regions, not redrawn experiments. If a PDF
edition changes, inspect the page and adjust the crop instead of assuming the
same figure location. Keep original aspect ratios and inspect the excerpt edges.

The local atlas is study material, not a freely reusable image library. Paper
access and conference acceptance do not establish asset reuse permission. Retain
original author credit and asset-specific terms; use owned/licensed images for
new project results. Never imply a published result was generated by this skill.
