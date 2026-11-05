<p align="center">
  <a href="https://grady10086.github.io/Prismatica/"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/homepage/masthead-v2-dark.png">
    <img src="docs/homepage/masthead-v2.png" alt="Prismatica — 科研绘图与视觉表达工作室" width="1200">
  </picture></a>
</p>
<p align="center"><a href="https://grady10086.github.io/Prismatica/">在线交互工作室 ↗</a> · <a href="#开始绘图">开始使用</a> · <a href="docs/gallery.md">精选画廊</a> · <a href="docs/usage.md">使用指南</a> · <a href="docs/examples.md">全部示例</a> · <a href="README.md">English</a></p>

Prismatica 是面向 AI 编程助手的**完整科研绘图工具套件**。提供实验数据、结果素材或已有草图，即可通过统一工作流完成选图、配色、组合排版、最终尺寸检查与可编辑导出。

**实验数据图 · 模型分析 · 复杂统计组合 · 方法主图 · 科研 teaser**

**[进入在线交互工作室 →](https://grady10086.github.io/Prismatica/)** · 27 个实时案例，可修改数据、调整配色并导出矢量图。[使用说明](docs/interactive-studio.md)。

## 精选展示

**扩散采样与数值诊断** · 实际运行的采样检查点、粒子轨迹与等预算收敛。

[![扩散采样与数值收敛组合](docs/gallery/diffusion-numerics.png)](docs/multimodal-diffusion.md#diffusion-sampling-and-numerics)

**跨模态对齐与检索** · 相似度结构、双向检索和逐查询变化。

[![跨模态对齐与检索诊断](docs/gallery/multimodal-retrieval.png)](docs/multimodal-diffusion.md#cross-modal-alignment-and-retrieval)

**多模态证据冲突** · 配对回答流向、条件响应面与选择性风险。

[![多模态证据冲突分析](docs/gallery/multimodal-conflict.png)](docs/multimodal-diffusion.md#multimodal-evidence-conflict)

[消融与模型诊断 →](docs/gallery.md#dense-cs-compositions) · [完整画廊 →](docs/gallery.md) · [论文参考与统计定义 →](docs/multimodal-diffusion.md)

<sub>参考 Nature 系论文组织方式的原创布局。多模态部分为合成数组；扩散部分为实际计算的二维解析 score 实验，不代表预训练图像模型性能。提供可编辑图形与复现命令。</sub>

## 从输入到成图

| 选图 | 组合 | 精修 | 交付 |
| --- | --- | --- | --- |
| 根据研究问题与已有证据选择图形。 | 将数据、图像与方法结构组织成连贯面板。 | 在论文实际尺寸下调整配色、层级、留白与字体。 | 导出 PDF、SVG、PNG 与可复现代码。 |

通过 **[$prismatica](skills/prismatica/SKILL.md)** 统一调用[绘图与排版](skills/scientific-figure-making/SKILL.md)、[论文配色](skills/paper-colors/SKILL.md)。样本配对、不确定性定义与数据来源贯穿绘图过程。

## 开始绘图

```sh
git clone https://github.com/Grady10086/Prismatica.git
cd Prismatica
python3 scripts/install_skills.py
```

一次安装三个 skill，默认位置为 `~/.codex/skills/`。已有目录会保留；更新可使用 `--replace` 并自动备份。必要时开启新的助手会话，然后提出需求：

> 使用 $prismatica，把我的实验 CSV 做成 180 mm 多面板论文图，展示模型对比和消融实验。统一配色，保留逐种子配对，导出 PDF、SVG、PNG，并检查最终尺寸的排版。

**[使用方式与输入要求](docs/usage.md)** · [全部示例与复现](docs/examples.md) · [参与贡献](CONTRIBUTING.md) · [MIT](LICENSE)
