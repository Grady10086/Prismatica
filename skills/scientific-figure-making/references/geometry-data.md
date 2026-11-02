# Ternary, vector-field and multiscale spatial compositions

Three original geometric layouts reference these visually inspected primary figures.
Published images and reported measurements are not bundled into the skill.

## Inspected references

- [Costs of transitioning the livestock sector to net-zero emissions under future climates](https://www.nature.com/articles/s41467-025-59203-5), Nature Communications 16, 3810 (2025), Figs. 3–4, PDF pp. 5–6. The paper combines trade-off ternary views, scenario labels and complementary measurements for 2030/2050. Borrow the triangular trade-off overview and paired contextual views. Its metrics are normalized scenario factors; our example is instead a strict three-part composition summing to one. Do not silently interpret arbitrary three-metric scores as compositional data.
- [GraphVelo allows for accurate inference of multimodal velocities and molecular mechanisms for single cells](https://www.nature.com/articles/s41467-025-62784-w), Nature Communications 16, 7831 (2025), Figs. 2–3, figure artwork on PDF pp. 5 and 7, captions on pp. 6 and 8. Figure 2 juxtaposes simulated continuous vector fields and trajectories across linear, cyclic and branching manifolds; Fig. 3 combines velocity fields, phase portraits and projection detail. Borrow vector/trajectory/detail organization. Our field is a defined physical-coordinate analytic example, not inferred RNA velocity, cellular fate or an embedding projection. Millimetres and seconds cannot be assigned to an RNA-velocity embedding by analogy.
- [Left-handed DNA for efficient highly multiplexed imaging at single-protein resolution](https://www.nature.com/articles/s41467-025-64228-x), Nature Communications 16, 8773 (2025), Fig. 2, PDF p. 4. An overview neuronal atlas is combined with target-specific maps, synapse views, organelle details and calibrated scale bars. Borrow the overview–region–local hierarchy, identity consistency and explicit physical scales. Our points are synthetic localizations, not microscopy pixels, reconstructed neurons or evidence of super-resolution.

## Reproduce

```bash
uv run --with matplotlib --with scipy python skills/scientific-figure-making/examples/nature_geometry_gallery.py --demo --out /tmp/nature-geometry
```

Optional --colors accepts a paper-colors Python export. The default exports the
same test palette as the other galleries. Outputs: three SVG/PNG compositions and
`data-and-summaries.json` with synthetic observations and geometry. CLI requires
explicit --demo. For measured data, adapt functions with real coordinate systems,
units, case IDs, transformations and spatial sampling definitions.

## Ternary composition changes

Seed 821; three predefined cohorts of 35 independent synthetic units. Initial
compositions come from three Dirichlet distributions. Final values multiply each
component by positive lognormal factors (log means log(.8,1.35,1), SD .08), then
explicitly divide by each row's sum. All three components are nonnegative and sum
to one; the mapping primitive rejects unclosed values rather than normalizing
silently. Vertices are A=(0,0), B=(1,0), C=(.5,sqrt(3)/2), with coordinates
x=B+C/2, y=sqrt(3)C/2. Grid lines are at 20 percentage-point increments.

All 105 final observations appear; diamonds are arithmetic cohort means of
compositions, not confidence regions or compositional geometric centres. Twelve
arrows connect the first four initial/final units from each cohort (selection by
ID, not effect size). White circles mark their initial values. The right scatter
uses paired initial/final log2(B/A), with an identity reference, while the lower
ECDFs show changes in A/B/C using different component colors. The cohort legend
applies to the main plot and ratio scatter; the component legend applies only to
change ECDFs. Fraction changes sum to zero per unit. These are descriptive, not
independent component tests. Real zeros require a stated log-ratio policy; never
add an undocumented pseudocount or interpret closure-induced anticorrelation as
causality. All raw initial/final fractions and displayed arrow IDs are saved.

## Steady field and pathlines

The field is defined analytically, not estimated from data:

`u(x,y) = .12 + .08*pi*sin(pi*x)*cos(pi*y)`
`v(x,y) = -.08*pi*cos(pi*x)*sin(pi*y)`

Coordinates are synthetic mm on x∈[0,2], y∈[0,1]; velocity units mm/s, time seconds.
The divergence du/dx+dv/dy is identically zero; normal velocity at y=0 and y=1 is
zero. Inlet/outlet exchange occurs at x=0/2. A 121×71 regular grid defines the speed
map and streamlines; color scale is fixed 0–.4 mm/s. The rasterized color surface
sits inside an otherwise editable SVG; it is not a wholly vector surface export.
Streamline arrows encode direction and constant line width does not encode speed.
A separate sparse quiver shows actual component magnitudes with a .2 mm/s key.

Five paths integrate dx/dt=u, dy/dt=v from (.05,y0), with y0=.12,.30,.50,.70,.88,
using solve_ivp, relative tolerance 1e-8, absolute tolerance 1e-10, max step .04 s.
Stop at x=2 or 18 s. Saved records include irregular integration times, positions
and whether the outlet was reached. Speed traces are evaluated on exactly these
paths, not independent illustrative curves. Section profiles use x=.3,1,1.7 mm.
Seed/path colors are consistent between pathline and speed-time panels; section
colors identify x positions in the separate section legend. Streamlines are
instantaneous tangent curves; pathlines are integrated particle histories. They
coincide geometrically here because this field is steady. In unsteady fields this
identity does not hold. No measured flow, CFD boundary-condition solution, force
inference or RNA-velocity analysis is implied.

## Nested spatial observations

Seed 822; 120 random cluster centres in a 200×200 μm synthetic field, with 35
localizations per cluster. Gaussian positional SD is 1.5 μm; coordinates are clipped
to the field. Categories are assigned per cluster, not inferred biological classes.
Full view contains 4,200 original observations. Region bounds are [65,135] μm on
both axes. The local centre is the recorded cluster centre nearest (100,100) μm;
its ±8 μm window lies within that region in this demo. Each view crops identical
observation IDs without rescaling coordinates, independently regenerating points
or changing colors. Scale bars span exactly 50, 20 and 5 coordinate μm respectively;
zoom panel sizes on the page can differ.

The local ECDF reports Euclidean distance from that selected centre, computed only
for local-window observations and split by category if present. It is not a radial
density or an edge-corrected spatial point-process statistic. One or more categories
may be absent from the local window. Legends distinguish the three shared category
colors; counts for field/region/local derive from saved masks. Localizations within
a cluster are not independent biological replicates. No biological significance,
resolution estimate or molecular interaction is inferred. Raw coordinates, cluster
IDs, category assignments, crop bounds, local centre and nested observation IDs
are preserved in JSON.

## Verification

Six tests cover ternary vertices/centroid, rejection of unclosed or negative
compositions, finite-difference divergence cancellation, wall-normal velocity,
nested ID preservation including boundary points, and invalid crop bounds.
Additional output checks verify fraction closure, nested local/region IDs and
positive integration times. These validate geometry; they are not a validation of
a scientific study's assumptions or sampling design.
