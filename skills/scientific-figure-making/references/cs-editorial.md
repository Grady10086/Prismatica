# Image-led editorial layouts for CS research

Use these compositions for computer vision, generative models and robotics when a user wants a polished, image-first teaser or talk slide. Large serif headlines, restrained rules and asymmetrical image hierarchy are presentation choices; use the skill’s publication profile for manuscript-sized typography.

## Three compositions

- **Video cinema**: one large published output, a separate input still, a linked detail crop and four ordered output samples. Inspired by [DynamiCrafter, ECCV 2024](https://doubiiu.github.io/projects/DynamiCrafter/), Fig. 4. Never infer elapsed time or generate intermediate frames from the four samples.
- **Object stage**: a large reconstructed mesh, matching input, textured reconstruction and generated normal views, plus a separate object gallery. Uses [Wonder3D, CVPR 2024](https://www.xxlong.site/Wonder3D/), Fig. 1. Keep the original alpha masks. Normal views, input images and reconstructed geometry have distinct meanings; gallery objects are independent examples.
- **Robot sequence**: a large manipulation observation, a vertical selection of the same task’s samples, and a horizontal second-task sequence. Uses [Physical Intelligence π₀](https://www.pi.website/blog/pi0), original report Figs. 6 and 10. Keep original order; do not add contact labels, inferred trajectories, timestamps or success scores.

These are credited studies of published results, not new experiments or model inference. The original paper images are not distributed as MIT-licensed skill assets. Supply local copies of the source PDFs; retain attribution and check applicable image reuse terms before publishing a derivative figure.

## Reproduce

From the repository root, with local source PDFs:

```sh
uv run --with pymupdf python skills/scientific-figure-making/examples/prepare_sequence_references.py \
  --dynamicrafter /absolute/DynamiCrafter.pdf \
  --wonder3d /absolute/Wonder3D.pdf \
  --pi0 /absolute/pi0.pdf --out /tmp/cs-source
uv run --with matplotlib python skills/scientific-figure-making/examples/cs_editorial_gallery.py \
  --source-dir /tmp/cs-source --out /tmp/cs-editorial
```

The preparer checks the expected paper asset dimensions and records PDF provenance. The renderer validates image dimensions and crop bounds, preserves aspect ratios, and exports PNG, editable-text SVG and a source-map JSON with asset hashes, original metadata, crops and sample order. Raster source images remain raster within SVG.

For a user’s own results, adapt the manifests and labels to their actual assets and provenance. Replace the published project names and credits consistently; never present these reference outputs as the user’s experiments. Inspect every rendered layout at full size, especially tall robot frames, whose native aspect ratios can intrude into the title area.
