# Result-first teasers with actual imagery

Use this workflow when a user wants a refined image-led teaser, or finds the
vector teaching diagrams too generic. Start with real project inputs, qualitative
outputs and measured evidence. The layout is a response to that material, not a
fixed three-column process. Use the earlier vector galleries only for explaining
mechanisms when an actual result image is unavailable.

## Composition studies implemented here

| Layout | Structure | Evidence to prepare |
|---|---|---|
| `editing-atlas` | Dominant edited result; smaller input and instruction; two compact paired examples | Correct input/output pairs and their real edit instructions |
| `visual-case` | Large visual case; explicitly marked detail crop; short response; compact aggregate result summary | Input, verified response summary, crop coordinates and published/project measurements |
| `robot-ribbon` | Large task/environment view; two action details; continuous ordered frame ribbon | One correctly ordered trajectory and task description |

Give images most of the area. Use asymmetry for hierarchy, not arbitrary
misalignment. Keep short labels attached to their images; put explanation in a
caption rather than in tall generic model blocks. Do not recolor actual images
to force them into the palette. Palette roles apply to annotations and plots.

## What was inspected and what the local examples contain

- Brooks, Holynski and Efros, [InstructPix2Pix](https://arxiv.org/abs/2211.09800v2),
  CVPR 2023, Fig. 1 (PDF p. 1). The input/output samples were visually inspected;
  the local editing atlas rearranges the original pairs, with one pair enlarged.
  It does not generate a new edited image or claim those results for this project.
- Liu et al., [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485v2),
  NeurIPS 2023, Tables 3 and 5 (PDF pp. 6–7). The input image and response were
  checked, and the aggregate relative scores transcribed from Table 5. The
  response shown in the new composition is labelled as a paraphrased summary.
  The chart describes the aggregate benchmark, not the score of the displayed
  photo. Its values are relative scores, not classification accuracy; uncertainty
  is the source's reported standard deviation.
- Black et al. / Physical Intelligence, [π₀ official paper](https://www.physicalintelligence.company/download/pi0.pdf),
  Fig. 2 (PDF p. 2). The six-frame sequence was visually inspected. Frame order
  is retained, and the source image is split only at its existing white separators.
  The enlarged details come from that same sequence. Stage labels are editorial
  descriptions, not invented timestamps or a new robot execution.

These examples were checked on 2026-10-26. Figures and tables were inspected in
full context before extracting the images. No paper title, author affiliation or
attribution is inferred from visual appearance alone.

## Prepare the local reference specimens

The skill includes code and instructions, not the paper PDFs or extracted raster
assets. Give the preparer local copies of the specified PDFs:

```bash
uv run --with pymupdf python skills/scientific-figure-making/examples/prepare_reference_teasers.py --instruct /path/to/instructpix2pix-v2.pdf --llava /path/to/llava-v2.pdf --robot /path/to/pi0-official.pdf --out /tmp/paper-reference-assets
uv run --with resvg-py python skills/scientific-figure-making/examples/result_teasers.py /tmp/paper-reference-assets/editing.json --out /tmp/result-teasers --png
uv run --with resvg-py python skills/scientific-figure-making/examples/result_teasers.py /tmp/paper-reference-assets/multimodal.json --out /tmp/result-teasers --png
uv run --with resvg-py python skills/scientific-figure-making/examples/result_teasers.py /tmp/paper-reference-assets/robotics.json --out /tmp/result-teasers --png
```

The preparer expects InstructPix2Pix arXiv v2, Visual Instruction Tuning arXiv v2,
and the inspected official π₀ download with a 3950 × 540-pixel six-frame Fig. 2.
It checks extracted dimensions and stops if they differ. These are deliberately
version-specific reference examples, not a general paper scraper. If a revised
PDF changes the image order or dimensions, inspect that revision before adapting
the extraction indices. Do not silently treat another image as the requested one.

The two arXiv papers are marked CC BY 4.0; pictured third-party material can have
separate terms. The π₀ arXiv distribution license is not a general open asset
license. Retain asset-specific rights and attribution. These generated specimens
are local design references; use owned or appropriately licensed project images
for publicly distributed templates or a paper. Code licensing does not license
borrowed raster artwork. Rights notes are saved with each specimen's provenance.

## Use actual project evidence

`result_teasers.py` accepts a JSON manifest and performs no network requests.
Start from a prepared manifest, replace source labels, text, image files and
measurements, and set `kind` to `PROJECT RESULTS` only for real project results.
A source label and source URL are required. `PUBLISHED REFERENCE STUDY` remains
visible for examples borrowed from existing papers.

Every asset has `file` and `size: [pixel_width, pixel_height]`. Paths are absolute
or relative to the manifest. Optional `crop: [x, y, width, height]` is in source
pixels and must lie inside the original image. A detail crop and each robot frame
use the same coordinate convention. Images are embedded as data URIs without
re-encoding or recoloring; SVG clip paths prevent adjacent strip frames bleeding
into letterbox margins. The original pixels remain in the SVG.

For `visual-case`, each result has `name`, `value` and `std`. The built-in chart
uses a 0–100 scale for relative scores; do not reuse it unchanged for different
metrics. For `editing-atlas`, preserve each before/after identity and instruction.
For `robot-ribbon`, preserve temporal order and label any omitted frames. Caption
fields remain editable rather than being inferred automatically from the images.

SVG generation is standard-library only. `--png` adds resvg-py rendering.
`--tokens /path/to/paper-colors.json` optionally reads the existing `ours` anchor
for annotations without modifying any photograph. SVGs retain editable labels,
source links in companion provenance JSON, image dimensions and crop coordinates.
Raster source images remain raster. The renderer is not a substitute for inspecting
output at manuscript size; the 183 mm master is a project-teaser composition study.

## Final visual and evidence check

Check full images and detail crops side by side. Keep crop boundaries explicit;
never describe editorial crops as model saliency or learned grounding. Confirm
labels, uncertainty definitions and source comparisons. Check text/image spacing,
readable thumbnails, frame order and external-resource independence. Inspect the
SVG/PNG after rendering; source extraction success alone does not establish that
the composition is clear or scientifically faithful.
