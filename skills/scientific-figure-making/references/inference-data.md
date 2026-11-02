# Volcano, enrichment and forest compositions

Three original layouts extend the Nature-informed data gallery. Primary PDFs were
retrieved and the cited figure pages visually inspected. Published results and
paper images are not bundled into this skill.

## Inspected references

- [Single-cell and chromatin accessibility profiling reveals regulatory programs of pathogenic Th2 cells in allergic asthma](https://www.nature.com/articles/s41467-025-57590-3), Nature Communications 16, 2565 (2025), Fig. 5, PDF p. 7. Volcano panels, feature-level maps, GSEA/running profiles and leading-edge expression detail create a whole-to-feature hierarchy. Borrow this hierarchy; our assay is synthetic continuous log2 signal with independent observations, not cell-count data or the paper's Seurat/Wilcoxon/Bonferroni analysis.
- [Large-scale transcriptomic analyses of major depressive disorder reveal convergent dysregulation of synaptic pathways in excitatory neurons](https://www.nature.com/articles/s41467-025-59115-4), Nature Communications 16, 3981 (2025), Figs. 1–2, PDF pp. 3–4. Enrichment dot plots sit above aligned volcano views for genes, transcripts and splicing, with dot count/color legends. Borrow explicit evidence alignment and separate count/statistic encodings. Our set labels and memberships are synthetic, not real GO pathways or biological conclusions.
- [Systematic review and meta-analysis of cardiovascular event risk prediction models in maintenance hemodialysis patients](https://www.nature.com/articles/s41598-025-07586-2), Scientific Reports 15, 21807 (2025), Fig. 3, PDF p. 7. A forest plot aligns study identities, confidence intervals, weights and pooled diamonds. Borrow the aligned evidence table and study/summary distinction. The original synthesizes AUCs and uses a different estimation method; our example synthesizes synthetic log odds ratios with REML. Do not apply an odds-ratio log axis or these formulas to AUCs.

## Reproduce

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_inference_gallery.py --demo --out /tmp/nature-inference
```

Optional --colors accepts a paper-colors Python export; the default is the previous
examples' test fixture. Outputs are three editable SVG/PNG compositions and
`data-and-summaries.json`. CLI requires explicit --demo. This is not a generic
real-data ingestion workflow: use validated project statistics, select methods
appropriate to the study, and replace demo labels/captions when adapting functions.

## Differential signal figure

Seed 721; 600 synthetic features × eight independent observations in each of two
groups. Signals are continuous log2-scale measurements, with no count normalization
or pseudocount operation. Each feature uses a two-sided Welch unequal-variance
t-test. Adjust all 600 p-values together using Benjamini–Hochberg (BH); q in the
code means the BH-adjusted p-value, not a separate Storey q-value estimator. The
volcano y axis is −log10(adjusted p), not raw p. Higher/lower colors require both
q < .05 and absolute difference >= 1 on the log2 scale. Applying an effect-size
filter is a display/selection rule; do not claim it separately guarantees FDR for
the post-filtered subset.

All features remain visible in volcano and MA views with identical selections.
Difference is group-B mean minus group-A mean on log2 scale; it corresponds to the
log ratio of geometric-scale signals, not necessarily the ratio of arithmetic
means. Right panels display all raw observations for the three smallest-q features;
black lines are group means, not confidence intervals. Jitter changes x position
only, seed 9. Those feature panels are selected on these same data and are not an
independent replication. Real RNA-seq or repeated-cell data need appropriate count,
normalization, pairing and biological-replicate models; do not treat cells from one
sample as independent people.

## Enrichment structure figure

Seed 722; query is the 62 higher-selected features from the same analysis. The
background is all 600 tested feature IDs, not a whole-genome default. Twelve sets
are generated before the analysis; some deliberately include extra IDs from the
synthetically shifted feature block. Every membership is saved; labels are Set 01–12
because no biological pathway annotation is being asserted.

Upper-tail overrepresentation uses `hypergeom.sf(k-1,M,K,n)`, with M = 600, K = set
size, n = query size and k = query/set intersection. Apply BH across all 12 tested
sets before display, including nonsignificant sets. The x axis is k/K (fraction of
the set hit by the query), not k/n, an odds ratio or fold enrichment. Point AREA
is 5 times k; color is −log10(BH-adjusted p). Overlapping sets are not independent;
state correction assumptions and consider an appropriate dependence-aware method
for real analyses. Gene selection/detectability bias needs a suitable background
and may require methods beyond a simple hypergeometric model.

The top-ranked set's running profile orders all features by decreasing mean
difference. Hit increments equal absolute difference divided by total absolute
difference of set members; misses decrement by 1/(M-K). This unnormalized weighted
running score returns to zero (up to roundoff). It is descriptive: no permutation
p-value, normalized enrichment score (NES) or GSEA significance is computed. Do not
label the ORA p-value as a running-profile test result. Bottom membership links show
the top four sets and first 14 selected query IDs in numeric order, explicitly a
subset of the graph. Links indicate set membership, not regulation or causality.

## Forest and sensitivity figure

Seed 723; twelve independent synthetic study log odds ratios y_i and supplied
known standard errors s_i. These aggregate inputs are simulated directly; no
participant event counts are available. Study intervals are y_i ± 1.95996 s_i, then
exponentiated; the null odds ratio is 1. Log-axis distances represent log OR.

Random-effects weights are proportional to 1/(s_i²+tau²). Estimate tau² >= 0 by
minimizing the intercept-only restricted negative log likelihood, omitting constants:

`0.5 * [sum(log(s_i²+tau²)) + log(sum(w_i)) + sum(w_i*(y_i-mu)²)]`

`mu = sum(w_i*y_i)/sum(w_i)`; `SE(mu) = sqrt(1/sum(w_i))`.

Square AREA is proportional to normalized REML weight; printed weights and CIs
match the plotted values. Pooled diamonds show mean and normal/Wald 95% intervals.
The common-effect comparator uses inverse within-study variance weights and is
labeled separately. No Hartung–Knapp correction, prediction interval, robust
variance estimation or clinical inference is implied. In small, dependent or
heterogeneous study collections, choose an appropriate estimator and uncertainty
method; do not choose the model solely from a heterogeneity test.

The precision scatter shows log OR versus SE with a vertical pooled reference;
there are no invented funnel limits, publication-bias claims or Egger tests.
Leave-one-study-out recomputes tau², weights and pooled intervals on eleven studies
for each omission. Its dotted line is the full-data pooled estimate. Saved JSON
contains all aggregate inputs, weights, tau², CIs and refits. A visually stable
leave-one-out panel alone does not establish robustness against selection bias.

## Implementation verification

Six tests check BH against SciPy (including ties and endpoints), an exactly
enumerable hypergeometric tail, background validation, the zero-heterogeneity
common-effect limit, REML permutation invariance/positive heterogeneity and invalid
inputs. These tests validate scoped primitives, not the suitability of a method
for an arbitrary study.

Primary implementation references:
- [SciPy false_discovery_control](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.false_discovery_control.html): BH/BY procedures and dependence assumptions.
- [SciPy hypergeom](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html): distribution parameters and upper-tail calculation.
