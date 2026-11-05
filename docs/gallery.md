# Selected gallery

Twelve original compositions, including three dense CS studies. These are original gallery designs with **synthetic inputs**, not screenshots from papers or performance claims. The readable gallery masters are 10.4 × 5.8–6 or 11 × 6.4 inches; adjust font sizes and dimensions for a specific manuscript venue.

## Multimodal and diffusion studies

Three additional compositions cover [cross-modal retrieval, evidence conflict and computed diffusion numerics](multimodal-diffusion.md). Their panel definitions, Nature-family source studies and reproduction commands are documented together. The homepage features these studies; all earlier compositions below remain available.

## Dense CS compositions

These three homepage figures reuse the exact arrays exported by `cs_showcase.py`. They replace the surrounding presentation cards with aligned scientific panels. Gallery masters are 11 × 6.7 inches; tune typography for the submission width.

### Factorial response atlas

![Factorial response atlas](gallery/editorial-ablation.png)

- **a:** 8 configurations × 16 shared seeds. Half-density curves are independently peak-normalized Gaussian KDEs, with all seed points and mean/95% percentile seed-bootstrap intervals below each row.
- **b:** marginal component effects are on-minus-off differences within seed, averaging the other factors. Densities summarize the 16 paired seed effects; black intervals bootstrap those effects.
- **c:** per-seed changes relative to the no-component configuration. Columns share one ordering by mean change over configurations. Fixed symmetric color scale (−10 to 10); end caps flag saturation.
- **d–e:** A × B and A × C comparisons, each averaged over the remaining factor. Faint lines retain individual seeds; heavy lines and error bars show means and 95% seed-bootstrap intervals. Nonparallel lines alone do not establish statistical interaction.
- [Editable SVG](gallery/editorial-ablation.svg)

### Model diagnostic plate

![Model diagnostic plate](gallery/editorial-analysis.png)

- **a:** hexagon color encodes counts of 240 paired synthetic predictions; both probability axes use 0–1. **b:** KDE violins summarize ten synthetic probe seeds per layer; the line connects layer means. No confidence interval is encoded by violin width.
- **c–d:** paired probability changes against independently generated difficulty and in four predefined equal-width difficulty bins. Half-density heights are peak-normalized and descriptive; raw cases remain visible.
- **e:** all paired changes, ordered by value; negative changes remain. **f:** case values and mean/95% case-bootstrap intervals in the same four bins. Q1–Q4 are bin labels, not empirical quantiles. These intervals exclude retraining uncertainty.
- [Editable SVG](gallery/editorial-analysis.svg)

### Performance and consistency plate

![Performance and consistency plate](gallery/editorial-performance.png)

- **a:** every simulated seed operating point; heavy lines connect mean scores at median simulated latencies for four evaluated budgets. Error bars show **seed SD**, not confidence intervals. **b:** peak-normalized KDEs and raw paired differences at budget 4.
- **c:** task means retain the method colors and marker shapes. Connectors trace method profiles over task IDs, not continuous task interpolation. **d:** task-specific mean differences versus reference on a fixed symmetric −6 to 6 scale, with saturation marked by end caps.
- **e:** for each seed, compute the fraction of ten tasks beating reference, then display the ECDF across 20 seeds. No independence assumption across tasks or significance claim is implied.
- The 10 × 4 × 20 task tensor averages exactly to the fixed-budget seed scores used in the overview.
- [Editable SVG](gallery/editorial-performance.svg)

