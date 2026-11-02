# Circular tracks, dose response and survival composites

These are original data-layout studies informed by visually inspected Nature
Portfolio figures. No paper images or reported measurements are redistributed.

## Inspected primary references

- [Ultra-high-scale cytometry-based cellular interaction mapping](https://www.nature.com/articles/s41592-025-02744-w), Nature Methods 22, 1887–1899 (2025), Fig. 2, PDF p. 5 (printed p. 1891). Panel d uses a Circos display of relative enrichment among interacting cell types; the page combines it with cell maps and quantitative summaries. Borrow circular category sectors and whole-to-detail reading. Our multi-track design is an original extension; its links are descriptive correlations, not physical cell interactions or relative enrichment.
- [Decrypting the molecular basis of cellular drug phenotypes by dose-resolved expression proteomics](https://www.nature.com/articles/s41587-024-02218-y), Nature Biotechnology 43, 406–415 (2025), Fig. 3a–b, PDF p. 5 (printed p. 410). The original juxtaposes concentration-response observations and fits with binding-affinity summaries and mechanistic detail. Fig. 2d–e (PDF p. 4) also uses radial potency representations. Borrow the observation/fit/parameter hierarchy; our three synthetic increasing response curves are not the paper's drug or protein measurements.
- [Real world effectiveness of chemotherapy plus bevacizumab with immunotherapy in colorectal cancer](https://www.nature.com/articles/s41598-025-13701-0), Scientific Reports 15, 29170 (2025), Fig. 1, PDF p. 4. Two Kaplan–Meier panels are paired with at-risk tables; Fig. 2 adds case-level duration displays on the same page. Borrow explicit censoring, risk-table alignment and the complementary individual-case view. Our groups are entirely synthetic, with no clinical treatment comparisons or study conclusions.

## Reproduce

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_advanced_gallery.py --demo --out /tmp/nature-advanced
```

Optional --colors accepts a paper-colors Python export. By default the earlier
galleries' test palette is exported locally. Exports: three editable SVG/PNG
compositions plus data-and-summaries.json with all input observations and derived
parameters. CLI requires explicit --demo. For measured data, adapt the functions,
replace synthetic labels and specify provenance, observational units and assumptions.

## Circular multitrack atlas

Seed 621; 60 features, five predefined modules of 12 features and 48 observations
per feature. Outer sectors encode module identity. The next track encodes the
z-score of each feature's observed mean across the 60 means (population SD).
Color scale is fixed −3 to +3; clipping affects color only and should be checked
on project measurements. The next radial track has a common baseline .82 and
height .17 times synthetic detection fraction (0–1). Inner ticks have baseline .65
and length .10 times synthetic count/100, with count ranging 10–100. Angular widths
are equal feature slots, not abundance. Modules and slot order are predefined.

The 18 strongest cross-module Pearson associations satisfying |r| > .30 are drawn
as equal-width quadratic curves; their width, curvature and distance do not encode
magnitude, flow or causality. Sign is not encoded. These are display-selected
associations, not significant findings. Full raw observations and link coefficients
are saved. Detection and counts are separately generated demo attributes, not
estimates derived from those observations. The companion scatter preserves every
feature; point AREA = .22 times count (legend included). Module summaries show
median and IQR of detection, not confidence intervals.

## Dose response

Seed 622; three conditions, ten concentrations from .001–100 μM, five independent
synthetic observations per concentration. Model:

`response = bottom + (top-bottom)/(1 + 10**((logEC50-log10dose)*slope))`

Fit all 50 raw observations per condition by unweighted bounded nonlinear least
squares. Demo bounds: bottom −30–40, top 50–130, logEC50 within measured log-dose
range, increasing slope .1–5. Bounds express this demo's model, not universal
biology. EC50 is the midpoint between fitted asymptotes, not necessarily absolute
50% response. Fit residuals are measured minus fitted response in percentage points.
Zero concentration is not placed on a log axis. No fitting beyond the measured
concentration range is shown.

Two hundred within-dose resamples of the five independent observations yield
pointwise percentile 95% bands and EC50 percentile intervals; each fit must succeed
and at least 180 successful fits are required. The successful parameter arrays are
saved. Bands are neither prediction intervals nor simultaneous confidence bands.
For paired plates, biological/technical nesting or correlated dose observations,
resample the appropriate independent unit instead. For real data, assess model
identifiability, bound hits, residual structure, heteroscedasticity and bootstrap
stability; select increasing/decreasing/biphasic models according to the assay.
No p-values, clinical dosing recommendations or invented drug properties.

## Right-censored time to event

Seed 623; three independent synthetic groups of 80 cases. Failure times follow
Weibull distributions; independently generated censor times are capped at 36
synthetic months. Save observed min(failure,censor) and event=1 for observed failure,
0 for censoring. The Kaplan–Meier product-limit estimator includes cases with
observed time >= t in the risk set immediately before t. For tied event/censor
times, events use that full risk set; both are then removed. Censor '+' markers use
the right-continuous survival value at the censor time.

Pointwise 95% intervals use Greenwood variance with a log–log transform. S=1 and
S=0 endpoints are handled explicitly. Bands describe estimator uncertainty, not a
prediction interval or simultaneous band. At-risk table and individual observed
duration dots come from exactly the same records. The right lower panel gives
survival at a prespecified 18 months and the same pointwise interval, not hazard
ratios. No log-rank tests, Cox fits or significant-group annotations are invented.
No left truncation, competing risks, weights or interval censoring are supported
by this small primitive; those designs need the appropriate estimator. Independent,
non-informative right censoring is assumed. Do not interpret these synthetic groups
as treatments or use this template to claim clinical efficacy.

Implementation references:
- [SciPy curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html): bounded nonlinear least squares.
- [lifelines KaplanMeierFitter](https://lifelines.readthedocs.io/en/latest/fitters/univariate/KaplanMeierFitter.html): right censoring and Greenwood log–log intervals.

Verification: seven primitive tests cover tied event/censor times, all-censored and complete-event samples, invalid inputs and noiseless 4PL recovery. KM estimates and Greenwood log–log intervals were also compared against lifelines on 100 seeded records with tied times and censoring, agreeing to 1e-10.
