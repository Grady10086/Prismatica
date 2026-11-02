# CS manuscript comparisons: factorial design, modality conflict, sampler cost

Use these compact 180×120 mm data figures for experimental sections. All arrays are **synthetic demonstration fixtures**, not measurements or values copied from a paper. Generated panels share their underlying samples; the script exports those arrays for replacement and inspection.

```sh
uv run --with matplotlib python skills/scientific-figure-making/examples/cs_paper_comparisons.py --out /tmp/cs-paper-comparisons
```

Requires sibling `cs_paper_data_gallery.py`. Outputs three vector PDFs, editable-text SVGs, 300-dpi PNGs, `comparison-inputs.npz` and `comparison-summary.json`.

## Full factorial ablation

Eight configurations for three binary factors, with eight shared synthetic seed indices. Tall left panel shows all configuration scores; right panels show A×B interaction (averaged over C) and marginal effects / difference-in-differences. Contrasts are first computed within seed, then summarized using the helper’s 2,000-resample percentile bootstrap. Do not average unrelated seeds and subsequently claim paired uncertainty. All intervals are pointwise 95%, with no multiple-comparison correction. Main effects average over the other factors; interaction contrasts are not standalone module-removal gains. A=fusion, B=routing, C=auxiliary are example names only. The baseline guide in the left panel is the all-disabled configuration mean, not a significance threshold. For actual results, test all required combinations or explicitly leave missing configurations unestimated.

## Modality conflict

Two synthetic model outcome arrays for the same 240 query IDs across image-only, text-only, congruent and conflicting conditions. Panels show condition accuracy, a conflict-condition 2×2 paired-outcome table, per-model congruent-minus-conflict drop, and B−A accuracy differences. Accuracy differences and drops use paired query resampling; single-condition intervals are query-bootstrap intervals of mean correctness. Counts are authoritative in the 2×2 table; color is a redundant count cue. This fixture uses shared uniforms with higher Model B success probabilities, so its wins are nested by construction and the loss cell can be zero; it is not evidence of universal dominance. Do not infer causal modality reliance from this synthetic pattern. Actual condition comparisons require well-defined correct labels, comparable queries and a documented conflict-construction protocol. Separate question/scene clusters require cluster-level rather than independent query resampling.

## Sampler quality and cost

Three synthetic samplers, three NFE budgets and 100 shared reconstruction-instance IDs. Both latency and reconstruction MSE are generated arrays, not actual measurements from hardware or pixels. The same arrays support quality–latency medians, latency violins at NFE 32, paired MSE-reduction ECDFs and fraction above a predefined MSE threshold of 0.10. The threshold is a fixture example, not a recommended scientific cutoff. In real experiments justify it before analyzing comparisons. Only the threshold panel shows 95% pointwise instance-bootstrap intervals; medians and violin distributions are descriptive. NFE labels identify measured budgets; connecting segments do not imply additional intermediate runs. No Pareto optimality is claimed beyond displayed measurements. Paired MSE requires actual corresponding reference targets and a declared image scaling/masking policy. Unconditional T2I quality needs different evaluation metrics. Real latency requires hardware, batch size, precision, synchronization and warmup details; do not equate NFE with latency.

Use this route rather than editorial layouts when the user requests suitable paper data plots. Replace fixture inputs and retain metric direction, grouping, uncertainty and matching identities consistently across panels. Keep all losing cases; do not erase the synthetic footer until real data replaces every fixture.
