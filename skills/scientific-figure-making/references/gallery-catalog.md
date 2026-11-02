# Scientific figure making

Make data figures readable at their final size in the paper. First release targets
Python 3.10+ and matplotlib 3.6+. Helpers live in `scripts/paper_layout.py`; copy
that standalone module beside the project's figure scripts when useful.

## Workflow

1. Inspect the existing plotting script, data and paper template. Keep scientific
   content, uncertainty definitions and method identities intact. Determine the
   intended width in millimetres and panel arrangement. If no venue dimensions are
   available, start at 85 mm single-column or 178 mm double-column, explicitly
   treating these as defaults rather than venue requirements.
2. Use the existing project palette. When `paper_colors.py` exists, import its
   `apply`, `style` and role map. For palette creation or changes, use the sibling
   [paper-colors](../../paper-colors/SKILL.md) if installed. This skill also works
   alone with the user's existing colors; it does not require a color book.
3. Set typography before creating artists and construct the figure at its intended
   physical size. Read [layout guidance](layout.md) for crowded legends,
   heatmaps and multi-panel arrangements. Do not shrink everything to force a fit.
4. Export PDF or SVG plus a PNG preview using `save`. Run `inspect` and resolve or
   explain its findings. Open the exported preview, inspect clipping and overlaps,
   and check the figure at its intended insertion size. A clean report alone does
   not establish that the figure is readable. If paper-colors is available, also
   run its lint and inspect a grayscale rendering for series distinguishability.
5. Keep the reproducible script, data provenance and output together. Report the
   final dimensions, formats, and any remaining limitations. Record the intended
   LaTeX inclusion width so later resizing does not silently shrink the text.

## Minimal use

```python
import matplotlib.pyplot as plt
import paper_layout as layout
from paper_colors import apply as apply_colors, style  # existing project export

layout.apply(font_size=8)
apply_colors()  # either order: layout never writes axes.prop_cycle or image.cmap
fig, ax = plt.subplots(figsize=layout.figure_size("single"), layout="constrained")
ax.plot([1, 2, 3], [70, 76, 80], label="Ours", **style(0))
ax.set(xlabel="Training steps (thousands)", ylabel="Accuracy (%)")
ax.legend()
print(layout.inspect(fig))
layout.save(fig, "figures/accuracy")
plt.close(fig)
```

`settings()` returns an rcParams dictionary for scoped use with
`matplotlib.rc_context(layout.settings())`. `figure_size` also accepts a numeric
width and `height_mm`; `save` accepts `formats=("pdf", "png")` and `dpi=300`.
It preserves canvas dimensions instead of cropping with `bbox_inches="tight"`.
`inspect` checks small text and text outside the canvas; it cannot detect all
collisions, validate data, or guarantee vector-backend text metrics match Agg.
SVG keeps text editable and requires the font on the receiving machine; PDF uses
TrueType fonts. External TeX rendering is optional and remains caller-controlled.

## Nature main figures (optional)

For Nature-style requests, read [Nature sources and patterns](nature.md).
Use `scripts/nature_profile.py` for 89/183 mm widths, 5–7 pt ordinary text,
8 pt bold lowercase panel letters and lighter strokes. Call `nature_profile.apply()`
in place of the general `layout.apply()`, then apply the existing paper-colors theme.
Do not override the generic defaults for other venues or assume these settings
apply to every Nature Portfolio journal or Extended Data. The reference separates
published production requirements from Nature Methods design recommendations.
It also links a reproducible three-panel example with raw observations and a heatmap.

## Nature Portfolio data charts

For benchmark data, training runs, ablations, sample distributions, paired
measurements or efficiency plots in a Nature-style request, read
[the data-chart casebook](nature-data.md). It distinguishes inspected
Nature, Nature Methods, Nature Machine Intelligence and Nature Communications
panels from our adaptations. Use `scripts/nature_charts.py` on verified data;
`examples/nature_data_gallery.py --demo` generates six explicitly synthetic
examples and a composite. Declare the observational unit and distinguish SD,
SEM, confidence intervals and predictive/member spread. Preserve unit pairing,
missing values and raw observations; do not invent significance or smooth data
as part of styling. The optional Nature profile does not replace other venues.

