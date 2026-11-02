# Spatial, temporal and set-overlap composites

Three additional original compositions avoid the heatmap–bar-chart default.
Primary PDFs were retrieved and the following pages visually inspected:

1. [A computational pipeline for spatial mechano-transcriptomics](https://www.nature.com/articles/s41592-025-02618-1), Nature Methods 22, 737–750 (2025), Fig. 2, PDF p. 4 (printed p. 740). The figure aligns cell segmentation, tension, pressure, cell identity and UMAP across three specimens. Borrow matched spatial/feature-space identities and the separation of categorical cell colors from continuous physical measurements. Our spatial view has original synthetic points and a computed PCA, not tissue images, inferred mechanical pressure or a UMAP.
2. [Spinal interneuron population dynamics underlying flexible pattern generation](https://www.nature.com/articles/s41467-025-64629-y), Nature Communications 16, 9634 (2025), Fig. 4, PDF p. 7. The figure combines cycle-aligned muscle traces, state trajectories, scatter associations and PC projections for two animals. Borrow the event-aligned time/state-space pairing. Our layout adds a synthetic event raster and rate strip, not the paper's experimental recordings or correlations.
3. [Plasma proteomics for biomarker discovery in childhood tuberculosis](https://www.nature.com/articles/s41467-025-61515-5), Nature Communications 16, 6657 (2025), Fig. 2, PDF p. 4. The figure places site composition, intensity ECDF, protein-identification UpSet, sample PCA and protein-level coefficient-of-variation distributions in one QC composition. Borrow the combination of coverage, distribution and sample geometry. Our overlap figure uses exclusive-intersection lollipops and separate synthetic measurements, not the paper's protein counts, batch correction or clinical outcomes.

## Reproduction

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_diverse_gallery.py --demo --out /tmp/nature-diverse
```

Optional --colors accepts a paper-colors Python export; default is the same test
fixture as the earlier galleries. Exports are three editable SVG/PNG compositions
and data-and-summaries.json. This demo-only CLI requires explicit --demo. Import
and adapt the functions for project measurements; replace demo labels and captions
and document units, case identities and exclusions. No paper images are bundled.

## Layout and interpretation contracts

**Spatial context**, seed 519: 1600 candidate points are generated uniformly in a
square; a specified elliptical/notched mask retains 869 synthetic observations.
Coordinates are assigned synthetic micrometre units; scale-bar length is exactly
200 coordinate units. Three predefined domains are determined from x + .4y.
The rectangular region is a subset of the same points, colored by their actual
synthetic signal values. All PCA points preserve these identities. PCA uses four
mean-centered features (not variance scaling), including the spatial coordinates;
it is a visualization, not evidence of independent biological clusters. Explained
variance labels come from SVD. Three ECDFs share x/y limits; each domain's n is
shown. Points within one field are not independent biological replicates. No
confidence intervals or statistical tests are implied.

**Temporal evidence**, seed 520: the left column uses a shared −1 to 3 s axis and
an onset line at 0. Forty synthetic units supply event times; .1 s histogram bins
are normalized by 40 units and bin width to obtain Hz. The 30 response traces are
separate simulations with mean ± sample SD (`ddof=1`), not CI/SEM. Event and response
panels share a generative envelope, not matched experimental unit IDs. Each peak
ECDF observation is the maximum of one of the 30 traces. The six right-hand state
paths are explicitly separate parametric illustrations, not PCA, a fitted latent
state or a transformation of the raster/response data. Do not present them as
measured state trajectories. For real work, substitute matched recorded trajectories
and indicate how the state projection is computed. ECDFs are step functions.

**Feature coverage**, seed 521: 420 synthetic feature identities have four binary
assay memberships. The universe is the union; no feature is absent from all sets.
The 15 displayed combinations are exclusive: an active assay is present and an
inactive assay absent. Their counts sum to 420; set sizes sum overlapping memberships
and therefore need not sum to 420. Detection sets are separate synthetic features
from the eight-channel intensity data. Ninety independent synthetic samples (30
per site) generate the ECDF of each sample's mean log2 intensity, PCA of centered
log2 intensities, and per-channel medians with 10–90% data ranges across samples.
These ranges are not confidence intervals; adjacent channels are connected as a
reading guide, not interpolation. Sample rows are matched across these three
panels. No batch correction is applied or claimed. The site palette is consistent.

All examples are explicitly synthetic and descriptive. JSON preserves raw
coordinates, domain IDs, PCA inputs, explained variances, raw response traces,
event times, rate bin edges and counts, state paths, feature membership,
intersection combinations/counts, sample sites and raw intensities. No fabricated
significance annotations. Panel letters continue the preceding composite series.
