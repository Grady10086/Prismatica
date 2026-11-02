# Layout at publication size

## Size and typography

Use the venue's actual column width when known. `figure_size(90, height_mm=62)`
means 90 × 62 mm, not pixels. At 100% insertion, 8 pt figure text remains 8 pt;
placing a 178 mm figure at 85 mm shrinks it to about 3.8 pt. Avoid this by plotting
at the intended width. Start with 8 pt labels/ticks and check the venue's minimum.
Use a font installed on the rendering machine; use the paper's font when available.
DejaVu Sans is a portable default, not a venue prescription. Match math fonts if
mixing mathtext and prose. Do not enable `text.usetex` without a working TeX setup.

## Axes and legends

Label quantities and units. Preserve meaningful limits and scales; bars normally
start at zero. Distinguish truncated axes clearly. State uncertainty type and
sample count in the caption; never invent error bars. Use sparse major ticks
rather than long, rotated tick labels. For long categories prefer horizontal bars.
Avoid smoothing or interpolation that changes the result's interpretation.

Use concise legend labels and a stable method order, with ours first when that
matches the paper's conventions. Prefer an unused region of the axes. If crowded,
place an axes legend outside with `bbox_to_anchor=(1.02, 1), loc="upper left"`
and allow constrained layout space, increase the canvas, or split panels. Check
that the legend does not cover results. Figure-level legends need explicit space
planning and visual verification across matplotlib versions.

## Multiple panels and heatmaps

Create axes with `layout="constrained"`; do not call `tight_layout()` afterwards.
Share axes only when quantities, units and scales match. Use a common legend for
repeated methods where space permits. Set short panel titles such as `(a) Accuracy`
and `(b) Latency`; keep title baselines aligned. Give each subplot enough physical
width for its labels. Increase height or use a double-column layout before reducing
font size. Colorbars need units and readable ticks; attach them to their intended
axes with `fig.colorbar(..., ax=ax)`. Set meaningful normalization consistently
across comparable heatmaps. Keep heatmap spines as needed rather than applying
line-chart conventions blindly.

## Export and review

PDF/SVG retain lines and text as vectors. Dense point clouds may use
`rasterized=True` on just the relevant artist; PNG DPI also controls those raster
layers in PDF. Prefer an opaque background unless the destination needs transparency.
`save` keeps the physical canvas size; move overflowing artists inside the canvas
instead of relying on tight cropping, which changes the output dimensions.

Review the PNG and the actual vector file in the paper. Check text, legends,
colorbars, clipped labels, panel spacing and grayscale distinctions. The helper
checks visible Text bounds and font sizes, not pairwise overlaps or color safety.
Never claim visual verification if no image viewer was used.

References: matplotlib's [constrained layout guide](https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html)
and [savefig API](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html).
