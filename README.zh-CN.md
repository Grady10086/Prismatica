<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/gallery/cover-dark.png"><img src="docs/gallery/cover.png" alt="Prismatica" width="1200"></picture></p>
<p align="center"><strong>面向科研的可视化工具箱</strong><br>选图、配色、排版、导出与检查，组合成一套工作流。</p>
<p align="center"><a href="README.md">English</a> · <a href="docs/gallery.md">精选画廊</a> · <a href="docs/examples.md">全部示例</a> · <a href="docs/usage.md">使用方式</a></p>

## 从数据到可读的研究图

[![CS 模型分析：配对预测、边缘分布、逐层探针与难度切片](docs/gallery/cs-model-analysis.png)](docs/gallery.md#cs-model-analysis)

<table><tr><td width="50%"><a href="docs/gallery.md#cs-factorial-ablation"><img src="docs/gallery/cs-factorial-ablation.png" alt="完整因子消融与交互分析"></a></td><td width="50%"><a href="docs/gallery.md#cs-performance-audit"><img src="docs/gallery/cs-performance-audit.png" alt="性能成本与逐任务对比"></a></td></tr><tr><td><strong>完整因子消融</strong>：配置、种子分布、主效应与交互。</td><td><strong>性能对比</strong>：预算曲线、配对增益与逐任务检查。</td></tr></table>

新增三组面向 CS 论文的实验组合图；[精选画廊](docs/gallery.md)现有九种布局，包含完整图、统计定义和可编辑 SVG。已有的环形图、表征分布与流向图继续保留。

Prismatica 是供 AI 编程助手使用的 skill 套件。它帮助确定图表类型、统计口径与配色，在最终尺寸下组织面板，并导出可编辑的 PDF／SVG 和 PNG 预览。

上图及精选画廊均使用**合成演示数据**，不代表任何真实模型的性能。原始数组、生成脚本、重采样方式与来源说明均可复现。

## 覆盖范围

- 训练动态、完整因子消融、模型比较、逐样本差异与不确定性。
- 跨模态检索、条件冲突、扩散重建质量、采样预算与成本。
- 聚类热图、相关矩阵、网络／桑基、空间／多尺度、分布／估计、剂量／生存、火山／富集／森林、ROC／PR／校准等组合图。
- 方法主图、任务闭环、真实输入／结果、连续帧与多模态／机器人 teaser。
- 用户提供的色库、语义配色与色阶、论文最终尺寸、矢量导出和视觉检查。

## 三个 skill，一起安装

`prismatica` 负责统一协调，`scientific-figure-making` 负责绘图与排版，`paper-colors` 负责配色。原有工具、示例和参考全部保留。

```sh
git clone https://github.com/Grady10086/Prismatica.git
cd Prismatica
python3 scripts/install_skills.py
```

默认安装到 `~/.codex/skills/`，已有目录不会自动覆盖。指定 `--replace` 才会在保留备份后更新；`--dest` 可选择其他目录。

使用示例：

> 使用 $prismatica，根据我的 CSV 做一张 180 mm 双栏实验图。保留逐种子数据和配对关系，标明误差区间，统一方法颜色，导出 PDF、SVG、PNG，并检查最终尺寸的文字与图例。

安装后如果当前会话尚未发现 skill，可在新会话中调用。图表脚本运行环境与 skill 安装分开；复现图库需要 Python 3.10+ 和 uv：

```sh
uv sync --all-extras --locked
uv run python skills/scientific-figure-making/examples/showcase_gallery.py --out /tmp/prismatica-gallery
uv run python skills/scientific-figure-making/examples/cs_showcase.py --out /tmp/prismatica-cs
uv run pytest -q
```

## 使用边界

实验数据图、方法主图、teaser 按实际用途选择版式。演示脚本不是通用 CSV 导入器；请让助手读取真实数据并修改相应生成部分，不能把演示值当作实验结果。论文原图提取工具需要用户自行提供本地 PDF，并保留原作者归属。原始论文图片、专有色库及个人资料不随库分发。

更多说明见 [精选画廊](docs/gallery.md)、[使用方式](docs/usage.md)、[全部示例](docs/examples.md) 和 [贡献指南](CONTRIBUTING.md)。

项目由扩展 [beautify](https://github.com/ruixuan-ray-zhang/beautify) 的工作整理而来，保留上游 [MIT 许可证](LICENSE) 与 [来源说明](NOTICE.md)。
