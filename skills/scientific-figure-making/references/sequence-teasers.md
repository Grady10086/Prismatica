# Image-dense video, 3D and robot teasers

Use these compositions when actual frames, multiview renders or manipulation
results are available. Start with visual evidence; keep the canvas to a short
heading, task/method labels, sequence ordinals and a source line. Move experimental
protocol details into the paper caption or provenance file, not explanatory cards.

## Six compositions

| Preset | Visual structure | Required evidence |
| --- | --- | --- |
| `video-cinema` | Dominant selected output, smaller conditioning image/detail, ordered strip | Four ordered output samples, the actual conditioning image and a declared detail crop |
| `video-proofsheet` | Three full-width method strips, four frames per method | Same condition across methods; retain source sample order and method names |
| `object-stage` | Large textured mesh, input/geometry at left, normals/color views at right, additional objects below | A matched input, reconstructed geometry, two normals and two color views, four additional reconstructed objects |
| `geometry-comparison` | Five method/input columns, individual rows or an intact source sheet | Matched object/view across columns; comparable renderer, scale and crop for project experiments |
| `robot-diptych` | Two large task outcomes above smaller preceding samples | Two tasks with five ordered shown frames each; enlarged last sample is not an independent evaluation |
| `task-mosaic` | Four task pairs in a two-by-two image collection | First and last shown views of four tasks; no implied success score |

These are composition studies, not author-style presets. Choose by the evidence.
A method comparison naturally uses a grid; a task collection or hero result need
not. Do not assign a performance claim merely because a result is larger or first.
The enlarged endpoint is labelled **last shown**, rather than “success.”

## Inspected primary references

- [DynamiCrafter, ECCV 2024 proceedings](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06298.pdf),
  p. 10, Fig. 4: conditioning image and four ordered video samples for each method.
  The local studies use the beer-pouring condition, with the original PikaLabs,
  SVD and DynamiCrafter outputs. The source figure also includes Gen-2, which this
  three-method selection omits. The conditioning image is a separate embedded
  inset, not a generated frame relabelled as input. Reference crops retain the
  existing watermark pixels.
- [Wonder3D, CVPR 2024 proceedings](https://openaccess.thecvf.com/content/CVPR2024/papers/Long_Wonder3D_Single_Image_to_3D_using_Cross-Domain_Diffusion_CVPR_2024_paper.pdf),
  p. 1, Fig. 1: input, generated normals/color views, geometry and textured mesh;
  p. 6, Fig. 5: reconstructed geometry and textured outputs across methods. The comparison
  retains all five objects and all four method columns as one intact sheet; some
  source rows overlap, so isolating objects would clip surfaces or introduce
  fragments of neighboring objects.
  These source renderings have different lighting; this is a published qualitative
  comparison, not a new controlled rendering experiment.
- [Physical Intelligence, pi0 paper](https://www.physicalintelligence.company/download/pi0.pdf),
  p. 7, Fig. 6 and p. 9, Fig. 10 in the inspected original edition: five shown
  frames per manipulation. The local studies use shirt folding, grocery bagging,
  stacking bowls, loading a microwave, packing a drawer and paper-towel replacement.
  Published montages do not establish frame rates or equal time intervals.

The examples rearrange existing published results; no inference was run. Keep
asset-specific rights and credits. PDF distribution access does not establish
unrestricted reuse of every depicted image. The repository contains source code
and documentation only, not downloaded PDFs or extracted publication rasters.
Use your own or appropriately licensed project images for an actual contribution.

## Reproduce locally

From the repository root, with the three cited PDF editions saved locally:

```bash
uv run --with pymupdf python skills/scientific-figure-making/examples/prepare_sequence_references.py \
  --dynamicrafter /path/to/06298.pdf \
  --wonder3d /path/to/Wonder3D_CVPR_2024_paper.pdf \
  --pi0 /path/to/pi0.pdf --out /tmp/sequence-assets

uv run --with resvg-py python skills/scientific-figure-making/examples/sequence_teasers.py \
  /tmp/sequence-assets/video-cinema.json --out /tmp/sequence-previews --png
```

Repeat the second command with another preset's manifest. SVG output uses the
standard library; PNG previews need `resvg-py`. Keep `sequence_teasers.py` beside
`result_teasers.py`. Optional `--tokens /path/to/paper-colors.json` applies the
`hues.ours.anchor` color to annotations only.

The preparation helper is edition-specific. It checks the page/image dimension
signature and records PDF SHA-256, page, image index, placement bounds and
extraction mode. It stops when a signature differs; inspect the new edition before
changing extraction indices. It never downloads papers. Original embedded bytes
are extracted directly except where a PDF stores a separate soft alpha mask;
those color/mask pairs are reconstructed losslessly as PNG so the object retains
its original transparency. No invented background, geometry or texture is added.

## Replace with project assets

For `geometry-comparison`, either provide three `objects` rows of five visual
references, or an intact `overview` reference with five `column_centers` in [0, 1].
The latter preserves precomposed comparisons whose objects overlap cell boundaries.

Each JSON manifest contains `layout`, `title`, `category`, `kind`, `source_label`,
`source_url` and `assets`, plus the layout-specific fields in the generated examples.
Declare `kind` as `PROJECT RESULTS` for your own verified results, or
`PUBLISHED REFERENCE STUDY` for a paper reference. `source_url` can point to the
project experiment record. Place images beside the manifest or use absolute paths.
Each asset has `file` and its actual pixel `size: [width, height]`.

A visual reference is `{"asset": "key"}` or
`{"asset": "key", "crop": [x, y, width, height]}`. Coordinates refer to source
pixels. All crops must be finite and inside the source raster. The scripts preserve
aspect ratio, clip each crop explicitly and share repeated image definitions to
keep large contact sheets compact. They embed the supplied raster bytes
unchanged. SVG text remains editable. Preparation crops for robot panels omit
existing player controls; all source image files and crop coordinates are retained.

Keep chronological sampling in the manifest. Do not fill a sequence with repeated
copies of one still, interpolate missing evidence, invent timestamps, reverse
frames, label a rendered viewpoint as a time step, or call a detail crop a new
sample. Numerals 01–04 indicate shown-sample order, not original frame numbers.
For real comparisons, keep matched prompts/conditions and sampling protocol;
select views consistently and describe the selection in the caption.

The output includes SVG, optional PNG, and a provenance JSON containing the full
manifest, all crops, asset SHA-256 hashes and annotation color. Source extraction
operations are separate from SVG placement operations. At 183 mm output width,
review readability and crop boundaries in the rendered PNG; also inspect the SVG
at the intended insertion size. A successful render does not validate a scientific
comparison.
