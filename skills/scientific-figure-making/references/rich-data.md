# Rich statistical compositions

Use `examples/nature_rich_gallery.py` for six additional compositions. These are
Nature-informed visual studies, not copied paper panels or a journal compliance
certification. Keep the role palette exported by paper-colors and editable text.

| Composition | Appropriate evidence | Required interpretation |
| --- | --- | --- |
| Raincloud | Several observed distributions | Points are observations; thick line is IQR; dot is median. Independently normalized KDE peaks compare shape, not prevalence. |
| Paired estimation | Before/after on the same independent units | Preserve matching IDs. Bootstrap the paired differences, not separate groups. Percentile intervals are not BCa intervals. |
| Joint density + marginals | Two measurements on matched cases | Report the unit and n. Pearson r is descriptive; contours are density levels, not probability coverage. |
| Bubble matrix | Method-by-dataset scores with differing sample counts | Encode count by marker AREA, label its legend; fix color limits across comparisons. |
| Rank trajectories | Method ordering across discrete tasks | Average tied ranks; preserve original scores. Lines are visual guides, not interpolation; rank gaps are not effect sizes. |
| Ridgeline | Ordered distributions with enough observations | Share the x scale and density scale. Rugs retain observations. 5th–95th percentiles describe data, not uncertainty of the mean. |

Run from the repository root:

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_rich_gallery.py --demo --out /tmp/nature-rich
```

Optional `--colors /absolute/path/paper_colors.py` accepts an existing paper-colors
Python export. The default uses the same test fixture as the basic data gallery.
Outputs: six individual SVG/PNG figures, a composite, raw synthetic JSON, computed
summaries and captions. `--demo` is mandatory so synthetic examples cannot silently
stand in for measurements. For real work, import the plotting functions with your
validated arrays, paired IDs and units, replace the demo captions and footer, and
record the provenance. Do not describe this demo CLI as a generic data-file loader.

The estimation primitive uses 5000 paired resamples with a fixed seed. Independent
cases are assumed; clustered, longitudinal or repeated measurements need a design-
appropriate bootstrap. KDE is descriptive; tiny or constant samples should use raw
points rather than a smooth density. The primitive returns a degenerate point for
constant observations; callers should draw that as a point rather than normalize
zero density. Joint KDE requires a nonsingular covariance matrix. Do not crop values
outside the example score limits; choose limits from real data and meaningful units.

Primary implementation references:
- [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html): paired resampling and confidence-interval methods.
- [SciPy gaussian_kde](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html): bandwidth and covariance limitations.
- [SciPy rankdata](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rankdata.html): explicit average handling of ties.

See `nature-data.md` for the inspected Nature Portfolio papers and production
constraints. Select compositions by the evidence, rather than adding density,
color or statistical annotations solely for decoration.
