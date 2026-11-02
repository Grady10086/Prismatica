# Recent multimodal/diffusion evidence layouts (2025)

Use `examples/recent_multimodal_gallery.py` for a recorded-generation storyboard, cross-modal evidence board and correction-failure atlas. These are reference compositions of published author results, not new inference. Local source PDFs are required and published pixels are not distributed with the skill.

```sh
uv run --with matplotlib --with pymupdf python skills/scientific-figure-making/examples/recent_multimodal_gallery.py \
  --asced /absolute/asced.pdf --mir /absolute/mir.pdf --flow /absolute/flow.pdf \
  --out /tmp/recent-multimodal
```

Requires the sibling helper `multimodal_diffusion_gallery.py`. Outputs PNG, editable-text SVG containing raster source panels, and a source record with PDF hashes, original pages, bounding boxes/xrefs and source URLs. The script checks image count and bounds, but PDF editions can differ: manually verify all crops and labels against the actual source pages. Original source plots remain raster, not editable/recomputed data.

## Sources and composition

1. [Cao et al., Temporal Score Analysis for Understanding and Correcting Diffusion Artifacts, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/html/Cao_Temporal_Score_Analysis_for_Understanding_and_Correcting_Diffusion_Artifacts_CVPR_2025_paper.html). Fig. 1 on PDF p1 provides four independent rows of nine published generation snapshots. The storyboard preserves row and column order and uses the final image of row four as its hero. Profiling/mutation/refinement groups are the authors’ phase interpretation, not newly estimated transition times. The source provides selected states with omissions between phase groups; do not call them all consecutive timesteps or invent scheduler/seed/timing labels. Native 256×256 image objects are extracted; the page’s vector annotation boxes and ellipses are not copied onto these images. The source’s final two rows illustrate artifact-producing cases. This is recorded generation evidence, unlike adding noise to a final image to imitate denoising.
2. [Huang et al., Deciphering Cross-Modal Alignment … via Modality Integration Rate, ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Huang_Deciphering_Cross-Modal_Alignment_in_Large_Vision-Language_Models_via_Modality_Integration_ICCV_2025_paper.pdf). Fig. 2 on PDF p2 supplies a visual/text token distribution projection and modality-gap plot. Colors are original, with interpretation in the paper caption; do not infer pairwise correspondences or causal integration from projected separation alone.
3. [Zhang et al., Cross-modal Information Flow in Multimodal Large Language Models, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhang_Cross-modal_Information_Flow_in_Multimodal_Large_Language_Models_CVPR_2025_paper.pdf). Fig. 1 on PDF p1 is an illustration summarizing attention-knockout findings. Keep its visual input, arrows and labels intact. It is not a measured per-example flow map. The alignment board explicitly separates this study from MIR; their panels do not share a dataset or measurement scale.

The failure atlas uses ASCED Figs. 5 and 6 on PDF p7. The large left source panel includes the original, SARGD, state-replacement and the paper’s own method. “Ours” refers to the paper authors, never the user or this skill. Right panels show the paper’s false positives, false negatives and typical correction failures. Preserve the yellow source boxes and native method labels. These author-selected examples do not establish failure rates or overall method rankings.

For user research, replace all source assets/credits with actual logged outputs, retaining within-case identity and known timestep order. Store decoder settings, seed, scheduler and timestep indices if available. Keep independent experiments explicitly separated. Use comparable crop/display settings for before/after results and disclose example selection. Do not manufacture missing intermediate states, alignment values or corrected outputs. Check applicable source-image reuse terms before redistribution; figures embedded in a paper are not automatically covered by its code license.
