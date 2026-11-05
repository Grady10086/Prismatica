# Three generative art studies: state, light and discrete geometry

Use for original website art, method overviews and image-led teasers needing a
more deliberate generative visual language. Researched 2026-11-05 against the
original project pages and visual documentation. Separate the source's claims,
our observations and the implementation choices below. This is an optional
composition reference; keep the project's registered palette and scientific
plotting workflow.

## Gamma: behavior gives form a reason

Source: FIELD.IO for Applied Intuition,
[Seeing in Gamma](https://field.io/work/applied-intuition-seeing-in-gamma), 2026.
The studio describes a generative visual system for machine perception and
coordinated decision-making. Its stated spectrum roles include magenta for
infrared, amber for thermal and cyan for LiDAR; density, direction and intensity
respond to environmental encounters.

In the documented excavator image, a largely neutral terrain and machine support
a broad colored field, while fine white lines and compact labels locate specific
observations. The field belongs to the scene rather than floating as a separate
rainbow decoration. The color field is dominant; annotations remain sparse.

Transfer: establish a stable mapping from state to visual response. For an
interactive method diagram, modality identity can control hue, selection can
control emphasis and actual orientation can control direction. Do not change
category colors opportunistically during transitions. Keep an explanation of
any numerical mapping and do not infer calibrated measurement accuracy from
the studio's communication imagery.

Prismatica interpretation: the Aura hero uses three fixed Iris color lanes on
one analytic surface. Pointer and scroll change the view, not color identities.
It is decorative geometry, not sensor output. Actual chart palettes and values
remain unchanged.

## SKALAR: compose light as grouped spatial structure

Source: Christopher Bauder and Kangding Ray,
[SKALAR, DARK MATTER Berlin](https://www.kinetic-lights.com/project/skalar/dark-matter-berlin),
2025 presentation. The original work predates this presentation. The documented
installation combines motorized mirrors, choreographed light and synchronized
sound; the official page lists 65 mirror discs.

The official hero documentation shows amber beams forming a shared spatial
focus within a dark industrial hall. Repeated suspended discs provide tangible
anchors; distinct beams and dark intervals make a large ensemble readable.
The useful lesson is coherent choreography, not adding bloom to every edge.

Transfer: animate related elements from a shared phase or state; use few crisp
cores, restrained wider light and visible gaps. On an interface, connect motion
to selection, focus or progression. Keep navigation stationary and legible.
Do not reproduce strobes or require sound to understand a scientific interface.

Prismatica interpretation: Light draws a bounded set of small facets and
synchronized line segments on the same Möbius geometry. It is an original
screen-space study, not an optical or robotic simulation. Iris colors and warm
ivory cores replace the source installation's palette.

## Pointillisme: let local samples preserve a global form

Source: Quayola,
[Pointillisme: Provence](https://quayola.com/pointillisme-provence/), 2023.
The artist describes videos and prints of Provençal foliage made through
high-precision laser scanning, including failures to resolve complex geometry
and color and associated chromatic aberrations. The page credits point-cloud
visualization and procedural animation.

The documentation juxtaposes bright, locally varied point structures against
dark gaps. Branch and foliage masses remain apparent through their spatial
distribution. Color variation and density organize the image without requiring
a continuous opaque skin. This is not arbitrary uniformly scattered noise.

Transfer: sample an actual form, keep the sampling stable between frames and
preserve depth ordering. Vary density only with a declared purpose. For real
3D results, preserve original coordinates and color values; label decimation,
color normalization and missing regions. Scanning error can be an artistic
subject, but a research visualization must not invent errors or hide failures
for a picturesque effect.

Prismatica interpretation: Points uses fixed deterministic samples of the
analytic Möbius surface, sorted by depth with bounded point sizes and Iris
color interpolation. It is not a scanned landscape or a result from a trained
model. Reduced mobile sample count affects only this decorative surface.

## Combine without losing the research

Use one shared form with alternate representations: state-linked color,
choreographed structure and discrete samples. A common geometry makes the
change of representation understandable and lets a viewer compare appearances.
Do not mix three unrelated spectacles into one data panel.

For data experiments, the transferable principles are stable semantic roles,
grouped emphasis and honest sampling. Keep uncertainty and measurements exact.
For teasers, a neutral evidence area can contrast with an original generative
illustration, with the distinction visible and stated when needed.

## Implementation review

- Every mode has a complete, readable still state and a keyboard button with
  selected state; no interaction depends solely on pointer motion.
- The pause control and reduced-motion preference stop decorative motion.
  Mode selection can redraw a paused still without restarting animation.
- Stop painting outside the visible hero; bound sample count and pixel ratio.
- Keep text, navigation and actual chart canvases free of particles or light.
- Preserve the half-twist seam and original geometry across representations.
- Link original projects as references; do not bundle their photos, videos,
  logos, soundtracks or source artwork as Prismatica-owned assets.

## Chart collection and laboratory interpretation

The website applies these principles to evidence as well as hero art:

- Shared panel headings use a small palette-linked accent and a fine neutral
  divider. Their treatment is in the SVG source, so canonical SVG/PNG exports
  keep it. Neutral paper and readable axes remain independent of the theme.
- Tide (blue, rose, ochre, sage) and Ember (bronze, slate, muted red, olive) are
  original optional browser palettes. They are not sampled from the works or
  identified as Pantone colors. Iris remains the default; fixed category order
  and numerical color domains are retained when changing palettes.
- The collection alternates larger primary previews with smaller supporting
  cards. Individual plots preserve the full vector viewBox rather than cropping
  evidence to fill a card.
- Hover adds a thin frame to the current panel. Selecting an observation adds
  local emphasis to its existing linked marks and keeps other observations
  visible. The evidence rail exposes the selected mark's actual tooltip values;
  previous/next buttons support keyboard inspection in SVG traversal order,
  which is not a ranking by value.
- Overlays and selection styles are transient interface state. Canonical exports
  contain the full data and omit hover frames and dimming. No cinematic light,
  artificial point jitter or decorative particles are added to measured marks.
