<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/horizontal-dark.svg">
    <img src="docs/brand/horizontal.svg" alt="Prismatica" width="500">
  </picture>
</p>

<p align="center">A visual toolkit for research · 面向科研的可视化工具箱</p>

Prismatica 将绘图、配色、论文排版、模型分析和结果展示组合为一套 skill 工作流。
支持紧凑的论文数据图，也支持方法主图与 image-led teaser；不以美化为由改变实验结果。

## One entrypoint, all drawing skills

| Skill | Role |
| --- | --- |
| [`prismatica`](skills/prismatica/SKILL.md) | 统一入口，协调配色、选图、排版、导出和检查 |
| [`scientific-figure-making`](skills/scientific-figure-making/SKILL.md) | 科研数据图、复杂组合图、实验分析、方法主图、teaser |
| [`paper-colors`](skills/paper-colors/SKILL.md) | 色库匹配、主题、顺序色阶、跨媒介导出与颜色检查 |

保留全部原有示例、统计工具、测试和论文参考；两个底层 skill 也可以独立调用。
完整图表路线见 [gallery catalog](skills/scientific-figure-making/references/gallery-catalog.md)。

## Install the complete suite

```sh
git clone https://github.com/Grady10086/Prismatica.git
cd Prismatica
python3 scripts/install_skills.py
```

默认安装三个目录到 `~/.codex/skills/`。已存在的目录不会被覆盖；安装器会在写入前列出冲突并退出。
用 `--dest /your/skills/directory` 可选择其他位置。仅更新已安装版本时显式使用 `--replace`；旧目录会保留为备份。
不要只复制统一入口：它需要两个 sibling modules。

Example:

> 使用 $prismatica，根据我的实验 CSV 选择合适的图和配色，做成 180 mm 双栏组合图。
> 保留逐种子数据与配对关系，说明置信区间，导出 PDF、SVG、PNG，并检查最终尺寸的可读性。

安装后若当前会话尚未显示新 skill，请在新会话中调用。

## Capabilities

- **论文数据图**：训练动态、消融与交互、跨模态检索／条件冲突、性能与成本比较。
- **复杂统计组合**：分布与估计、聚类热图、相关矩阵、网络、桑基、空间／多尺度、剂量响应、生存、火山／富集／森林、ROC／PR／校准与决策曲线。
- **方法主图与 teaser**：层级框架、闭环机制、真实图像／连续帧、视频生成、3D 和机器人结果展示。
- **配色与导出**：用户提供的色库、可复用主题与色阶、最终尺寸排版、PDF／SVG／PNG 和视觉检查。

## Preview

Original layouts rendered from **synthetic demonstration data**:

![Training dynamics](docs/images/training-dynamics.png)
![Factorial interactions](docs/images/factorial-interactions.png)

## Reproduce and test

Python 3.10+ and uv:

```sh
uv sync --all-extras --locked
uv run python skills/scientific-figure-making/examples/cs_paper_data_gallery.py --out /tmp/paper-data
uv run python skills/scientific-figure-making/examples/cs_paper_comparisons.py --out /tmp/paper-comparisons
uv run pytest -q
```

All fixture data remain labeled synthetic. Paper-reference tools require separately supplied local PDFs and keep author/source labels; they do not run model inference. Users must supply real measurements to generate reportable results.

## Brand

The selected **Iris** logo palette uses the user's local Solid Coated V5 library:
6091 C / 4082 C / 2438 C, with 432 C for the wordmark. The four exported sRGB colors
and vector artwork are in [docs/brand](docs/brand). They are brand colors, not a
universal categorical-data palette. Screen values are approximations; the source
color book is not distributed or covered by our MIT license.

## Sources and license

Developed while extending [ruixuan-ray-zhang/beautify](https://github.com/ruixuan-ray-zhang/beautify).
Upstream MIT authorship is preserved in [LICENSE](LICENSE) and [NOTICE](NOTICE.md).
Original paper PDFs, extracted paper illustrations, proprietary color books and personal files are not included.
Reference-image/data rights remain with their owners. Prismatica is not affiliated with or endorsed by Pantone LLC.
The earlier `scientific-figure-making` repository name redirects here after the rename.
