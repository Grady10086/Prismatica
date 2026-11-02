# Scene-first project teasers

Use this reference when the user wants a visually expressive project teaser or
rejects a generic box-and-arrow example. Keep [source cases](research-patterns.md)
separate from this skill's own design recommendations. These layouts are starting
compositions, not author-specific presets or a Nature submission profile.

## What failed in the early example

The original architecture/evidence example was a schematic teaching aid: large
repeated rectangles, equal emphasis on unchanged operations, generic module
names and legends competing with the plot. It did not provide a meaningful scene
or the visual specificity expected of a project teaser. Retain it only as a small
control-comparison example, not as the visual-quality target for new work.

## Start from the claim and actual visual evidence

Write a short figure brief: the input, the technical change, the observable
output, and the evidence. Then choose the largest visual object. For spatial AI
this is often a scene, map, camera-conditioned output, or reconstructed geometry.
For other tasks it may be the generated result or a concrete input/output pair.
Avoid inventing an urban scene simply because the paper mentions a world model.

The supplied gallery is explicitly synthetic geometry for exercising composition.
For an actual paper, replace it with project-owned scene renders, real results and
correct method labels. Do not present geometry samples as reconstruction results,
random dots as learned attention, or invented curves as measurements.

## Build hierarchy without decoration

- Make the actual scene/output visually dominant. Draw technical operations
  smaller, close to the representation they transform. Introduce a full box only
  when it encloses a meaningful module or subsystem.
- Use one primary reading direction. Align cameras with their views, crop boxes
  with their magnified details, and tokens with the operation that consumes them.
  Use labelled branches for an actual conditional or training-only path.
- Treat typography as a small hierarchy: panel/section label, short object label,
  optional secondary note. Keep prose explanations in the caption. Avoid making
  a diagram look like an app dashboard or a stack of presentation cards.
- Choose one accent for the contribution and a secondary accent only when it
  carries a different meaning. Neutral structures should still have enough
  contrast to survive print. Keep dataset class colors distinct from method colors.
- Use scale changes deliberately: a large environment, a smaller detail crop, then
  compact quantitative evidence. Do not shrink the environment until its detail
  is indistinguishable, or enlarge a decoder label until it competes with results.
- Use camera frusta, sparse points and voxel grids only when they are meaningful
  to the method. Label whether they represent measured geometry, a feature-space
  abstraction or a purely illustrative diagram. Avoid decorative glows, shadows
  and extrusions without scientific meaning.

## Three composition recipes

| Recipe | Dominant visual | Supporting elements | Best suited to |
|---|---|---|---|
| Scene overview | Large spatial scene/representation | Posed inputs on left; matched query views on right | Reconstruction, spatial memory, novel-view generation |
| Local mechanism | Scene with a query region | Retrieved features and a small decoder/output strip | Local retrieval, sparse computation, region-conditioned prediction |
| Scene plus evidence | Scene or real result on left | One directly labelled accuracy–cost plot on right | A visual capability tied to an efficiency claim |

These are implemented by `examples/teaser_gallery.py`. Their geometry is an
original axonometric scene rendered at several rotations, not copied paper art.
The script can consume a `paper-colors.json` export via `--tokens`; without one,
it reads two invented values from the repository's synthetic test fixture. All
additional chromatic fills are tints of those anchors; structural grays are neutral.

```bash
# Standard-library SVG generation; editable text and geometric paths.
python3 skills/scientific-figure-making/examples/teaser_gallery.py --out /tmp/beautify-teasers
# Optional PNG previews; no system Cairo installation required.
uv run --with resvg-py python skills/scientific-figure-making/examples/teaser_gallery.py --out /tmp/beautify-teasers --png
# Use a small exported paper palette, not a complete color book.
uv run --with resvg-py python skills/scientific-figure-making/examples/teaser_gallery.py --out /tmp/my-teasers --tokens /path/to/paper-colors.json --png
```

The SVG canvas is 183 mm wide. Treat these as project-page composition studies;
for manuscript delivery, recheck text at the actual insertion size, remove long
headlines and demo footers, and apply the target journal's specifications. The
SVG retains editable text; font substitution can change line lengths, so inspect
with the final production font. PNG is a preview, not the editable master.

## Visual acceptance pass

1. At thumbnail size, the task and contribution should be identifiable from the
   scene and relationships, rather than from reading every sentence.
2. At the final viewing size, check label length, foreground/background contrast,
   connectors crossing text, small point marks, cropped content and wasted gaps.
3. For comparisons, use the same views, crops, scales and normalization. Supply
   representative/failure examples where the claim requires them; aesthetic
   selection must not replace a sampling protocol.
4. Review the exported image. Revise the composition before making more variants
   if it still looks like anonymous boxes. Keep the final chosen direction and
   record why it supports the specific research claim.
