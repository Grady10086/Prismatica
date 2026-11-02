# Multimodal and diffusion reference compositions

Three image-driven experimental layouts from published author outputs, with no model inference or fabricated benchmark scores. Supply local source PDFs; paper images are not bundled in the skill or relicensed under the repository license.

```sh
uv run --with matplotlib --with pymupdf python skills/scientific-figure-making/examples/multimodal_diffusion_gallery.py \
  --llava /absolute/Visual-Instruction-Tuning.pdf \
  --instruct /absolute/InstructPix2Pix.pdf \
  --ptp /absolute/Prompt-to-Prompt_preprint.pdf \
  --out /tmp/multimodal-diffusion
```

Exports three PNGs, editable-text SVGs with embedded raster source images, and `source-record.json` recording source PDF hashes, page numbers, image xrefs, dimensions and page coordinates. It sorts image placements by page position rather than assuming PDF object order. Count/dimension checks catch some incompatible editions; always verify against the original figure, especially labels and row/column identity.

## Layouts

**Multimodal response audit.** One large photographic input and a column of four concise response cards. Source: [LLaVA / Visual Instruction Tuning](https://llava-vl.github.io/), PDF page 6, Table 3. All four responses correspond to the same unusual-scene question; card text is explicitly a paraphrase of the published answer, not a new model response or direct quotation. Teal/coral colors separate the displayed response summaries, not calibrated correctness scores. This is one selected qualitative example and supports no aggregate ranking. The original photograph has a separate source listed in the paper; preserve that provenance when reusing it.

**Diffusion control atlas.** Dark page, a large featured edit, all nine image/text guidance combinations and a separate five-method comparison strip. Source: [InstructPix2Pix](https://arxiv.org/abs/2211.09800), PDF pages 5 and 7, Figs. 4 and 9. Grid rows are image guidance 1.0, 1.2, 1.6; columns are text guidance 3, 7.5, 15. Featured image is the central cell. The comparison strip is the first source row in Fig. 9: input, SDEdit conditioned on caption, Text2Live, SDEdit conditioned on edit, InstructPix2Pix. Caption-conditioned and instruction-conditioned methods receive different textual inputs; retain that distinction. The strip uses a different image/edit from the guidance study. No quality score or global method winner is inferred.

**Diffusion process attention study.** Large synthesized image, six token maps and nine original ordered maps across diffusion steps. Source: [Prompt-to-Prompt](https://prompt-to-prompt.github.io/), [project PDF](https://prompt-to-prompt.github.io/ptp_files/Prompt-to-Prompt_preprint.pdf), page 5, Fig. 4. Top maps are averaged over steps; bottom maps show the word bear over time. Preserve original 16×16 map pixels and published colors using nearest-neighbor display. These are cross-attention maps, NOT decoded denoising states. The original caption describes samples from T=250 to 1 at equal intervals; the layout uses sample ordinals rather than inventing rounded timestep labels. Raster colors cannot recover exact normalized weights; do not add a numeric colorbar. Attention does not prove causal localization.

For a paper with actual inference artifacts, reuse the composition while replacing every image, response and label consistently. A denoising storyboard requires decoded intermediates from one logged seed, prompt, scheduler and timestep sequence; never synthesize a process by adding noise to a final image. Use source credits and applicable image reuse terms when distributing published material. Wide editorial previews need venue-sized typography before use in a manuscript.
