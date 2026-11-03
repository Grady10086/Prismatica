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

**Factorial ablation** · Seed distributions, component effects and interactions.

[![Dense factorial ablation study](docs/gallery/editorial-ablation.png)](docs/gallery.md#dense-cs-compositions)

**Model diagnostics** · Prediction density, layer probes, difficulty slices and failure cases.

[![Six-panel model diagnostic study](docs/gallery/editorial-analysis.png)](docs/gallery.md#dense-cs-compositions)

**Performance audit** · Operating points, paired effects, task profiles and consistency.

[![Dense performance and cost audit](docs/gallery/editorial-performance.png)](docs/gallery.md#dense-cs-compositions)

[Explore the full gallery and editable figures →](docs/gallery.md)

<sub>Original compositions using synthetic demonstration data. Statistical definitions and reproduction commands accompany every study.</sub>

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