## Research composition references

For AMI-related work, World Labs, Yiming Li (Tsinghua), Shuicheng Yan or research
teasers, read [the source casebook](research-patterns.md). It records
specific inspected figures and separates observations from adaptations. Choose
compositions by the research claim, not an invented author-style preset. Use the
project's native vector tools and paper-colors diagram roles for implementation.

## Scene-first project teasers

For expressive project teasers or feedback that a diagram looks generic, read
[teaser design](teaser-design.md). Make the actual scene, input or result
the dominant visual. Use the three original vector studies to explore hierarchy,
then substitute real project assets and evidence. The earlier box-based example
is a teaching aid, not a visual-quality target. Match the user's chosen direction.

## Multimodal, generative and robotics teasers

For visual QA, conditional generation, controlled sample grids or robot policy
figures, read [domain-specific teasers](domain-teasers.md). It links
inspected primary sources and provides four original templates with different
visual subjects. Use image slots to insert actual project inputs/results; update
example captions to match them. Do not reuse a city/voxel scene for unrelated tasks.

## Image-led teasers with actual results

When the user wants more refined layouts, actual photos or published/project
outputs instead of teaching diagrams, use [result-first teasers](result-first-teasers.md).
Choose among the asymmetric edit atlas, visual case with detail crop/evidence,
and ordered robot ribbon. These have distinct compositions rather than one
three-column skeleton. Prefer this workflow over the vector placeholder galleries
when actual inputs/results are available. Retain source labels and distinguish
published references from new project results. Never invent scores or a model run.

## Recent conference figure references

For recent best-paper figures or influential model-report visuals, read the
[2025–2026 figure casebook](recent-paper-figures.md) and its linked
catalog. Twelve inspected papers cover eight conferences plus a video report.
Choose by the visual evidence: scene reconstruction, material detail, physical
assembly, contextual deployment, concept composition or interactive video
refinement. Awards and design suitability are separate; preserve the exact award
category. The local atlas builder renders primary-PDF excerpts without downloads.

## Video, 3D and manipulation sequences

For image-dense video generation, multiview 3D or manipulation teasers, read
[sequence teasers](sequence-teasers.md). Six additional presets cover
a cinematic output with filmstrip, method proofsheet, mesh stage, surface comparison,
robot task diptych and four-task mosaic. Prefer short labels over explanatory
cards. Use actual ordered samples and matched comparison conditions; never
invent motion frames, camera angles, success labels or timestamps.

## Reproducible examples

From the repository root:

```bash
uv run --with matplotlib python skills/scientific-figure-making/examples/make_examples.py --out /tmp/beautify-figures
uv run --with matplotlib python skills/scientific-figure-making/examples/nature_panels.py --out /tmp/beautify-nature
uv run --with matplotlib python skills/scientific-figure-making/examples/research_composition.py --out /tmp/beautify-research
uv run --with resvg-py python skills/scientific-figure-making/examples/teaser_gallery.py --out /tmp/beautify-teasers --png
uv run --with resvg-py python skills/scientific-figure-making/examples/domain_teasers.py --out /tmp/domain-teasers --png
```

The first command produces a method comparison, an ordered ablation, and a two-panel
figure as PDF/SVG/PNG; the second demonstrates the Nature profile. Both use
deterministic synthetic measurements and the existing test palette. Examples export
that palette into their output folder; they never read or modify the user's color
registry. Synthetic results are demonstrations only.

The scene-first gallery produces three editable SVG studies with optional PNG
previews. SVG generation uses the standard library; `--png` requires resvg-py.
`--tokens` accepts the project's paper-colors JSON export. See the teaser reference
for provenance and final-size review. All geometry and example results are synthetic.

## Rich statistical compositions

When users want more visually varied data figures, read
[rich statistical compositions](rich-data.md). Six additional examples
cover raincloud distributions, paired bootstrap estimation, joint density with
marginals, score/count bubble matrices, tied-rank trajectories and ridgelines.
Use `scripts/rich_charts.py` for the statistical primitives. Preserve raw values,
matching identities, uncertainty definitions and accessible paper-colors roles.
The demo CLI explicitly requires `--demo`; it is not a real-data ingestion tool.

