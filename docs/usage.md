# Use Prismatica

## 1. Install the skills

Run `python3 scripts/install_skills.py` from a clone. It installs the unified entrypoint and both sibling modules. This only copies the skills; `uv sync --all-extras --locked` installs Python dependencies for running this repository's galleries.

## 2. Supply evidence and the intended use

For a data figure, give the data file, column meanings, experimental unit, run/item IDs, metric direction and insertion width. For an existing figure, include its script if available. For a method overview, give the actual components and interactions; for a teaser, give the matched input/results and their provenance.

Example data columns (an input convention, not a mandatory global schema):

| Column | Meaning |
| --- | --- |
| `method` | Stable method identity across plots |
| `seed` | Actual training/evaluation run identifier |
| `item_id` | Query/case identity for paired comparisons |
| `step` | Recorded epoch, iteration or sampling step |
| `metric` / `value` | Metric identity and observed value |

Missing records must remain missing. Multiple questions from one scene may require scene-level resampling. Per-case variability and training-seed uncertainty are different quantities.

## 3. Ask for a specific outcome

### Manuscript data figure

> Use $prismatica with results.csv. Compare three methods at matched seeds, show individual runs and 95% seed-bootstrap intervals, use a 180 mm double-column layout, and export editable SVG/PDF plus PNG. Report the resampling unit and missing-data handling.

### Improve an existing plot

> Use $prismatica to improve plot.py without changing values or statistical summaries. Reduce label collisions, unify method colors and legend order, and inspect the result at 85 mm width.

### Method overview

> Use $prismatica to organize my three actual components into a method overview. Put the closed loop at the center, connect detailed mechanisms to it, and use only the results I supplied in the evidence inset.

### Result-led teaser

> Use $prismatica to arrange these input/output images and recorded frames into a teaser. Keep sample order and crop identity, label the methods and source, and use a layout distinct from a three-column teaching diagram.

## 4. Review the deliverable

Check claim/plot fit → values and identities → uncertainty definition → visual hierarchy → final-size typography → accessible colors → vector export. A successful export or automated text check does not replace visually inspecting the actual figure.

## Color workflow

An existing project theme takes precedence. `paper-colors` can register colors from a user-supplied book and export theme files, then `scientific-figure-making` applies the roles to the selected composition. Color-book source files stay outside the repository. The Prismatica Iris identity is a brand palette, not a mandatory plot palette.

## What the example commands do

They generate known, labeled fixtures or process explicitly supplied paper assets. They do not automatically interpret arbitrary CSV schemas. Have the agent read your data and adapt the appropriate script. A paper-reference script is a design study, not a new experiment or model run.
