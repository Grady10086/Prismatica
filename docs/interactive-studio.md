# Interactive studio

[Open Prismatica online](https://grady10086.github.io/Prismatica/)

The GitHub Pages website complements the Python figure-making suite with fifteen browser-native study presets across nine computational families. Every gallery card opens a live composition; no plot is a PNG masquerading as an interactive chart. The browser figures reinterpret the selected static studies rather than numerically reproducing every Python panel.

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

The model checks execute the actual JavaScript modules with QuickJS, validate every preset at default and numeric parameter boundaries (45 complete SVG renders), and check deterministic sampling, CSV validation, retrieval ranking, matched effects, analytic-score gradients and numerical convergence. Browser QA additionally verifies editing, navigation, rendering, palette changes and downloads.

[The deployment workflow](../.github/workflows/pages.yml) validates and packages only `site/` with revisioned asset URLs, then publishes it after a matching push to `main`. Hosting does not require changing the repository's visibility. Model and data code is intentionally part of the public browser bundle; it contains no credentials.

The landing artwork uses the same Iris palette and original Möbius geometry as the README banner. Pointer motion eases the camera tilt; scrolling rotates and gently deforms the strip while preserving the half-twist seam. Silk, Wire and Contour are rendering styles for the same surface. Rendering is capped at approximately 30 fps, uses a smaller mesh on narrow screens, and suspends when offscreen or hidden. The pause control and system reduced-motion setting stop automatic animation.

Visual-direction references: [Active Theory](https://activetheory.net/), [Resn](https://resn.co.nz/) and [Codrops](https://tympanus.net/codrops/). The site uses an original particle sculpture, typography and interface; it does not copy their artwork or source. Scientific composition references remain documented in [the gallery](gallery.md) and [multimodal/diffusion studies](multimodal-diffusion.md).

The collection and laboratory share the Iris interface with a warm paper canvas. Study changes crossfade; compatible data changes interpolate SVG geometry for 230 ms. Dense figures use a short crossfade. Transitions can be interrupted by another edit, and both the pause control and reduced-motion preference disable them. SVG and PNG exports always use the final calculated figure, independent of any intermediate animation frame.

Use the panel selector above the figure to focus a single panel; Fit restores the complete composition. Click a keyed data mark to pin the same observation across linked panels. Clear selection or Escape releases it. Editing data clears the selection; exports contain the complete final figure without interactive dimming. Panel focus eases over 280 ms and respects reduced motion. Heatmaps use a sequential scale for non-negative ranges and a peach–paper–Iris diverging scale for signed ranges, with explicit endpoint legends.
