# Complex data compositions: inspected Nature Portfolio references

These original layouts draw on the evidence hierarchy of published figures. They
are not reproductions, borrowed results, or claims of submission compliance.

## Visually inspected primary references

1. **AutoFocus: a hierarchical framework to explore multi-omic disease associations spanning multiple scales of biomolecular interaction**, Communications Biology (2024),
   [paper](https://www.nature.com/articles/s42003-024-06724-2), Fig. 2, PDF p. 4.
   Panel b combines a small numeric correlation matrix and coefficient scale;
   panel c places a densely populated hierarchical tree over a platform annotation
   strip, with a separate categorical legend. Borrow the aligned tree/strip/matrix
   vocabulary and the distinction between categorical and continuous colors.
   Our two-axis clustered heatmap is an original extension, not its Fig. 2c.
2. **Correlations reveal the hierarchical organization of biological networks with latent variables**, Communications Biology (2024),
   [paper](https://www.nature.com/articles/s42003-024-06342-y), Fig. 5, PDF p. 7.
   Panels c and d align spike observations with small correlation matrices and
   statistical summaries below. Borrow the whole-to-detail arrangement, matched
   observed variables and consistent ordering. Our example uses descriptive Pearson
   coefficients only; it does not reproduce the paper's modularity hypothesis tests.
3. **Combining remote sensing with local knowledge is vital for understanding forest change in West Africa**, Scientific Reports (2025),
   [paper](https://www.nature.com/articles/s41598-025-23133-5), Fig. 2, PDF p. 4.
   Nine small-multiple Sankey diagrams retain land-cover class colors across time;
   ribbon width represents area. Borrow conserved flows, persistent categories and
   restrained translucent links. Our ribbons represent integer case counts, not area.

All three PDFs were downloaded and their figure pages visually inspected during
this expansion. References document layout inspiration; demo measurements are not
extracted from these papers. No paper images are bundled into the skill.

## Three original compositions

- **Clustered response atlas**: two dendrograms, categorical cohort strip, 24×36
  row-standardized heatmap, feature-aligned cohort profiles and raw column means.
  Standardize each feature using sample SD (`ddof=1`); average-linkage Euclidean
  distance on standardized rows and columns; optimal leaf ordering. Apply identical
  leaf permutations to annotations and companion panels. Side profiles are cohort
  means at each discrete feature; connecting lines are reading guides. Fixed z scale
  −3 to +3; check real ranges before reusing. Raw means are only meaningful when
  features share units; otherwise remove that panel.
- **Correlation architecture**: dendrogram and lower triangle, example pair in raw
  units, distribution of all 66 unique variable pairs. Pearson correlations use all
  160 matched finite cases; average linkage on `1−r`, not `1−abs(r)`. Fixed scale
  −1 to +1. Numeric labels for `abs(r) >= .6` are a display rule, not a significance
  threshold. No p-values or inference from the histogram's dependent pair counts.
- **Transition observatory**: three conserved stages, case-level final-score
  distributions and stage composition bars. Every one of 240 cases has a category
  at each stage. Ribbon width is proportional to count with one global scale;
  every intermediate node has equal incoming and outgoing totals. Ribbons inherit
  the source category of each adjacent transition. Adjacent tables do not visually
  track a full three-stage path; use saved case records if full paths matter.
  Violin fills are descriptive KDE; every case is shown, with a white median dot.
  No uncertainty intervals or significance claims. Categories 1–3 retain their
  meanings across stages; new states need explicit separate labels.

Missing values, unmatched cohorts and constant variables are not silently imputed.
Real work must state missing-data policy and observational unit; use a design-
appropriate correlation method and uncertainty analysis if inference is requested.
Synthetic seed is 91; plotting jitter seed is 3. Data, case IDs (record row index),
leaf orders, standardized matrix, correlations, transition tables and stage counts
are exported for audit. No bootstrap or fabricated significance annotations.

## Reproduce

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_complex_gallery.py --demo --out /tmp/nature-complex
```

Optional `--colors PATH` accepts a paper-colors Python export. Otherwise the test
palette is exported locally. Outputs are three SVG/PNG compositions, synthetic
input-data.json, computed-summaries.json and captions.txt. SVG text remains editable.
The CLI only generates explicit demos; plotting functions can be adapted to validated
project arrays. Choose axes, units, sample matching and ranges for those data rather
than retaining the demo's labels or claiming the synthetic footer as experimental
results. Each figure uses 183 mm width and 125–130 mm height. Inspect at final size.

## Association modules and transition fingerprints

Two further original studies use the same inspected references above. The network
view extends the whole-to-detail organization of Communications Biology Fig. 5;
it does not infer that paper's latent functional organization. The four-cohort
flow view extends Scientific Reports Fig. 2's small-multiple organization.

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_network_gallery.py --demo --out /tmp/nature-network
```

**Association modules** juxtaposes an undirected thresholded graph, full reordered
correlation matrix, displayed degree and module-level mean correlations. Modules
M1–M3 are predefined synthetic groups, not algorithmically discovered communities.
Use average Pearson r over unique off-diagonal pairs for within-module cells;
between-module cells average unique cross-group pairs. These are descriptive
summaries, not pooled effect estimates or statistical tests. Node positions are
fixed on a circle; distance and closeness have no analytical meaning. Edges satisfy
`abs(r) >= .75`, with width `.3 + abs(r)` points. Solid gray indicates positive
association; dashed rose indicates negative association if present. The threshold
is for display, not significance. Degree changes with threshold; the complete
matrix preserves all coefficients. The current synthetic example has positive
edges only. No directional or causal claim is implied.

**Transition fingerprints** compares four cohorts of 180 synthetic cases, each
starting with 60 cases in each of three categories. Record row indices identify
cases within each cohort; rows are not matched across different cohorts. Each
cohort has an input and final category. Ribbon widths share one count scale because
all four totals equal 180; unequal totals require a global count scale rather than
per-panel normalization. Matrices are conditional probabilities, each input row
summing to 1 before percentage-label rounding. Matrices share a 0–1 color scale. Unchanged category is trace(table)
divided by total; it is not clinical survival, model success or a causal effect.
The final stacked bars use the same category colors and a common 0–100% axis.
Generation seed is 819. This comparison is descriptive and contains no confidence
intervals or significance claims.

Both studies export editable SVG/PNG and `data-and-summaries.json` with synthetic
features, edge list, degree, predefined module assignments, module mean r,
case-level transition records and count tables. The CLI requires explicit --demo.
For real data, document category meanings, case identity, missing-data policy,
units and thresholds, then adapt the plot functions and replace the synthetic
labels. Never relabel these generated measurements as actual project results.
