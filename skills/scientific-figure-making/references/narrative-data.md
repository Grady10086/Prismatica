# Evidence-led layouts: failures, input branches and capability landscapes

Use these when the figure should connect individual examples with aggregate
behavior. This gallery uses real handwritten images and measured outputs of a
small trained classifier. Unlike the synthetic statistical galleries, its footer
explicitly names the real dataset, demo model and artificial input variants.

## Visually inspected Nature Portfolio references

- [FATE-MAP predicts teratogenicity and human gastrulation failure modes by integrating deep learning and mechanistic modeling](https://www.nature.com/articles/s41467-026-69596-6), Nature Communications 17, 3327 (2026), Figs. 1–2, PDF pp. 3 and 5. Embedding maps are connected to phenotype images, representative clusters and detailed profiles. Borrow the overview-to-example evidence structure. Our PCA map does not discover biological phenotypes, infer mechanisms or implement FATE-MAP.
- [Outputs of generative diffusion models are often unattributable](https://www.nature.com/articles/s41467-026-75667-5), Nature Communications 17, 6974 (2026), Figs. 1–3, PDF pp. 2–3. A factual image is situated among many counterfactual outputs; the paper also shows model-ablation routes and selected variants with differences. Borrow a fixed source with explicit variant comparisons. Our branches are controlled pixel perturbations of a classifier input, **not** causal training-data attribution, generated counterfactual universes or diffusion-model ablation. Do not call them causal counterfactual estimates.
- [Automated navigation of condensate phase behavior with active machine learning](https://www.nature.com/articles/s41467-025-64617-2), Nature Communications 16, 9598 (2025), Figs. 3–4, PDF pp. 6–7. Measured experimental points, evolving phase diagrams, representative micrographs and condition-dependent properties are juxtaposed. Borrow an explicit condition plane linked to examples and measurements. Our fixed-grid corruption evaluation is not active learning, a material phase transition or an experimentally validated phase boundary.

Paper pages were downloaded and visually inspected. No paper images are bundled.

## Reproduce

```bash
uv run --with matplotlib --with scipy --with scikit-learn python skills/scientific-figure-making/examples/nature_narrative_gallery.py --demo --out /tmp/nature-narrative
```

Optional --colors accepts a paper-colors Python export. Default palette is the
previous galleries' test fixture. Outputs: three editable SVGs with embedded raster
image chips, PNG previews and evidence.json. CLI requires --demo; dataset pixels
come from the installed scikit-learn bundle, not downloaded paper images or an
image generator. See [load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)
for dataset provenance (UCI optical-recognition handwritten digit data).

## Shared actual experiment

Use the full scikit-learn digits dataset (1,797 8×8 images, intensities 0–16).
Source IDs are original dataset row indices. A stratified train/test split with
random_state=1021 and test_size=.30 produces 1,257 training and 540 held-out images.
Train LogisticRegression(C=3,max_iter=2000,random_state=1021) on training pixels/16.
No model is retrained for any panel or input condition. Predictive softmax scores
are not calibrated probabilities or guarantees of correctness.

PCA with two components and full SVD is fitted on training pixels/16 only and
transforms held-out pixels. Test labels are not used to fit the classifier or PCA.
The held-out evaluation and examples are exploratory views of this one fixed
split, not independent studies or population-general performance guarantees.
Exact outputs can depend on library versions; JSON records scikit-learn version,
source train/test IDs, held-out pixels and labels, predictions, score vectors,
model coefficients/intercepts and plotted PCA coordinates.

## Failure atlas

Plot all 540 held-out cases in the training-fitted PCA coordinates. Gray points
are correctly classified; rose points are actual mistakes. Select the six errors
with highest maximum predicted class score, using a stable sort. The contact sheet
shows their unmodified source pixels, original ID, label → prediction and maximum
score. Connecting lines and point outlines refer to those same records. Selection
is deliberately post-evaluation; the six examples do not estimate failure-category
prevalence. The dataset's real low-resolution pixels remain visibly pixelated,
without invented detail or image smoothing.

The ECDF uses every held-out case split by correct/error status. Three numeric
error pairs are the most frequent observed label/prediction pairs, not handpicked
mechanisms. PCA proximity is not evidence that points share a failure cause, and
this layout performs no clustering or causal explanation. Do not draw named
failure regions without an independently defined annotation or validated cluster
analysis. The observed demo run has 17 errors; the code always computes that
count rather than fixing it to a desired figure shape.

## Controlled input branches

Pick the correctly classified held-out digit 8 with smallest original source ID.
All six variants are computed directly from that same original image, not from
the preceding image in a branch:

- Central mask: multiply the 4×4 pixel window rows/columns 2:6 by .6 or 0.
- Intensity: multiply all pixels by .65 or .35 with a fixed displayed 0–16 scale.
- Horizontal shift: move right by one or two pixels, zero-fill the left and drop
  pixels crossing the right boundary; never wrap pixels to the other side.

Branch edges order perturbation severity; they do not imply temporal evolution,
a sequential composition of edits or causal identification. Every image is passed
to the same fitted model. Labels show the new argmax and score assigned to the
original digit label. Scores are rounded for display; full vectors and variant
pixels are saved. Severe perturbations may alter the human-readable digit or
remove its identity. No new semantic ground truth or human validation is asserted.
Use “controlled sensitivity” rather than “causal counterfactual” for this demo.

## Capability landscape

Evaluate a 13×11 fixed grid: Gaussian noise SD 0–6 in steps of .5 raw pixel units;
central-mask strength 0–1 in steps of .1. Mask first, add noise second, clip to
0–16 and apply the same pixel/16 scaling and fixed classifier. All 540 held-out
source cases appear in every cell. Seed 1022 generates one standard-normal noise
array per source image; reusing it across all conditions makes the comparison
paired and reproducible. It is one noise realization per image, not a repeated-
noise or independent-sample uncertainty analysis.

At each cell, original-label accuracy is the fraction of predictions agreeing with
the unmodified dataset label. This is a conventional artificial-corruption score;
it does not certify that severe variants preserve human class identity. Save integer
correct counts and n=540, not only rounded percentages. The 3D surface connects
observed grid values without a fitted performance model or smoothing; gray dots
mark the evaluated cells. Surface geometry is determined by the scores, not drawn
for a preferred terrain shape.

The lower map uses observed >=90% cells and an interpolated 90% contour. That
threshold is illustrative, not a significance test, safety guarantee or validated
operational boundary. Between-cell contour positions are interpolations, not
additional experiments. Three sections show actual sampled grid values with
markers. Image chips use the same original source as the branch figure, the same
noise realization and three actual conditions: (0,0), (3,.5), (6,1). They display
individual predictions and separately label aggregate cell accuracy. One example's
appearance is not representative evidence for the whole cell.

## Adapt to research data

Preserve a table with unique case ID, split, true label, prediction, score vector,
image reference and any approved failure annotations. Fit embedding transforms on
the appropriate reference data and record which samples selected the examples.
For branches, record the source ID, exact intervention, affected region, variant
image, model version and output; distinguish measured, generated and hypothetical
results. For a capability grid, keep both condition values, per-case outcomes,
replicate/seed IDs, n and an explicit criterion. Leave untested cells missing;
never fabricate a smooth terrain, dense images or causal arrows to fill gaps.

Six unit tests check identity operations, zero-fill shifts, mask locality,
common-noise behavior, clipping, unchanged inputs and invalid perturbations.
Output checks verify disjoint splits, exact error counts, example/source matching,
143 evaluated cells, grid baseline agreement and finite normalized score vectors.
