# Image-led editorial studies

Use these when the user prioritizes beauty, a strong hero image and visual rhythm
for a teaser, talk, project page or large-format overview. They are a distinct
editorial option alongside the Nature main-figure profile: large serif titles,
warm-white or midnight canvases and a 269×196 mm composition are deliberate.
Do not claim these are Nature submission-compliant main figures. For manuscript
panels, adapt the hierarchy and typography to the actual final insertion size.

## Three compositions

1. **Ivory microscopy**: one large unaltered 512×512 image, two linked 128×128 crops,
   a shared-unit luminance ECDF and restrained numerical annotations. Warm white,
   a large serif heading, purple/rose accents and fine rules organize the page.
   Data source: scikit-image immunohistochemistry, acquired at CMMI. Bounds in
   [xmin,xmax,ymin,ymax] are [60,188,70,198] and [280,408,280,408]. ECDFs contain all
   16,384 pixels per crop, with skimage rgb2gray luminance. These pixels are spatially
   dependent; the plot makes no inferential cell/tissue or protein-expression claim.
   512² describes image dimensions, not cells or independent samples.
2. **Midnight deep field**: large NASA source image, four linked aperture crops,
   a compact two-by-two detail gallery, soft lavender accents and restrained type.
   A simple image heuristic thresholds rgb2gray luminance > .32, labels connected
   components (skimage default full 2D connectivity), keeps area >=12 pixels and
   selects the four largest eligible components whose centroids are >=90 pixels
   apart and >=45 pixels from image boundaries. Crops are 80×80 pixels centered on
   integer-truncated centroids. The circular main-image markers are radius 30 pixels;
   they locate the selected centroid, not the exact square-crop boundary. Printed
   “bright pixels” is the full component area, not aperture-integrated flux or
   component area restricted to the crop. Total candidate count is computed before
   edge/separation filtering. Candidates are not verified galaxies, astrophysical
   object types or a calibrated detection catalog. Do not interpret the display
   selection as a representative sample.
3. **Orbital retina**: a circular viewport of the real RGB fundus image, two
   220×220 pixel crops and three sampled-color rings. The viewport clips only the
   displayed image to the inscribed circle; underlying crop/sample data remain
   original. R/G/B ring colors are explanatory accents using paper-colors roles,
   not the RGB image's natural color or inferred tissue classes. At each of 180
   equally spaced angles, sample the nearest original pixel on a circle of radius
   .36 × image width, centered at ((w−1)/2,(h−1)/2). Positive display angles run
   counterclockwise: image y = cy − r*sin(theta), x = cx + r*cos(theta). Ring opacity
   is .12 + .88*channel/255; alpha spans .12–1, with no per-ring normalization.
   This is a color-sampling visualization, not vessel density, disease risk,
   a biological periodicity estimate or a diagnostic analysis. Crop bounds are
   [320,540,620,840] and [820,1040,350,570]. Spatial units are pixels; no physical
   scale bar or anatomical subregion labels are invented.

RGB source intensities are not recolored, generated or contrast-enhanced. Crops
are exact array slices and displayed with nearest-pixel interpolation. Source
images can have their own original acquisition/processing; “unaltered” means no
additional enhancement by this script, not raw detector measurements. Images are
embedded raster assets inside editable SVG text/paths. Page rules and ornaments
are layout, not additional data. Large titles are layout-study placeholders,
not scientific findings or reusable manuscript claims.

## Source provenance and permissions

All three sources are curated scientific sample images provided by
[scikit-image data](https://scikit-image.org/docs/stable/api/skimage.data.html).
The official documentation was checked for individual source credits:

- `immunohistochemistry`: CMMI; no known copyright restrictions. Documentation
  identifies colonic glands with FHL2/DAB and hematoxylin counterstaining. Our
  pixel analysis does not measure or validate those biological annotations.
- `hubble_deep_field`: NASA Hubble eXtreme Deep Field, public-domain usage per
  the official dataset documentation. Preserve NASA credit when adapting.
- `retina`: Mikael Häggström, Medical gallery (2014), CC0 / public-domain dedication
  per the official dataset documentation. Preserve descriptive credit.

These are **not images from a Nature paper** or the user's experiments. The visual
principles extend the already inspected whole-to-detail compositions in
`narrative-data.md` (FATE-MAP and controlled comparison galleries) and
`geometry-data.md` (multiscale protein-image atlas). No restricted paper image was
adapted or relabeled as project evidence. Record actual rights for replacement
images; the sample sources' permissions do not transfer to unrelated images.

## Run and adapt

```bash
uv run --with matplotlib --with scikit-image python skills/scientific-figure-making/examples/editorial_image_gallery.py --demo --out /tmp/editorial-images
```

Optional --colors accepts a paper-colors Python export. Default role palette is
exported from the same test fixture as prior galleries. The midnight style uses
explicit accessible light ink on dark navy; image colors remain original.
Some sample images may be downloaded on first use by scikit-image's own dataset
loader. Runtime access therefore depends on its cache/network. Source photographs
are not copied into the repository; final SVG/PNG outputs embed the used assets.

Outputs: three SVG/PNG studies and provenance-and-measurements.json recording
image shape, pixel-byte SHA256, crop bounds, derived luminance means, selection
thresholds, component coordinates/areas and exact ring sample coordinates/values.
Use crop bounds and original image identities when replacing photographs. If an
image or measurement is unavailable, leave the corresponding view absent rather
than inventing a more attractive result. Do not reuse the large numerical callouts
for unrelated metrics without an actual computed quantity and unit.

Rendering checks cover overlap/readability of every study. Output verification
recomputes nearest-pixel ring values, all crop bounds and source pixel hashes.
This expansion changes visual composition and image measurements; it introduces
no classifier experiment or clinical inference.
