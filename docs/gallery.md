# Selected gallery

Three deliberately different compositions. These are original gallery designs with **synthetic inputs**, not screenshots from papers or performance claims. The readable gallery masters are 10.4 × 5.8 inches; adjust font sizes and dimensions for a specific manuscript venue.

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
```

Output: three PNG/SVG/PDF figures, `showcase-inputs.npz`, and `provenance.json` with the random seed and fixture status. Replace the data generation blocks with actual measurements and recompute all derived panels before publication.

## Beyond this selection

The [full example index](examples.md) covers statistical composites, manuscript experiments, method overviews and image-led teasers. Those modes have different goals and visual conventions. Earlier [training](images/training-dynamics.png) and [factorial](images/factorial-interactions.png) fixtures remain available for regression/reference, but are no longer the homepage showcase.
