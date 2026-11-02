# CS manuscript data figures

Use this route when the user wants data plots suitable for the experimental section of a paper. It takes priority over editorial/teaser routes for such requests. Use compact labeled subplots, readable axes, shared method colors and interpretable statistics; omit hero headlines and unrelated source-image collages.

```sh
uv run --with matplotlib python skills/scientific-figure-making/examples/cs_paper_data_gallery.py --out /tmp/cs-paper-data
```

Produces three 180×120 mm figures in PDF, SVG and 300-dpi PNG, plus raw `demo-inputs.npz` and `summary.json`. Every value is synthetic and explicitly marked as such. This script is a reproducible fixture generator, not an importer of actual training logs or published benchmarks. Replace its generation blocks with real inputs, then recompute all panels. Do not remove the synthetic label before replacing the data.

## Training dynamics

Eight indexed demo runs per method, 101 evaluation epochs. (a) Train/validation cross-entropy: median over runs; validation band Q1–Q3, dashed training median. (b) Gradient L2 norm with the same run-level summaries. (c) Fixed-checkpoint boxplots with all eight points visible: median, Q1/Q3, 1.5-IQR whiskers; jitter deterministic and horizontal only. (d) Seed-index-matched final outcomes. Real comparisons require an actual shared seed/protocol pairing; independently run methods should not be connected merely for appearance. IQR describes run variation, not uncertainty of the mean. Loss and gradient arrays are synthetic independent fixtures, not derived from a trained network.

## Cross-modal alignment diagnostics

120 synthetic paired 64-D image/text embeddings, normalized to unit length. All retrieval ranks and cosine distributions are computed from these same embeddings. (a) Image→text Recall@k among the fixed set of 120 candidates. (b) Matched cosine similarities versus a cyclic shift of the text IDs (known mismatched fixture pairs). (c) Pair-level matched cosine change B−A. (d) Recall@1/5/10 changes and 95% percentile paired bootstrap intervals using 2,000 resamples of query IDs. Candidate set and ranks are held fixed during bootstrap: intervals quantify query-level variability conditional on this gallery, not gallery sampling or training-seed uncertainty. The artificial pairs each have one unique match; real many-positive retrieval needs appropriate relevance labels. Similarity is a diagnostic and does not establish causal multimodal fusion. Synthetic fixture negatives are not a general hard-negative mining method.

## Diffusion reconstruction evaluation

80 indexed synthetic reconstruction instances at NFE 4/8/16/32. (a) Median MSE and interquartile error bars across instances, not a confidence interval. (b) Paired instance-level reduction at NFE 32, including negative improvements. (c) Complete empirical CDFs at that same NFE. (d) Mean paired reduction by predefined synthetic input-difficulty quartile with 95% percentile bootstrap CIs (2,000 within-quartile instance resamples). These MSE values are generated fixtures, not computed from generated pixels. Replace with actual reference reconstruction errors. MSE requires a valid paired target and is not a general text-to-image quality metric; unconditional generation should use appropriate distributional metrics and repeated evaluations instead. NFE is not automatically equivalent to wall-clock latency or scheduler steps, especially with guidance or multistage methods.

Retain the actual pairing/grouping unit for resampling. Specify sample size, statistic, uncertainty, metric direction and hardware when applicable. Preserve outliers and losing cases. Do not digitize values by eye from reference-paper screenshots or mix different studies into a fictitious common experiment.
