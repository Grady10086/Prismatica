# Interactive studio

[Open Prismatica online](https://grady10086.github.io/Prismatica/)

The GitHub Pages website complements the Python figure-making suite with thirty-two browser-native study presets across fifteen computational families. Every gallery card opens a live composition; no plot is a PNG masquerading as an interactive chart. The browser figures reinterpret the selected static studies rather than numerically reproducing every Python panel.

## Explore

- Change parameters to regenerate a deterministic demonstration. **New sample** increments the random seed; **Reset** restores the preset. The same seed and parameters reproduce the same browser dataset.
- Use three coordinated palettes. Hover marks to inspect values and highlight matching case/seed IDs in linked views.
- Use **＋** to zoom, drag to pan, or **Fit** to restore the full figure. **⤢** expands the interactive canvas where the browser supports fullscreen. Diffusion includes a trajectory time slider and playback.
- Open **Data studio** to edit CSV, import CSV/JSON or download the current measurements. Invalid schemas, duplicate observation keys and broken matched designs are rejected before replacing a figure. Parameter changes regenerate demonstration data; edits replace it. Import/export requires no server.
- Download editable **SVG** or a 2400 × 1488 **PNG**. Exports contain the complete figure, irrespective of the current zoom. **Copy link** shares seed, parameters, palette and study. It intentionally excludes imported data: share the CSV/JSON separately.
- Filter the collection by field or search by title/topic. Navigation and controls support keyboard input; decorative motion respects the system's reduced-motion setting and has a manual pause control. Main interface copy can switch between English and Chinese; scientific labels and schemas remain English.

## Evidence and statistical conventions

All browser datasets are synthetic fixtures unless a user replaces them. The diffusion plate performs actual probability-flow integration on a known two-dimensional Gaussian mixture using an analytic score. It does not run a pretrained image model. Browser random generation and intervals differ from the Python examples, so browser values should not be compared to screenshots as if they were identical experiments.

The browser uses pointwise **normal-approximate mean intervals** (`mean ± 1.96 × sample SD / √n`) where stated, not the Python bootstrap intervals. These intervals are illustrative, are not simultaneous, and should be revisited for small samples or bounded/discrete outcomes. Density curves are descriptive Gaussian KDEs. The Python workflow remains the route to final manuscript statistics and venue-specific typography.

| Family | Editable schema | Derived views |
| --- | --- | --- |
| Six-set overlap | `item,A,B,C,D,E,F` | Unique integer IDs, binary membership, at least one set per item; exact exclusive masks and inclusive pairs |
| Paired analysis / estimation | `case,group,before,after` | Paired observations, changes, density, group effects; groups 0–3 |
| Task fingerprints / atlas | `task,seed,baseline,updated` | Radial tracks, paired effects, seed variability; shared seed IDs required. Fingerprint chords select baseline correlations r ≥ .75, with no causal claim. |
| Full-factorial ablation | `config,seed,score` | All eight configurations (0–7), within-seed marginal effects and interactions; all configurations require the same seed IDs |
| Performance / quality–cost | `method,budget,seed,latency,error` | Three methods (0–2), common budget/seed identities, operating points, densities, ECDF and paired error reductions; latency is simulated in presets |
| Representation landscape | `case,group,x_before,y_before,x_after,y_after` | Paired **2D** vectors and group-centroid distance ratios; no PCA or higher-dimensional quality claim |
| Matched flows | `case,initial,round1,round2` | Conserved counts in bins <35, 35–threshold and ≥threshold; fixed bin threshold across all stages |
| Cross-modal retrieval | `query,candidate,baseline,updated` | Complete square cosine matrices over the same query/candidate IDs (max 64); single matching target per query, ranks, Recall@k and margins |
| Evidence conflict | `case,quality,text_strength,offset_visual,offset_text,offset_other` | Deterministic softmax probabilities under three conditions, argmax answer flows and selective risk. The response surface sets offsets to zero; it is not empirical confidence. |
| Diffusion numerics | `particle,x,y` | Geometric-noise-grid VE probability-flow ODE, same-start Euler/Heun/midpoint, finite σ=.01 endpoint. Error uses a 512-score-call Heun reference; checkpoint zoom limits are explicit, and central trajectories are clipped to the viewport. No perceptual/FID claims. |

Numeric input must be finite and within ±1,000,000; diffusion has tighter coordinate/particle limits. CSV quoting is unnecessary because the schemas contain numbers only. Maximum file size: 2 MB; maximum table size: 12,000 rows, with additional family-specific bounds. Data is held in page memory, including per-study edits; reload clears custom data. There are no analytics, remote fonts or runtime CDN dependencies.

## Develop and deploy

The site uses framework-free HTML, CSS and ES modules under [`site/`](../site/index.html). Relative URLs work under the `/Prismatica/` project path and on local servers.

```sh
python3 -m http.server 8877 --directory site
# Open http://127.0.0.1:8877/
uv run --with quickjs python scripts/test_web_models.py
```

The model checks execute the actual JavaScript modules with QuickJS, validate every preset at default and numeric parameter boundaries (96 complete SVG renders), and check deterministic sampling, CSV validation, retrieval ranking, matched effects, analytic-score gradients and numerical convergence. Browser QA additionally verifies editing, navigation, rendering, palette changes and downloads.

[The deployment workflow](../.github/workflows/pages.yml) validates and packages only `site/` with revisioned asset URLs, then publishes it after a matching push to `main`. Hosting does not require changing the repository's visibility. Model and data code is intentionally part of the public browser bundle; it contains no credentials.

The landing artwork uses the same Iris palette and original Möbius geometry as the README banner. Pointer motion eases the camera tilt; scrolling rotates and gently deforms the strip while preserving the half-twist seam. Silk, Wire and Contour are rendering styles for the same surface. Rendering is capped at approximately 30 fps, uses a smaller mesh on narrow screens, and suspends when offscreen or hidden. The pause control and system reduced-motion setting stop automatic animation.

Visual-direction references: [Active Theory](https://activetheory.net/), [Resn](https://resn.co.nz/) and [Codrops](https://tympanus.net/codrops/). The site uses an original particle sculpture, typography and interface; it does not copy their artwork or source. Scientific composition references remain documented in [the gallery](gallery.md) and [multimodal/diffusion studies](multimodal-diffusion.md).

The collection and laboratory share the Iris interface with a warm paper canvas. Study changes crossfade; compatible data changes interpolate SVG geometry for 230 ms. Dense figures use a short crossfade. Transitions can be interrupted by another edit, and both the pause control and reduced-motion preference disable them. SVG and PNG exports always use the final calculated figure, independent of any intermediate animation frame.

Use the panel selector above the figure to focus a single panel; Fit restores the complete composition. Click a keyed data mark to pin the same observation across linked panels. Clear selection or Escape releases it. Editing data clears the selection; exports contain the complete final figure without interactive dimming. Panel focus eases over 280 ms and respects reduced motion. Heatmaps use a sequential scale for non-negative ranges and a peach–paper–Iris diverging scale for signed ranges, with explicit endpoint legends.

## Expanded compositions

The collection now contains **32 compositions: six each in Multimodal, Generative and Model analysis, nine in Statistical, and five in Bioinformatics**. The original fifteen remain available at their existing study IDs. Nine additional views use the same validated input schemas; all panels are calculated from the imported observations or explicitly labelled toy integration.

| Study | Category | Additional analysis / layout |
| --- | --- | --- |
| `retrieval-ranks` | Multimodal | Tall query-level rank trajectories, paired log-ranks, four top-1 transition counts and ordered reciprocal-rank changes |
| `retrieval-directions` | Multimodal | Four directional recall curves, directional rank asymmetry, updated margins and per-pair rank gaps; reverse retrieval uses transposed matrices |
| `conflict-simplex` | Multimodal | Ternary probability trajectories, evidence balance and entropy–confidence diagnostics |
| `conflict-calibration` | Multimodal | Reliability bins, multiclass Brier distributions, selective risk and bin support |
| `diffusion-solvers` | Generative | Median and P10–P90 convergence bands, selected positions vs endpoint reference, ordered final errors and solver tails |
| `diffusion-modes` | Generative | Large particle map, nearest-target occupancy vs reference and displacement–error relationships |
| `sampling-budget` | Generative | Median and empirical P10–P90 budget curves, shared-seed gains between consecutive supplied budgets, fixed-budget effects and latency ECDFs |
| `sampling-tails` | Generative | Strict error exceedance, linked seed trajectories, fixed-budget operating points, paired effects and pooled upper-quartile exceedance counts |
| `paired-agreement` | Statistical | Difference-vs-mean view, mean ±1.96 SD descriptive limits, difference density, group shifts and all ordered observations |

Rank ties use the same optimistic rule as the original retrieval view: one plus the number of strictly greater similarities. Both directions preserve matched IDs. The calibration fixture defines the visual answer (class 0) as correct; ECE uses eight equal-width confidence bins, and multiclass Brier is the sum of squared differences from that one-hot target. Marker sizes show bin support. It is a descriptive toy-model analysis, not a claim about calibrated pretrained models. Ternary coordinates use normalized class probabilities; entropy is normalized by log(3).

Sampler bands are empirical 10th–90th percentiles across shared seeds or particles, **not confidence intervals**. Consecutive-budget gains are pooled descriptive differences and require at least two supplied budgets; a single-budget import displays an explicit missing-comparison message. Latency remains simulated in presets. Diffusion mode occupancy assigns each endpoint to the nearest of eight known centres; it is neither FID nor a learned generative-model benchmark. The 512-call Heun endpoint is a numerical reference, not an exact solution. Agreement limits describe observed differences and do not establish interchangeability or a confidence interval.

The Statistical category also includes three [set-overlap compositions](set-overlap.md): a schematic petal shared-core summary, an exact UpSet view and pairwise Jaccard analysis. This brings the collection to 27 views across fifteen computational families.

The [Bioinformatics guide](bioinformatics.md) specifies the five typed biological schemas, Newick import, local tissue images, validation limits and Python exports. These families accept text identifiers; earlier numeric schemas remain unchanged.


## Refined evidence inspection

The collection uses larger overview cards among smaller previews. All previews
retain the complete SVG composition. Alignment, representation and performance
plates use tighter panel spacing while preserving numerical scales and values.
Panel letters and fine dividers follow the selected chart palette in browser
and exported figures.

The palette selector includes the original Iris, Mineral and Spectral themes,
plus Tide and Ember. The latter are original role-based palettes inspired by
our art studies, not sampled artwork or Pantone-book matches. Palette changes
leave observations and derived results unchanged.

Select a data mark to pin its existing linked observation. The Linked Evidence
rail shows its tooltip values; use the previous/next buttons (also keyboard
focusable) to inspect other keyed observations. The order follows rendered
marks, not measured rank. Escape or Clear selection restores the complete view.
Hover frames and selection effects are omitted from canonical SVG/PNG exports.

For the underlying visual decisions and original sources see
[generative art studies](../skills/scientific-figure-making/references/generative-art-studies.md).


## Dark exhibition canvas

The collection and laboratory default to a dark canvas. The Dark canvas / Paper
canvas button switches both areas together without changing data or calculated
metrics. Display colors keep their hue families while lightness is adapted for
the background; legends use the same transform as the marks. Embedded local
images keep their pixels. Selection, zoom and data editing work in both views.

SVG and PNG export use the canonical light paper figure, independently of the
website canvas setting. This keeps manuscript outputs ready for a light page;
the button tooltips identify the export background.


Dark-view contrast uses brighter point and unfilled-path stroke paints, quieter
panel surfaces and readable coordinate labels. Point radii, weighted line widths,
opacity encodings and every data coordinate are preserved. Heatmap cells and
their legends share one color transform; local mark emphasis is limited to
explicitly tagged categorical point fills and series line strokes. Spatial
expression spots and other quantitative color mappings use the same transform
as their legends. Selection retains more surrounding
context, with a restrained halo on linked marks. Paper-view and export colors
remain independent of this display treatment.
