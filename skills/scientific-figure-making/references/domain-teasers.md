# Teasers for multimodal, generative and robotics research

This gallery complements the spatial examples with different visual subjects:
image/question pairs, generated objects, controlled output matrices and a robot
manipulation sequence. Use the same typography and palette infrastructure, but
choose a composition that exposes the research task. Do not force every task
into an environment or voxel diagram.

## Primary references and how they were used

Checked 2026-10-26. These are collaborative research works; none is a personal
or lab-wide illustration style specification.

| Source | Inspected material | Adaptation for this gallery |
|---|---|---|
| [Cambrian-1](https://cambrian-mllm.github.io/cambrian-1/), Tong et al., NeurIPS 2024 | Fig. 6, Spatial Vision Aggregator; original project-page image visually inspected | Keep visual features and text tokens distinguishable; show where the modalities connect. The supplied example is a generic visual-QA composition, not an implementation of SVA. |
| [DiT](https://www.wpeebles.com/DiT.html), Peebles and Xie, ICCV 2023 | Block-design and scaling figures visually inspected in the previous reference pass; project text describes matched sampling noise | Separate conditioning from generation; use matched views or noise when a comparison requires it. The drawn denoising strip is an original explanatory illustration, not a DiT model trace. |
| [π₀](https://www.pi.website/blog/pi0), Black et al. | Official [paper](https://www.physicalintelligence.company/download/pi0.pdf), Figs. 1–2, PDF pp. 1–2, rendered and visually inspected | Combine a concrete task scene, language goal, policy interface and short ordered task sequence. The gallery's drawn robot is generic, not a replica of one of the paper's embodiments. |
| [Diffusion Policy](https://diffusion-policy.cs.columbia.edu/), Chi et al. | Official project description of conditional action diffusion and receding-horizon control, read as a conceptual reference | Show predicted action chunks separately from executed prefixes and observation feedback. This is a conceptual reference, not a claim to have visually reproduced its method figure. |

Only links and original explanatory drawings enter the repository. Keep the
paper artwork separate from reusable template assets. Our adaptations are design
recommendations, not requirements imposed by the source authors.

## Four template families

### 1. Multimodal grounding

Input image and a short question sit together; visual and text feature strips
meet at a compact cross-modal interface; output pairs the response with its
supporting region. Use this for VQA, visual grounding, image-conditioned dialogue,
or a visual reasoning teaser.

The placeholder question is consistent with the placeholder drawing. Replace
both when inserting actual project assets. A drawn region is an illustrative
annotation, not a learned saliency map. Distinguish multiple vision encoders from
multiple input modalities: image and text are two modalities; several image
encoders do not automatically add video/audio capabilities.

### 2. Conditional generation

Keep the condition visible on the left, show a short process strip in the middle,
and allocate the right side to generated outputs. Label denoising direction
explicitly. Replace process drawings with genuine intermediate states if the
figure claims a particular model's actual inference trajectory. Noise dots are
only a schematic texture here.

Use for text-to-image or image-conditioned generation. Label prompts, seeds,
checkpoints and sampling settings in the actual caption. Keep a controlled
comparison's shared variables fixed; use diverse samples to demonstrate variety,
not to support an unmeasured quality advantage.

### 3. Controlled-generation matrix

Use a larger result grid instead of a model diagram. Rows and columns correspond
to two explicit controls. Keep object geometry, camera, framing and any other
non-varied factors consistent. The default illustration crosses two finishes
with three patterns, a factorial demonstration rather than a quantitative result.

For real evaluations, do not claim that only one factor changed if several
settings, prompts, seeds or source images also changed. Publish enough metadata
to tell which controls are fixed. Include failures where required by the claim.

### 4. Robot perception/action loop

Pair the observation with the language goal, draw a small policy interface,
then show action chunks and a task sequence. Route the new observation back to
the input separately from the forward action path. Label predicted actions,
executed actions, state and feedback distinctly.

Use actual time stamps if supplied; the synthetic default uses stage numbers,
not fabricated timings. Do not imply a drawn sequence was physically executed,
a controller was validated, or a robot was successful. Keep consistent camera,
object identity, gripper position and object state across actual task frames.
The figure generator does not connect to or control hardware.

## Generate and replace with project assets

```bash
# Standard library only, with the sibling teaser_gallery.py in the same folder.
python3 skills/scientific-figure-making/examples/domain_teasers.py --out /tmp/domain-teasers
# Also generate preview PNGs.
uv run --with resvg-py python skills/scientific-figure-making/examples/domain_teasers.py --out /tmp/domain-teasers --png
# Existing palette and local project results.
uv run --with resvg-py python skills/scientific-figure-making/examples/domain_teasers.py --out /tmp/project-teasers --tokens /path/to/paper-colors.json --assets /path/to/assets.json --png
```

SVG generation uses the standard library; `resvg-py` is optional for PNG rendering.
Default colors are two invented test-fixture values, not color-book data. The
`--tokens` schema matches `paper-colors export` JSON. The files retain editable
text and vector shapes. Canvas width is 183 mm; review the actual inclusion size
and target venue's typography rules before submission.

Asset manifest example (paths resolve relative to the manifest, or use absolute paths):

```json
{
  "multimodal_input": "results/input.png",
  "multimodal_output": "results/grounded-answer.png",
  "generated_1": "results/sample-1.png",
  "robot_observation": "results/observation.png",
  "robot_step_1": "results/approach.png",
  "robot_step_2": "results/lift.png",
  "robot_step_3": "results/place.png"
}
```

Available slots:

| Slots | Meaning |
|---|---|
| `multimodal_input`, `multimodal_output` | Matching input and annotated/evidence output |
| `generated_1` through `generated_4` | Conditional generation samples, row-major |
| `control_1_1` through `control_2_3` | Two rows × three columns of controlled outputs |
| `robot_observation` | Initial visual observation |
| `robot_step_1` through `robot_step_3` | Ordered task frames |

PNG, JPEG and WebP files are embedded in the SVG as data URIs; no external image
links or network fetches remain. They are aspect-fit without cropping. Missing
slots keep the synthetic drawing, so inspect the provenance manifest and replace
all corresponding slots before calling a panel real evidence. When replacing an
output image, the generator does not add the synthetic bounding-box annotation.
Edit prompts, answers, stages and control labels in the generated SVG to match
the actual project. Image replacement does not infer new captions automatically.
Raster images remain raster; editable text does not turn them into vector data.

## Visual review

Inspect SVG and PNG for long labels, tiny result tiles, ambiguous arrows and
misaligned samples. Keep reference inputs visibly distinct from predictions.
For videos/robot tasks, preserve order and describe frame selection. For image
comparisons, keep crop, camera, scale and display normalization matched. A gallery
of attractive examples is not evidence of generalization on its own.