For complex clustered heatmaps, correlation matrices and Sankey composites, read
[complex data compositions](complex-data.md). Three visually inspected
Nature Portfolio papers motivate original layouts with aligned dendrograms,
annotation strips, raw-data detail views and conserved transitions. Reproduce via
`examples/nature_complex_gallery.py --demo --out PATH`. Keep every reordered
annotation aligned; distinguish correlation display thresholds from significance;
validate stage counts and identity matching before drawing flows.

For network–matrix–module combinations or multi-cohort Sankey comparisons, use
`examples/nature_network_gallery.py` and the additional guidance in
[complex data compositions](complex-data.md). Fixed graph geometry
has no distance meaning; displayed degree depends on the edge threshold. Shared
flow widths must represent the same count across panels, while conditional
transition matrices use explicit row normalization.

For spatial context with linked zooms, event rasters with aligned traces, or
exclusive-set overlap with ECDF/PCA quality-control panels, read
[diverse data compositions](diverse-data.md) and use
`examples/nature_diverse_gallery.py`. These studies cite three additional inspected
Nature Portfolio figures. Preserve spatial units and matched identities; distinguish
parametric illustration from measured trajectories; state the exclusive meaning
of UpSet combinations and the population behind each distribution.

For circular multi-track atlases, dose-response fit/residual/EC50 combinations, or
Kaplan–Meier/censoring/risk-table compositions, read
[advanced data compositions](advanced-data.md). Use
`examples/nature_advanced_gallery.py --demo --out PATH` and the explicitly scoped
primitives in `scripts/advanced_stats.py`. Keep radial scales and link selection
explicit, choose dose models and resampling units from the assay, and calculate
risk tables and censor marks from the same case records as the survival curve.

For volcano/MA/raw-observation layouts, overrepresentation/rank-profile/set-member
compositions, or forest/precision/leave-one-out combinations, read
[inference data compositions](inference-data.md) and use
`examples/nature_inference_gallery.py`. Define the full correction family, tested
background and overlap denominator explicitly. Keep ORA separate from rank-profile
inference, and preserve effect type, interval method and study independence in
forest figures. Scoped primitives live in `scripts/inference_stats.py`.

For ternary composition shifts, analytic vector-field/trajectory/section layouts,
or calibrated multiscale spatial views, read
[geometric data compositions](geometry-data.md) and use
`examples/nature_geometry_gallery.py`. Reject silently unclosed compositions;
distinguish streamline geometry from time-integrated paths; preserve original
spatial units, category identities and nested crop IDs. Scoped contracts are in
`scripts/geometry_charts.py`.

For ROC/PR with scalar uncertainty, reliability/support/ECE/Brier combinations,
or decision-curve/net-benefit/action-burden layouts, read
[prediction evaluation compositions](prediction-data.md) and use
`examples/nature_prediction_gallery.py`. Preserve matched cases, explicit positive
class and prevalence. Distinguish AP from trapezoidal PR area, bin-rate intervals
from calibration bands, and unstandardized net benefit from clinical effectiveness.
Use out-of-sample predictions and design-appropriate resampling for real work.

For evidence-led figures built around failure examples, controlled input branches
or empirical capability landscapes, read
[narrative data layouts](narrative-data.md) and use
`examples/nature_narrative_gallery.py`. This demo trains a real classifier on the
bundled digits dataset, linking observed failures, actual image variants and
measured condition grids. Preserve sample/split identities and example-selection
rules; distinguish sensitivity interventions from causal counterfactual inference,
and show which landscape values were actually evaluated. Never invent result
images, failure mechanisms or untested condition cells to improve composition.

When users prioritize beauty and image-led editorial presentation, read
[editorial image studies](editorial-images.md) and use
`examples/editorial_image_gallery.py`. Three distinct palettes/compositions use
real microscopy, astronomy and retinal sample images with exact linked crops and
pixel-derived measurements. These large-format teaser/talk studies are separate
from the Nature main-figure typography profile. Keep source credit, original image
intensities, crop identities and honest statistical semantics while changing the
visual hierarchy; do not replace missing evidence with decorative “results”.

