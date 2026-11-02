# CS experimental composition gallery

Use `examples/cs_analysis_gallery.py` for three complementary experiment layouts. The editorial serif title, warm ivory background, muted teal/blue/coral palette and varied panel proportions belong to a presentation profile. Adapt typography and figure size to the target venue for a manuscript.

```sh
uv run --with matplotlib python skills/scientific-figure-making/examples/cs_analysis_gallery.py --out /tmp/cs-analysis
```

Outputs: three PNGs, editable-text/vector SVGs and `demo-data.json`. All numerical values, model names and curves are synthetic demonstrations, explicitly labeled in the figures and JSON. The script does not load real benchmark results; replace the arrays and recompute all derived summaries before using it for a paper.

## Choose a composition

- **Representation**: one dominant layer-correspondence matrix, token-routing fractions and a categorical probe profile. The matrix is constructed similarity, NOT measured CKA or attention. Real replacements require a specified similarity estimator, sample set and layer alignment. Routing fractions must share a denominator and sum to one. Different probe tasks may need separate scales instead of an arbitrary shared score.
- **Factorial ablation**: all eight configurations for three binary factors, mean ± SEM over six synthetic seeds, a two-factor interaction panel averaged over the third factor, and marginal effects derived from the same runs. Marginal effects are averages over other conditions, not isolated removal effects. Do not fill in untested combinations; omit or mark them missing. Use paired uncertainty when actual runs share seeds and make uncertainty on effects explicit if drawing inferential conclusions.
- **Performance trade-offs**: quality versus latency with parameter-count area encoding, a two-objective Pareto frontier, robustness curves, budget scaling and task-specific deltas. Parameter count is a third descriptive variable and is not part of this frontier. Keep hardware, batch size, precision, timing protocol and evaluation set comparable. Here Delta/Elm task deltas average to their respective aggregate gains over Birch. Curves use synthetic point estimates without uncertainty; real repeated measurements should show their uncertainty.

Retain consistent model colors across all panels. Keep observed points visible; do not add smooth interpolations that imply unmeasured experiments. Axis truncation is appropriate for these point and line plots when labeled clearly; use zero baselines for magnitude-encoded bars. Large editorial titles must not reduce readable axis text in a final two-column paper.