**Literature context:** the analysis themes were cross-checked against the published figure descriptions of [AdaptiveNN, Nature Machine Intelligence (2025)](https://www.nature.com/articles/s42256-025-01130-7) (multi-task cost comparisons and controlled ablations) and [high-level visual representations, Nature Machine Intelligence (2025)](https://www.nature.com/articles/s42256-025-01072-0) (layer-wise and matched representation comparisons). These are original synthetic layouts, not reproductions of those paper figures or results.

## CS model analysis

![CS model analysis](gallery/cs-model-analysis.png)

- **Paired predictions:** 240 synthetic cases, identical probability axes, baseline/updated marginal histograms. The symmetric color scale encodes updated-minus-baseline probability; colorbar end caps indicate saturation beyond ±0.25. Probability estimates are synthetic, not calibrated model outputs.
- **Layer probes:** a separate 12-layer × 10-seed fixture. Shading is a pointwise 95% Student t interval over seeds (df=9), not simultaneous coverage across layers. This does not establish a causal role for a layer.
- **Difficulty slices:** four fixed equal-width bins of independently generated input difficulty. Intervals bootstrap paired case differences within each bin (2,000 resamples); they do not include retraining uncertainty.
- **Use for:** instance-level changes alongside layer behavior and predefined failure strata. Marginals share the main axes; no losing cases are filtered.
- [Editable SVG](gallery/cs-model-analysis.svg)

## CS factorial ablation

![CS factorial ablation](gallery/cs-factorial-ablation.png)

- Complete 2³ design with 16 shared seed IDs in every configuration. The left panel shows all seed outcomes, configuration means and 95% seed-bootstrap intervals; the binary strip documents factor membership.
- Component effects average on-minus-off over all settings of the other factors **within each seed**, then bootstrap those paired seed effects. These are marginal factorial effects, not leave-one-out effects from the full model.
- The A × B panel averages over C; connecting lines identify factor settings rather than continuous dose. The fixture deliberately includes a harmful regularizer and a non-additive interaction.
- **Use for:** component attribution when the full factorial experiment is available. Resample seeds jointly; do not infer interaction significance from nonparallel lines alone. Intervals are pointwise, without multiplicity adjustment.
- [Editable SVG](gallery/cs-factorial-ablation.svg)

## CS performance audit

![CS performance audit](gallery/cs-performance-audit.png)

- Four methods × four evaluated budgets × 20 matched seeds. Operating-point coordinates are median simulated latency and mean task score; connections only join measured fixture points, not a fitted optimum. Latency uses a log scale.
- Fixed-budget effects compare each method to the reference at budget 4 using the same seed IDs; intervals are 95% percentile bootstraps of paired seed differences (2,000 resamples). This is an equal-budget comparison, not an equal-latency comparison.
- The wide bottom strip shows ten tasks using the same method colors and symbols. Its 10 × 4 × 20 source tensor averages exactly to the fixed-budget seed scores, so the overview and task audit reconcile. Gray connectors group methods within a task, not an ordered method trajectory.
- **Use for:** performance/cost comparisons that retain heterogeneous task outcomes. Actual submissions should report hardware, timing protocol, warm-up and budget definitions; this fixture has no hardware-measured timings.
- [Editable SVG](gallery/cs-performance-audit.svg)

## Multi-track task fingerprint

![Multi-track task fingerprint](gallery/circular-fingerprint.png)

- 18 synthetic tasks, 24 shared seeds. Inner ring: updated mean (0–100); middle: paired gain (−10 to 10); outer: updated across-seed SD (0–8). Each track has its own explicit color scale.
- Chords include every baseline run-level task correlation with r ≥ 0.80; they show association, not causation. Correlations use the same shared-seed arrays.
- The companion scatter compares updated mean with seed variability, using group colors and distinct markers.
- **Use for:** multi-task profiles with stability and related task families. Read precise values from Cartesian panels rather than chord geometry.
- [Editable SVG](gallery/circular-fingerprint.svg)

## Representation landscape

![Representation landscape](gallery/representation-landscape.png)

- 360 paired synthetic 6D vectors across four predefined groups. PCA is fitted once to pooled before/after vectors; the main view and before inset share projection and axis limits.
- Contours are per-group KDE levels at 15%, 40% and 75% of peak density, **not confidence regions**. Relative levels do not encode equal probability mass.
- ECDFs and median/IQR intervals summarize after/before distance-to-group-centroid ratios in the original 6D space. Centroids are estimated from the displayed groups; projection separation alone is not evidence of representation quality.
- **Use for:** paired representation changes with a high-dimensional quantitative companion. Replace the fixture with actual embeddings and validate the relevant downstream metric.
- [Editable SVG](gallery/representation-landscape.svg)

## Matched evaluation flows

![Matched evaluation flows](gallery/evaluation-flow.png)

- The same 180 synthetic cases appear in three evaluation rounds. Fixed score bins are <35, 35–<65 and ≥65. Ribbon widths encode counts; every transition conserves its source and destination marginals.
- Side panels retain individual regressions and mean paired final-minus-initial changes by initial bin. Intervals are 95% percentile bootstraps over cases within each initial bin (2,000 resamples), not independent-run uncertainty.
- Initial-bin comparisons are descriptive and can be affected by regression to the mean. They do not establish subgroup treatment effects.
- **Use for:** tracking case transitions with consistent thresholds and case identities.
- [Editable SVG](gallery/evaluation-flow.svg)

## Benchmark atlas

![Benchmark atlas](gallery/benchmark-atlas.png)

- **Left:** baseline and updated means across 12 synthetic tasks; common radial offset, linear bar-length scale, no area encoding. The center is the equally weighted mean updated task score.
- **Right:** within-seed score changes for the same tasks. Points are mean paired changes; intervals are 95% percentile bootstrap CIs over eight shared seeds (2,000 resamples). Negative effects remain visible.
- **Use for:** a broad task inventory with a precise effect panel beside the overview. For fine ranking alone, use Cartesian comparisons.
- [Editable SVG](gallery/benchmark-atlas.svg)

## Paired estimation

![Paired estimation](gallery/paired-estimation.png)

- All 48 synthetic observations retain their before/after pairing. Offset violins summarize distributions without replacing the raw points.
- The KDE is descriptive; the rug shows each observed difference. Negative and positive regions share the same density estimate.
- Group intervals are 95% percentile bootstraps of paired changes within four predefined groups (12 cases/group). These are pointwise, not multiplicity-adjusted intervals.
- **Use for:** repeated measurements, per-query model changes and subgroup estimates. Groups must not be selected after examining the desired outcome.
- [Editable SVG](gallery/paired-estimation.svg)

## Quality and cost

![Quality and cost](gallery/quality-cost.png)

- Three synthetic samplers at NFE 4/8/16/32/64; the left panel connects only evaluated operating points. Latency is simulated, not hardware-measured.
- The fixed-budget panel shows median/IQR across 60 instances; the ECDF retains the whole error distribution. Distinct markers supplement the colors.
- **Use for:** paired-target reconstruction with an appropriate MSE definition. It is not an unconditional text-to-image quality evaluation; no Pareto or significance claim is inferred.
- [Editable SVG](gallery/quality-cost.svg)

## Reproduce

From the repository root:

```sh
uv sync --all-extras --locked
uv run python skills/scientific-figure-making/examples/showcase_gallery.py --out /tmp/prismatica-gallery
uv run python skills/scientific-figure-making/examples/advanced_showcase.py --out /tmp/prismatica-advanced
uv run python skills/scientific-figure-making/examples/cs_showcase.py --out /tmp/prismatica-cs
uv run python skills/scientific-figure-making/examples/cs_dense_gallery.py --inputs /tmp/prismatica-cs/cs-inputs.npz --out /tmp/prismatica-editorial
uv run python scripts/build_gallery_cover.py --gallery /tmp/prismatica-advanced --out /tmp/prismatica-cover
uv run python scripts/build_homepage.py --out /tmp/prismatica-homepage
```

Each figure script outputs three PNG/SVG/PDF figures, `showcase-inputs.npz`, `advanced-inputs.npz` or `cs-inputs.npz`, and `provenance.json` with the random seed and fixture status. Replace the data generation blocks with actual measurements and recompute all derived panels before publication.

The homepage displays complete dense compositions directly. `build_homepage.py` rebuilds the light/dark brand mastheads.

## Beyond this selection

The [full example index](examples.md) covers statistical composites, manuscript experiments, method overviews and image-led teasers. Those modes have different goals and visual conventions. Earlier [training](images/training-dynamics.png) and [factorial](images/factorial-interactions.png) fixtures remain available for regression/reference, but are no longer the homepage showcase.

## Set overlaps and shared cores

[Flower, UpSet and Jaccard compositions](set-overlap.md) accept item membership tables and preserve exact union, core, exclusive and inclusive pair counts. The bundled skill includes reusable Python plotting functions and editable vector exports.