For more image-led editorial layouts using volumetric fluorescence, recorded
materials sequences, dual-channel live-cell images or botanical microscopy, read
[editorial sequences](editorial-sequences.md) and use
`examples/editorial_sequence_gallery.py`. Preserve source credits, shared display
limits across channels/time and actual sequence order. Declare maximum projections,
false-color LUTs and percentile clipping; do not invent intervening frames, time
intervals, molecular colocalization or measured motion from page arrangement.

For image-first **CS** teasers, read [CS editorial layouts](cs-editorial.md)
and use `examples/cs_editorial_gallery.py` with local assets prepared by
`examples/prepare_sequence_references.py`. Choose video hero + filmstrip, 3D object
stage or robot task sequences according to the evidence. Preserve input/output
identities, original sample order and source attribution; these published reference
studies are not new inference. Prefer relevant CS result imagery over microscopy
when the user is making a computer-science paper.

For CS experiment figures beyond teasers, read [CS analysis compositions](cs-analysis.md)
and use `examples/cs_analysis_gallery.py`: representation/routing/probes, complete
factorial ablation with derived effects, and efficiency/robustness/budget/task
comparisons. The bundled values are labeled synthetic demonstrations. Replace
inputs and recompute summaries together; preserve uncertainty definitions, factor
coverage, consistent model colors and the objectives defining any Pareto frontier.

For more visual CS diagnostics, read [training, attention and failure compositions](cs-diagnostics.md)
and run `examples/cs_diagnostic_gallery.py`. Its three layouts use actual local
digits-model outputs: checkpoint observatory, patch-attention studio and error/control
casebook. Keep model weights distinct from causal explanations, disclose post-hoc
example selection, and preserve sample identity across checkpoints and comparisons.

For image-rich multimodal and diffusion experiment layouts, read
[multimodal/diffusion compositions](multimodal-diffusion.md) and run
`examples/multimodal_diffusion_gallery.py` with local published PDFs. It provides
a same-image response audit, guidance-sweep/result-comparison atlas, and diffusion
cross-attention process study. Preserve method/input identities, mark paraphrased
answers, and distinguish attention maps from decoded denoising intermediates.

For recent-paper reference compositions with recorded denoising snapshots,
cross-modal evidence and correction failures, read [2025 multimodal layouts](recent-multimodal.md)
and use `examples/recent_multimodal_gallery.py`. Keep independent trajectories and
independent papers separate, distinguish selected generation states from every
consecutive timestep, and retain authorship of panels labeled “Ours”.

When the user asks for **manuscript experimental data plots**, prioritize
[CS paper data figures](cs-paper-data.md) and
`examples/cs_paper_data_gallery.py` over the editorial galleries. Use the 180-mm
compact subplot profile, actual data and defined uncertainty; do not substitute
large headline layouts or collages of unrelated published panels. The bundled
training/alignment/reconstruction inputs are explicitly synthetic fixtures.

For additional manuscript data layouts, use [CS paper comparisons](cs-paper-comparisons.md)
and `examples/cs_paper_comparisons.py`: full factorial ablation, modality-conflict
outcome analysis and sampler quality/cost distributions. Derive paired contrasts
before resampling; distinguish sample variation from uncertainty and synthetic
latency/error fixtures from actual measurements.

For benchmark-wide iteration comparisons and capability/module analyses, read
[The Trinity figure reference](trinity-paper.md): grouped radial bars
(Fig. 5), split-specific iteration curves (Fig. 6), annotated correlation matrices
(Fig. 7), and routing performance/token comparisons (Table 4).
`examples/trinity_data_reference.py` redraws verified explicit published values
from a supplied PDF; keep source attribution, split denominators and Oracle status.

For a dense method **overview/main figure** combining task scope, a central
feedback loop, implementation details and a small evidence inset, read
[Trinity Fig. 1 overview reference](trinity-overview.md). It is a
method-composition option, not the default style for experimental data plots.
Adapt the structure to the actual method; the original Fig. 1 can be extracted
from a supplied paper using `examples/trinity_data_reference.py`.
