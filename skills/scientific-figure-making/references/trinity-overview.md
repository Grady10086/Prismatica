# Trinity Fig. 1: integrated method overview

Source: [The Trinity: Capability-Driven Recursive Self-Improvement for Multimodal Agents](https://arxiv.org/pdf/2610.36077), arXiv:2610.36077v1, Fig. 1 on PDF p1. The figure is a single native 4600×2181 raster asset in the inspected PDF. Use it as a **method overview** reference, separate from the compact manuscript data-plot route. The original artwork is not bundled with the skill.

## Actual composition

The image has a roughly 2.1:1 aspect ratio. Its top banner combines a subdued visual mosaic, short title and subtitle. The main middle band has three conceptual regions:

- **Left, task/world space:** nested tiers for open-world diversity, long-horizon interactions, perception and reasoning. Real scene thumbnails explain the scope. A narrow Creator library/tree strip links this region to the central mechanism.
- **Center, role interaction:** Creator, Explorer and Evolver arranged as a triangle. Directed, labeled arrows describe world creation/exploration, execution traces, verified feedback and adaptation. This is an explicit closed loop rather than a generic left-to-right pipeline.
- **Right, agent/Harness space:** nested tiers for prompt/context engineering, tools/memory/planning/verification/loop, and a capability-conditioned Harness family. A narrow Explorer inheritance tree connects this region to the center. Numbered tiers mirror the left region.

The bottom band is not another copy of that pipeline. Its left ~60% is a 3-column × 2-row detail grid: task tree / capability tree / Harness tree, then world exploration / world creation / capability-aware router. Its right ~40% is one evidence panel containing aggregate iteration results and separate Train/Unseen grouped radial bars. This division makes it possible to read scope → mechanism → implementation → evidence in the same overview.

## Transferable authoring choices

1. Choose a central organizing relationship, then place the input/world and model/system views on its two sides. Use a triangular feedback loop only when the actual method has three interacting roles; do not invent roles or arrows to imitate this paper.
2. Give the two sides parallel hierarchies and a consistent reading direction. Keep stage names, tree nodes, module colors and arrow semantics identical across the overview and detailed method figure.
3. Use an evidence inset to summarize measured outcomes; repeat exact numbers from the corresponding data figure/table. Its purpose is orientation, not replacing readable experimental plots. State split denominators and preserve distinctions between 18-benchmark and 16-non-robot Unseen summaries.
4. Use local mechanisms in the bottom detail grid, with short verb labels. Do not force six panels on a method with fewer mechanisms. Prefer whitespace to extra decorative icons.
5. Use real task images only where they convey task type; distinguish scene observations, simulation views and generated examples. Icons are explanatory marks, not evidence. The source’s mascot/branding is specific to its authors and is not a required template element.
6. Inspect at actual paper width. This original is dense; copying all tiny labels into a narrow column will not preserve readability. Use a double-width overview and move fine detail to the detailed method figure when necessary. Keep text/vector diagrams editable when authoring a new figure rather than flattening the entire result.

## Inspect the original

The existing reference renderer now also exports an **unaltered native-resolution original**, not a generated imitation:

```sh
uv run --with matplotlib --with pymupdf python skills/scientific-figure-making/examples/trinity_data_reference.py \
  --paper /absolute/2610.36077.pdf --out /tmp/trinity-data
```

`trinity-overview-original.png` is extracted from Fig. 1’s PDF image object after checking its dimensions. `source-data.json` records its page, xref, bounding box and the PDF hash. Other outputs are separately labeled numerical redraws of Fig. 7 / Table 4. Do not represent the original overview as our artwork or as a reusable MIT asset; preserve source attribution and check applicable reuse terms if redistributing it. For a user’s method, rebuild the composition from that method’s own roles, steps and evidence.
