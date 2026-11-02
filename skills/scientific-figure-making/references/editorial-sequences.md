# More image-led editorial layouts: fluorescence, materials and time

Four additional image-led studies extend `editorial-images.md`. They keep its
large serif titles, fine rules, restrained captions and dominant scientific imagery,
while varying light/dark backgrounds, spatial details and temporal composition.
These are original large-format teaser/talk/project-page layouts, not journal
submission templates. Headings are visual-study placeholders, not research claims.

## Sources and rights

All four datasets have CC0 entries in the official
[scikit-image data provenance repository](https://gitlab.com/scikit-image/data/-/raw/master/README.md),
which was read alongside the
[dataset documentation](https://scikit-image.org/docs/stable/api/skimage.data.html).
Source data are retrieved via scikit-image/pooch or supplied as local .npy files;
raw volumes are not copied into this repository.

- **kidney**: Genevieve Buckley, Monash Micro Imaging (2018). Mouse kidney tissue,
  Nikon C1 confocal acquisition; shape 16×512×512×3 (ZYXC), uint16. Channel emission
  wavelengths 450/515/605 nm; spacing 1.24 μm in XY and 1.25 μm in Z.
- **nickel_solidification**: C. Gus Becker and researchers from CSM/UCSB, APS beamline
  32-ID-B at Argonne National Laboratory (2019). Eleven 384×512 uint16 radiographs
  of nickel-alloy solidification. Source describes high-speed acquisition at
  80,000 fps, but this gallery does not assume that the 11 packaged frames are
  contiguous at the original acquisition rate; only source frame indices are used.
- **protein_transport**: Andrea Boni and Jan Ellenberg, EMBL; two-channel live-cell
  sequence, shape 15×2×180×183 (TCYX), uint8. Original study: Boni et al., *Live
  imaging and modeling of inner nuclear membrane targeting reveals its molecular
  requirements in mammalian cells*, J Cell Biol 209(5):705–720 (2015),
  DOI 10.1083/jcb.201409133. No time interval or molecular channel assignment is
  inferred from the file name.
- **lily**: Genevieve Buckley, Monash Micro Imaging (2018). Four-channel confocal
  plant-stem cross-section; shape 922×922×4 (YXC), uint16; XY spacing 1.24 μm.

These are source-credited real sample datasets, not generated illustrations or the
user's experiment. They are not images extracted from a Nature article. The
layout hierarchy continues the inspected multiscale and image-linked references
in `geometry-data.md` and `narrative-data.md`; it does not reproduce those studies.

## Four compositions and display contracts

**Noir fluorescence** uses a large maximum-intensity projection and three
channel-resolved crops of one ROI. Project over Z=0; keep each channel separate
until display composition. Each channel is linearly mapped from zero to its
99.8th percentile over the whole original volume, clipped to [0,1], multiplied by
its declared violet/cyan/amber lookup color, then added and clipped to RGB [0,1].
The same channel limits/LUTs are used for main image and crops. ROI bounds are
[190,330,160,300] in [xmin,xmax,ymin,ymax] pixels. Scale bar length is exactly
100/1.24 XY pixels. Maximum projection may merge structures from distinct depths;
spatial overlap in the composite is not evidence of molecular colocalization.
Channel colors are false colors, not literal wavelength colors or inferred labels.

**Silver solidification** juxtaposes source frame 5, two exact 128×128 crops and
six frames in original order (0,2,4,6,8,10). A single grayscale mapping uses global
0.5th and 99.5th percentiles over all 11 frames; identical limits apply to hero,
filmstrip and crops. The source's modest visible change is retained rather than
exaggerated, sharpened or replaced. The layout does not estimate front velocity,
new phases or event timing. Frame 5 is an index, not a timestamp. Crop bounds:
[70,198,90,218] and [280,408,180,308]. No physical scale bar is invented.

**Kinetic protein** presents original frames 0/7/14 in a descending editorial
sequence, with a common frame-index guide. Two channels are mapped from zero to
each channel's global 99.8th percentile over the entire sequence using fixed
blue/amber LUTs; additive RGB composition is clipped to [0,1]. No denoising,
sharpening, registration, artificial motion, interpolated frames or per-frame
brightness fitting is performed. The staggered page positions denote ordering,
not measured cell displacement. Do not infer transport kinetics from page spacing.
A two-channel overlay alone is not a quantified colocalization or localization
analysis. Channel means are exported from raw values, not stretched display RGB.

**Botanical architecture** pairs a four-channel whole field with three exact
160×160 crops. Each channel uses zero/global 99.8th-percentile limits and its stored
LUT; additive RGB is clipped. The candidate crop grid has top-left x/y positions
80,220,360,500,640; rank tiles by mean **display composite** intensity and greedily
retain three whose top-left positions differ by Euclidean distance >200 pixels.
This is a transparent bright-region display selection, not a representative
sampling design, cell segmentation or biological annotation. Crop labels refer to
regions, not plant organs or inferred cell types. Scale bar spans 200/1.24 pixels.

All channel mapping limits, source dimensions, LUTs, projection axes, crops, frame
indices, raw channel means and pixel-byte hashes are saved. Percentile clipping is
an explicitly documented display transform; it does not change stored raw arrays.
No biological effect sizes, independent sample counts or statistical claims are
invented. Sources may have their own original acquisition processing.

## Reproduce

```bash
uv run --with matplotlib --with scikit-image --with pooch python skills/scientific-figure-making/examples/editorial_sequence_gallery.py --demo --out /tmp/editorial-sequences
```

Optional `--asset-dir /absolute/path` reads kidney.npy, nickel_solidification.npy,
protein_transport.npy and lily.npy with allow_pickle=False. If a local file is
absent, the named scikit-image loader is used and may download via pooch on first
access. No implicit search of user research directories occurs. CLI requires
explicit --demo. Keep these input arrays separate from project evidence when
adapting; retain accurate source credits for any replacement images.

Outputs: four editable SVGs with embedded raster images, PNG previews and
provenance-and-display.json. All pages are 10.6×7.7 inches; redesign typography and
spacing for a small manuscript column. Default false-color LUTs are explicit
channel display choices, not method-identity palette roles. Do not silently recolor
an established assay legend when integrating these layouts into a paper.

Validation recomputes hashes, shared percentile limits, slice indices, crop bounds,
finite display composites and raw mean summaries. Every exported composition is
visually reviewed for overlapping labels, missing images and unreadable credit.
