# ROC/PR, calibration and decision-curve compositions

These three original layouts extend fixed-prediction model evaluation. Published
figure pages were visually inspected; no reported outcomes or paper images are
redistributed. Clinical reference papers inform layout, not claims of clinical
validity for the synthetic examples.

## Inspected Nature Portfolio references

1. [A Causal and interpretable machine learning framework for postcranioplasty risk prediction and surgical decision support](https://www.nature.com/articles/s41746-026-02370-6), npj Digital Medicine 9, 184 (2026), Figs. 3–4, PDF pp. 6–7. ROC/PR, calibration and decision curves appear with subgroup evidence across validation settings. Borrow a common cohort definition and consistent model identities across discrimination, calibration and utility views. Do not copy a diagonal chance reference into PR space: our PR baseline is the observed positive fraction. Our data are not geographical/temporal external validation or causal estimates.
2. [Characterization of pathogenic microorganisms in diabetic foot infections and development of a risk prediction model](https://www.nature.com/articles/s41598-025-07092-5), Scientific Reports 15, 23553 (2025), Fig. 3, PDF p. 6. ROC intervals, calibration with prediction-support rug, and a decision curve are combined. Borrow support context and explicit action baselines. Our calibration is fixed-bin descriptive reliability, not a fitted logistic/nonparametric calibration or bootstrap bias-corrected nomogram, and our net benefit is unstandardized per-case utility.
3. [Deep ensemble learning with transformer models for enhanced Alzheimer’s disease detection](https://www.nature.com/articles/s41598-025-08362-y), Scientific Reports 15, 24720 (2025), Figs. 13–14, PDF p. 16. PR and binned calibration views motivate examining ranking and observed probability separately. Borrow that complementary evidence. Do not import its reported PR area as an AP definition, or infer calibration from sparse bins without support counts.

## Run

```bash
uv run --with matplotlib --with scipy --with scikit-learn python skills/scientific-figure-making/examples/nature_prediction_gallery.py --demo --out /tmp/nature-prediction
```

Optional --colors accepts a paper-colors Python export; default is the earlier
galleries' test palette. Outputs: three SVG/PNG compositions and
`data-and-summaries.json`. CLI requires explicit --demo. Scoped contracts live in
`scripts/prediction_stats.py`; the gallery uses scikit-learn for ROC and AP.

## Synthetic cohorts and shared identities

Cohort 1: seed 921, n=800. Cohort 2: seed 922, n=500, with a −.45 shift in latent
risk. For each case, z follows Normal(−1.55+shift,1.35), outcome follows
Bernoulli(expit(z)). Fixed simulated prediction channels are:

- A: expit(z+Normal(0,.35))
- B: expit(1.5*(z+Normal(0,.7)))
- C: expit(z+Normal(0,1.1)+.5)

There is no trained model, calibration fit or threshold tuning. These prediction
rules are fixed before labels are evaluated. Calling this cohort held-out test
evidence, temporal validation or an independent external replication would be
misleading. JSON record row indices identify matched cases across all panels;
model column order is A/B/C. Each cohort has independent observations; both outcome
classes must be present for ROC/PR. Cohort positive fractions are computed and
shown, never assigned from a desired chart shape. Model colors remain consistent.

For project data, use proper out-of-sample predictions; fit all preprocessing,
feature selection, calibration and threshold policies using separate training/
validation data. Preserve biological or participant clusters in uncertainty
calculations. State outcome horizon, positive class and case ascertainment.

## Discrimination and ranking composition

Exact empirical ROC uses all score thresholds (`drop_intermediate=False`). AUROC
is the standard rank/trapezoidal ROC area; ROC chance reference is the diagonal.
PR uses the empirical step curve; the horizontal baseline is the positive fraction
in the same cohort. Report non-interpolated **average precision (AP)** from
`average_precision_score`, not trapezoidal PR area or a vaguely named AUPRC.
AP and PR baselines depend on prevalence and are not directly comparable across
arbitrarily rebalanced populations.

Four hundred ordinary row bootstrap draws (seed 925) use the same sampled case
indices for all three models. One-class draws are skipped and fewer than 95%
successful draws cause failure. Scalar AUROC/AP intervals are 2.5th/97.5th
percentiles; this is conditional fixed-prediction uncertainty, without model
refitting. It does not include training variability, provide simultaneous bands
or constitute a significance test of model differences. Bootstrap metrics are
saved. The bottom-left ECDF uses all Model A predictions, split by true outcome,
with counts and positive/negative line styles. No curves are smoothed.

## Calibration diagnostics composition

Use ten fixed equal-width bins on [0,1], shared across models. Bins are left-closed,
right-open except the final bin includes 1. Empty bins are omitted and observations
are never silently dropped. For each occupied bin, plot mean predicted probability
and observed fraction positive. Dot AREA = .18 × bin n (legend included). Vertical
95% Wilson score intervals describe the binomial event fraction given that bin's
membership; they are not bootstrap confidence bands for the entire calibration
function and do not include uncertainty in the bin's mean prediction. Connecting
lines are reading guides, including across empty bins. Separate plots show all
prediction histograms (20 fixed bins), support by reliability bin and signed
observed-minus-predicted bin error.

ECE is sum_b (n_b/N)*abs(observed_b−predicted_b) with this exact binning. It is a
bin-dependent descriptive statistic and cannot be compared without the binning
rule and sample definition. Brier score is mean((p−y)^2), assessing both calibration
and discrimination plus outcome uncertainty; lower Brier does not alone prove
better calibration. Point summaries have no invented error bars. Wilson endpoints
at observed fractions 0/1 are handled explicitly to avoid roundoff causing invalid
negative error lengths. Saved JSON includes every bin index, n, prediction mean,
observed fraction, Wilson interval, ECE and Brier score.

## Decision utility composition

Thresholds are fixed at 101 values from .05 to .30, an illustrative range without
clinical justification. The action rule is p >= threshold (ties included). Net
benefit is **unstandardized**, per case:

`NB(pt) = TP/N − FP/N * pt/(1−pt)`

Act-on-all uses the cohort's own prevalence: prevalence − (1−prevalence)*pt/(1−pt).
Act-on-none is exactly zero. Negative values are retained and the two cohorts use
the same y limits. The lower-left panel shows Model A minus act-on-all on Cohort 1;
400 paired row resamples (seed 926) recompute both terms using the same resampled
labels and probabilities at every threshold, giving pointwise percentile 95%
intervals. These are not simultaneous confidence bands and do not select a
significant/optimal threshold range. The action-fraction panel counts predicted
positives directly from the same Cohort 1 cases.

Utility depends on the harm/benefit assumptions represented by threshold odds,
outcome horizon and calibration. A positive estimated curve alone is not evidence
of clinical effectiveness or treatment benefit. The two synthetic cohorts differ
in latent risk; their difference is not a causal prevalence experiment. No
case-control sampling correction, competing-risk or censored time-to-event DCA is
implemented. For those study designs, use the corresponding estimator and target
population prevalence. JSON saves all labels, model probabilities, threshold grids,
cohort-specific net benefits, act-all curves and difference-interval bounds.

## Verification and primary implementation sources

Six tests check bin endpoints/empty bins, exact ECE/Brier values, Wilson endpoint
coverage, manually enumerable net benefit, equivalence to all/none baselines,
threshold ties and rejection of invalid probabilities/bins. The gallery is rendered
and visually checked for overlapping labels and bin support.

- [scikit-learn calibration guide](https://scikit-learn.org/stable/modules/calibration.html): reliability diagrams and Brier interpretation.
- [scikit-learn average_precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html): non-interpolated AP definition.
- [Vickers and Elkin, Decision curve analysis: a novel method for evaluating prediction models](https://pmc.ncbi.nlm.nih.gov/articles/PMC2577036/), Medical Decision Making (2006): threshold-based net benefit framework.
