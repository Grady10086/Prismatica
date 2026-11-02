# The Trinity: benchmark-wide evolution and capability analysis

Reference: [The Trinity: Capability-Driven Recursive Self-Improvement for Multimodal Agents](https://arxiv.org/abs/2610.36077), The Trinity Research Team, arXiv:2610.36077v1, 2026. [PDF](https://arxiv.org/pdf/2610.36077). Inspected PDF pages 10–12 and their extracted text; version identifier appears on p1. This is a paper-specific reference, not a generic Nature profile.

## What to borrow

- **Fig. 5, PDF p11: grouped radial bars, Train / Unseen side by side.** A shared grey baseline plus four sequential pink/red iterations makes many benchmark trajectories visible in a compact overview. Bars use a 0–100 score scale and include benchmark labels around the circumference. Use for a broad benchmark inventory, not for precise ranking of nearly equal scores. Preserve the radial origin/range and group gaps. Radial bar *length*, not area, encodes score. Always provide a Cartesian alternative or data table for exact comparison. Benchmark-specific metrics on the same nominal scale are not automatically equivalent in meaning.
- **Fig. 6, PDF p11: split-specific iteration small multiples.** Common iteration positions, sparse markers, endpoint numbers, muted reference lines and a separate native-benchmark curve carry more information than a poster headline. Keep denominators explicit: the paper’s Train mean covers 28 benchmarks, native Train covers 17; its Unseen curve/reference means cover 16 non-robot benchmarks, while Fig. 5 includes 18 Unseen benchmarks. Do not merge those denominators or infer every mean from the radial chart. Macro-averaging is benchmark-equal, not pooled over instances.
- **Fig. 7, PDF p12: annotated diverging correlation matrix.** Six capability rows and six protocol columns; numeric coefficients make even pale cells readable. Keep a symmetric [-1,1] scale centered at zero, original signs, three decimals and full abbreviation definitions. The source describes correlations for 29 modules. Do not infer causal contributions or add significance marks/intervals without underlying data.
- **Table 4, PDF p12: routing quality and inference cost.** Plot Train/Unseen in separate panels using performance versus total inference tokens. Distinguish Random, self-routing, added capability definitions, added retrieved execution memory, and retrospective Oracle. The script abbreviates cumulative configurations as Self-routing / + Capability / + Memory; these are labels for the exact table rows, not isolated treatment effects. Connect only the first four configurations as a reading guide; Oracle remains separate.
- **Fig. 4, PDF p10: cost components and performance across iterations.** Useful for amortized setup/reuse costs. Prefer aligned panels with a shared iteration axis when dual axes would suggest an arbitrary association; do not tune axis limits to manufacture parallel trends.

The manuscript uses restrained burgundy/rose, grey reference marks, small legends and compact plot/table integration. Apply these choices to data density and hierarchy rather than adding large decorative titles.

## Reproduce verified numerical redraws

```sh
uv run --with matplotlib --with pymupdf python skills/scientific-figure-making/examples/trinity_data_reference.py \
  --paper /absolute/2610.36077.pdf --out /tmp/trinity-data
```

Depends on sibling `cs_paper_data_gallery.py` for typography only. Exports two 180-mm SVG/PDF/PNG figures plus source-data JSON: Fig. 7’s 36 correlation coefficients and Table 4’s 20 performance/token values. Constants are transcribed from PDF text, then checked against all 56 extracted values before rendering. Unexpected editions fail rather than silently mixing values. The output records PDF SHA-256, source URL and version. No original paper image/PDF is bundled. These are **redrawn published values**, not the paper’s original figure artwork and not our experiments. No unreported uncertainty is added. Original source attribution remains on each exported figure.

Capability abbreviations: PST=perception and state tracking; HCI=hypothesis and counterpart inference; CFR=constraint checking and feedback repair; GVT=goal commitment and value trade-off; VEA=video evidence acquisition; VC=video comprehension. Correlation columns are Perception, Memory, Inference, Planning, Orchestration and Loop.

For a user’s own experiments, use their values, denominator definitions and run-level uncertainty, remove Trinity-specific claims and update attribution consistently. Do not retain the paper’s numbers under another method name or estimate radial-bar values by eye. Appropriate original-image reuse terms still apply if distributing screenshots of the paper.

## Main overview figure

Fig. 1 is also included as a structural reference; read
[Trinity integrated overview](trinity-overview.md) for its paired hierarchies,
central three-role loop, six detail panels and performance inset. The renderer
exports `trinity-overview-original.png` from the supplied PDF as an unaltered
source reference, separately from the numerical redraws.
