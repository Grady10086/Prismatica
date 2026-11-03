<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/homepage/masthead-dark.png">
    <img src="docs/homepage/masthead.png" alt="Prismatica — from research evidence to publication-ready figures" width="1200">
  </picture>
</p>
<p align="center"><a href="#start-creating">Get started</a> · <a href="docs/gallery.md">Gallery</a> · <a href="docs/usage.md">Guide</a> · <a href="docs/examples.md">Examples</a> · <a href="README.zh-CN.md">简体中文</a></p>

Prismatica is a **complete scientific figure toolkit for AI coding agents**. Bring your data, results or figure draft; use one workflow to choose the visual form, coordinate colors, compose panels, refine the final layout and export editable figures.

**Experiment plots · model analysis · statistical composites · method diagrams · research teasers**

## Selected work

[![Full-factorial ablation with seed distributions, component effects and interaction analysis](docs/homepage/experiments.png)](docs/gallery.md#cs-factorial-ablation)

[![Model behavior analysis and performance-cost comparison compositions](docs/homepage/diagnostics.png)](docs/gallery.md#cs-model-analysis)

[Model analysis ↗](docs/gallery.md#cs-model-analysis) · [Performance audit ↗](docs/gallery.md#cs-performance-audit)

[![Multi-track task profiles and matched evaluation flows](docs/homepage/compositions.png)](docs/gallery.md#multi-track-task-fingerprint)

[Multi-track profiles ↗](docs/gallery.md#multi-track-task-fingerprint) · [Evaluation flows ↗](docs/gallery.md#matched-evaluation-flows) · **[Full gallery ↗](docs/gallery.md)**

<sub>Original compositions with synthetic demonstration data. Full-size figures, statistical definitions, editable SVGs and reproduction commands are in the gallery.</sub>

## One workflow, from input to figure

| Plan | Compose | Refine | Deliver |
| --- | --- | --- | --- |
| Choose charts around the research question and available evidence. | Combine data, images and diagrams with consistent visual roles. | Tune palette, hierarchy, spacing and typography at the target paper size. | Export PDF, SVG and PNG with reproducible source code. |

The suite combines [figure making](skills/scientific-figure-making/SKILL.md) and [paper colors](skills/paper-colors/SKILL.md) behind one entrypoint: **[$prismatica](skills/prismatica/SKILL.md)**. Pairing, uncertainty and data provenance remain part of the drawing workflow.

## Start creating

```sh
git clone https://github.com/Grady10086/Prismatica.git
cd Prismatica
python3 scripts/install_skills.py
```

Installs all three skills into `~/.codex/skills/`. Existing folders are preserved; use `--replace` to update with backups. Open a new agent session if needed, then ask:

> Use $prismatica to turn my experiment CSV into a 180 mm multi-panel figure. Show model comparisons and ablations, use a consistent palette, preserve matched seeds, and export PDF, SVG and PNG. Check the layout at its final size.

**[Usage & inputs](docs/usage.md)** · [All examples & reproduction](docs/examples.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
