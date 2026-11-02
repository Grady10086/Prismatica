# Research figure composition: an evidence-based casebook

Reviewed 2026-10-26. These observations concern specific collaborative works,
not official lab style guides or an individual's fixed drawing style. Preserve
scientific meaning and the project's palette when adapting a composition.

## Inspected sources and attribution

| Reference | Primary source and visual location | Scope |
|---|---|---|
| AMI-related predecessor | [I-JEPA](https://arxiv.org/abs/2301.08243), Fig. 3, PDF p. 3 | 2023 Meta AI/academic work by Assran et al., including LeCun and Rabbat; predates AMI. |
| World Labs | [Atlas](https://www.worldlabs.ai/blog/atlas#model-architecture), rendered Model Architecture diagram | Team technical blog, not a lab-wide style specification. |
| Yiming Li | [Tsinghua profile](https://collegeai.tsinghua.edu.cn/en/People/Full_time_PI/Yiming_Li.htm), [author homepage](https://yimingli-page.github.io/); [VoxFormer](https://openaccess.thecvf.com/content/CVPR2023/papers/Li_VoxFormer_Sparse_Voxel_Transformer_for_Camera-Based_3D_Semantic_Scene_Completion_CVPR_2023_paper.pdf), Figs. 1–2, PDF pp. 1, 4 | Spatial intelligence researcher Li Yiming, not the namesake at liyiming.tech. Paper predates his Tsinghua appointment. |
| Shuicheng Yan | [Author homepage](https://yanshuicheng.info/); Yu et al., [MetaFormer](https://arxiv.org/abs/2111.11418), Fig. 1, PDF p. 1 (arXiv v3) | A coauthored example, not individually attributed artwork. |
| Saining Xie / DiT | [Official project page](https://www.wpeebles.com/DiT.html), "Block designs for DiT" and "The effects of scaling DiT on FID" images | Peebles and Xie, 2023. Xie's [current homepage](https://www.sainingxie.com/) establishes the AMI connection; it does not make DiT an AMI publication. |
| Yiming Li / spatial search | [Thinking in 360°](https://humanoid-vstar.github.io/), Introduction's "Spatial supersensing teaser" (`figs/teaserv4.png`) | Collaborative work including Li and Xie; no individual drawing authorship asserted. |

The first, third and fourth papers were rendered and visually reviewed. Atlas,
DiT's two images and the spatial-search teaser were visually inspected in a
browser. Keep the original sources linked rather than copying them into the
skill. The [AMI website](https://amilabs.xyz/) reviewed did not expose a direct
publication figure collection; direct AMI coverage remains limited. Source
observations below are separated from our design adaptations.

## 1. I-JEPA: corresponding prediction branches

**Observed:** vertically separated context and target pathways; repeated patch
grids and matching target marks; dashed routed connectors to the representation
comparison rather than reconstructed pixels.

**Adaptation:** keep the same object mark across pathways and label each branch.
State where the loss acts. Give data flow, parameter updates and loss connections
separate labels or line conventions. Stop-gradient and EMA annotations belong
only where the actual method specifies them. Do not label an arbitrary two-branch
model JEPA or assume its weights are shared.

**Useful for:** distillation, prediction/target encoders, representation learning.

## 2. Atlas: conditions aligned with controlled outputs

**Observed:** brackets separate spatial context from output frames; camera glyphs
sit below corresponding visual elements with upward connections.

**Adaptation:** put the conditioning variable next to the exact output it controls.
Keep reference observations and generated content explicit. Turn interactive
sequences into selected labelled views for print; show times/camera positions and
hold crop, scale and camera fixed in method comparisons. A contact sheet is our
print adaptation, not the blog's exact layout. One attractive frame cannot prove
temporal or geometric consistency.

**Useful for:** novel views, scene generation, world-model rollouts.

## 3. VoxFormer: overview and implementation at different scales

**Observed:** Fig. 1 pairs a compact image-to-voxel concept with performance
comparison. Fig. 2 expands image features, depth-based proposals, cross-attention
and dense self-attention; a stage boundary and repeated query/voxel glyphs connect
these representations.

**Adaptation:** let the teaser explain the change and its purpose, while the main
method figure explains the computation. Reuse representation symbols across both.
Reserve detailed tensor shapes for the expanded view; give geometry correct
coordinate/camera cues. Voxels should stand for voxels, not decorate arbitrary
latent vectors. Keep semantic-class colors consistent across ground truth and
predictions, separately from method-role colors.

**Useful for:** 2D-to-3D perception and staged reconstruction.

## 4. MetaFormer: controlled architecture change beside evidence

**Observed:** aligned architecture columns retain the scaffold while changing
the token mixer. The adjacent accuracy-versus-MACs plot uses bubble size for
model size and direct model-family labels.

**Adaptation:** hold unchanged structure visually constant and highlight the
changed operation. Pair an efficiency claim with relevant evidence. Specify
latency, MACs, GPU hours or memory; these costs are not interchangeable. If size
is encoded, marker area should be proportional to the quantity, with a size key.
Comparable points need compatible data, hardware and evaluation protocols. Do
not infer significance from small visual gaps or draw a frontier across
incompatible experiments.

**Useful for:** architecture ablations and accuracy–cost claims.

## 5. DiT: overview, expanded detail and subdued alternatives

**Observed:** a compact architecture links to an expanded block with dashed zoom
lines. Alternative blocks are faded. The scaling figure repeats aligned axes and
stable model-color identities while changing the variable in the foreground.

**Adaptation:** expand one mechanism in a purposeful inset rather than drawing
every operation at the same scale. Maintain consistent faceting to isolate the
experimental variable. Fade context sparingly; preserve legibility and never
hide a competing result. Do not copy DiT's exact colors or default to its block
arrangement for unrelated models.

**Useful for:** conditioning mechanisms and controlled scaling experiments.

## 6. Thinking in 360°: concrete environment and local task detail

**Observed:** the left side explains agent orientation and field of view; repeated
task examples on the right connect a panorama, marked target region and desired
final view.

**Adaptation:** make an actual environment or result the primary visual, then pair
a marked region with its correct detailed view. Use fewer, larger examples for
a small figure. Keep the sensing setup explicit instead of replacing it with a
generic robot icon. Do not distort camera/region correspondence for layout.

**Useful for:** embodied tasks, spatial search and scene-driven project teasers.

## Choose by question

| Question | Composition | Verification |
|---|---|---|
| What changes in the method? | Aligned scaffold + emphasized operation + matched ablation | No confounded comparison |
| What conditions a prediction? | Branch correspondence or condition/output strip | Arrow types and targets explicit |
| Better at comparable cost? | Directly labelled accuracy–cost plot | Comparable protocol, cost units and axis directions |
| Consistent geometry/identity? | Fixed-view contact sheet and matched crops | Same normalization; representative and failure cases |
| How does 2D become 3D? | Compact overview plus expanded stage diagram | Representation and coordinate conventions agree |

For project teasers read [teaser design](teaser-design.md): it provides three
original scene-first SVG studies and a visual review checklist. The earlier
`research_composition.py` box example is a control-comparison teaching aid, not
a visual-quality target. Use project-native TikZ/SVG/draw.io tools for diagrams
and [paper-colors roles](../../paper-colors/references/diagrams.md) for their colors.
This casebook adds composition guidance, not a renderer for arbitrary model graphs.
All adaptations are this skill's recommendations, not requirements from the
cited authors. Do not carry over logos, illustrations, result values or screenshots
into a new figure merely because the source is publicly readable.
