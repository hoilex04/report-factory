---
name: report-factory
description: Universal Knowledge Card Factory — Transform articles/papers into standardized Obsidian cards. Supports custom domains, intelligent detection, and Canvas output.
user-invocable: true
triggers:
  - "制卡"
  - "收割"
  - "处理"
  - "分析"
  - "report"
  - "生成卡片"
version: 2.1-unified
---

# Report Factory: Universal Knowledge Card Generator

> 追踪信息，沉淀知识 —— 将零散的技术内容转化为可复用、可关联、可溯源的 Obsidian 知识卡片。

**Core Philosophy**: Evidence over opinions. Quantitative data over qualitative claims. **Your domains, your rules.**

---

## Quick Start / 快速开始

```bash
# 首次配置（必须）
/setup-domains

# 单篇处理
/process https://arxiv.org/abs/2602.xxxxx

# 批量收割
/harvest wechat    # WeChat RSS (last 7 days)
/harvest arxiv     # arXiv top 30 (current month)
/harvest inbox     # Inbox.md (green channel, no time filter)

# 深度分析 / 战略研究
/analyze "端侧 AI 部署趋势"
```

---

## Table of Contents

1. [双模式架构](#双模式架构)
2. [预配置领域包](#预配置领域包)
3. [模式 A：生产车间 — 制卡流水线](#模式-a生产车间--制卡流水线)
4. [模式 B：战略级研究中心 — 假说驱动型智能举证](#模式-b战略级研究中心--假说驱动型智能举证)
5. [卡片输出格式规范](#卡片输出格式规范)
6. [配置与路径](#配置与路径)
7. [行为约束与质量门禁](#行为约束与质量门禁)
8. [FAQ](#faq)

---

## 双模式架构

在处理指令前，先通过输入内容判断启动模式：

- **【生产模式】触发**：输入包含 URL、PDF、具体文章内容，或指令含"收割、处理 Inbox、处理 RSS"
- **【研究模式】触发**：输入包含"分析、选题、为什么、如何证明、寻找论据"等意图

---

## 预配置领域包

### Pack 1: AI Research (Default)

| Code | Domain | Keywords | Typical Metrics |
|------|--------|----------|-----------------|
| **EAI** | Embodied AI | Robot, Manipulator, Locomotion, Embodied AI, Grasp, Navigation, VLA, Control | latency, success_rate, training_time |
| **AIH** | AI Hardware | NPU, Chip, AI PC, Wearable, Edge Computing, Hardware, Sensor, ASIC, FPGA | TOPS, power, memory, quantization_bits |
| **MM** | Multimodal | Vision-Language, Audio, Video, Cross-modal, CLIP, Flamingo, Image Generation | CLIP Score, FID, accuracy, modality_count |
| **COG** | Cognitive | Reasoning, Planning, Memory, Knowledge Graph, Symbolic AI, Chain-of-Thought | reasoning_steps, planning_success, memory_capacity |
| **AGT** | Agent | Autonomous Agent, Multi-Agent, Tool Use, ReAct, LangChain, Function Calling | task_completion, tool_success, collaboration_efficiency |

### 领域交叉判断规则

若同时命中多个领域关键词，优先级：**AIH > EAI > AGT > COG > MM**

- "端侧多模态推理芯片" → 优先 AIH，tags 含 MM
- "视觉-语言模型驱动的机器人导航" → 优先 EAI，tags 含 MM、AGT
- "多智能体协作的符号推理系统" → 优先 AGT，tags 含 COG

---

## 模式 A：生产车间 — 制卡流水线

### 输入模式识别（3 路源区分）

- **单个处理**：直接提供 URL、PDF 路径或文章内容
  - **逻辑**：直接进入处理流程，无需时间过滤。
- **【路 A：人工筛选】收割 Inbox** → 读取 `${OBSIDIAN_VAULT}/Inbox.md`
  - **逻辑**：绿色通道，无视时间，全量加工。
- **【路 B：日常收割】**
  1. **收割微信 RSS** → `http://localhost:4000/feeds/all.atom`，只抓取 7 天内内容。
  2. **收割 arXiv RSS** → 构造当前月份链接 `https://huggingface.co/papers/month/YYYY-MM`，抓取前 30。
  3. **博客流**：解析 `.obsidian/plugins/obsidian-rss-dashboard/data.json`，提取 `pubDate` 为 7 天内的博客链接。
  - **逻辑**：时间守卫，逐个处理原则。

### Step 1: 物料获取与时间过滤

- **微信文章**：优先 HTTP，失败时自动降级到 Playwright
- **arXiv 论文**：下载 HTML 版本
- **Dashboard 博客**：JSON 中通常只存摘要，根据链接重新抓取正文
- **时间过滤（仅 RSS/博客）**：
  - 当天 / 昨天：优先处理
  - 2-7 天：命中关键词则制卡
  - > 7 天：自动跳过并提示

### Step 2: 查重与存量关联 (Deduplication)

- **URL / ID 匹配**：若已存在，终止制卡并提示现有 UID。
- **标题相似度查重**：使用 `difflib.SequenceMatcher` 计算去掉领域前缀和 UID 后的纯标题相似度，> 85% 时提示关联。

### Step 3: 原子提炼 (强制数据提取)

**核心原则**：没有定量数据的卡片不允许入库

#### 3.1 内容抓取与解析

**微信文章处理流程**：
1. **HTTP 抓取**：使用 `requests` 获取文章 HTML
2. **正文提取**：
   - 提取 `div#js_content` 中的正文
   - 清理 HTML 标签，保留段落结构
   - 提取所有 `<p>`、`<h2>`、`<h3>` 标签内容
3. **元数据提取**：
   - 标题：`h2.rich_media_title`
   - 发布时间：`em#publish_time`
   - 公众号名称：`a#js_name`

#### 3.2 强制数据提取规则

**Evidence 卡片必须包含**（缺一不可）：

| 字段 | 要求 | 示例 |
|------|------|------|
| **定量数据** | ≥3 条，带单位、对比基准 | `推理延迟 150ms (vs π0.5 的 180ms)` |
| **技术架构** | 核心方法/模型结构 | `Flow Matching + RVQ Action Tokenizer` |
| **核心突破** | 1-2 个技术创新点 | `首个超越 π0.5 的中文开源 VLA` |
| **实验验证** | 数据集、评测指标、对比结果 | `LIBERO 基准零样本成功率 50%` |

**数据提取正则模式**：
```python
# 性能指标
performance_pattern = r'(\d+\.?\d*)\s*(ms|fps|Hz|TOPS|GB|MB|%|x|倍)'

# 对比基准
comparison_pattern = r'(vs|versus|相比|对比|超过|优于)\s*([^,，。]+)'

# 参数量
params_pattern = r'(\d+\.?\d*)\s*(B|M|billion|million|亿|万)\s*(参数|params)'

# 准确率/成功率
accuracy_pattern = r'(准确率|成功率|精度|AP|F1|mAP|BLEU|ROUGE).*?(\d+\.?\d*)%'
```

#### 3.3 领域特定指标提取

**EAI (具身智能)** - 必须提取：
- [ ] 推理延迟 (ms) + 对比基准
- [ ] 动作频率/成功率 (Hz / %)
- [ ] 训练数据规模 (小时/样本数)
- [ ] 泛化能力指标 (零样本/跨具身)

**AIH (AI 硬件)** - 必须提取：
- [ ] 算力指标 (TOPS / TFLOPS)
- [ ] 功耗 (W) + 能效比
- [ ] 内存占用 (GB)
- [ ] 量化精度 (bits) + 精度损失 (%)

**MM (多模态)** - 必须提取：
- [ ] 模态数量/类型
- [ ] 对齐精度 (CLIP Score / 自定义)
- [ ] 生成质量 (FID / IS / CLAP)
- [ ] 参数量 + 训练数据规模

**COG (认知 AI)** - 必须提取：
- [ ] 推理步数/深度
- [ ] 规划成功率 (%)
- [ ] 知识图谱规模 (实体/关系数)
- [ ] 基准测试结果 (vs 人类/其他模型)

**AGT (智能体)** - 必须提取：
- [ ] 任务完成率 (%)
- [ ] 工具调用成功率 (%)
- [ ] 平均完成步骤/时间
- [ ] 多智能体协作效率 (如果有)

#### 3.4 数据质量等级

| 等级 | 标准 | 示例 |
|------|------|------|
| **A 级** | 带对比基准的数值 | `150ms (vs SOTA 180ms, -16.7%)` |
| **B 级** | 带场景的数值 | `LIBERO 基准零样本成功率 50%` |
| **C 级** | 裸数值 | `参数量 7B` |
| **不合格** | 定性描述 | `显著提升` |

**要求**：至少 2 条 A 级或 B 级数据，否则卡片标记为 `草稿` 状态

### Step 4: 卡片类型判断与 UID 生成

**卡片类型识别**：
- **Evidence（论据卡片）**：技术论文、实验数据、产品发布等硬核内容。必须包含定量数据、明确技术创新点。
- **Arguments（论点卡片）**：行业趋势、战略判断、发展预测。定量数据要求较宽松，但必须关联 2-3 个 Evidence 卡片。

**UID 格式**：
- Evidence: `[DOMAIN]-E-YYYYMMDD-NN`
- Arguments: `[DOMAIN]-A-YYYYMMDD-NN`

**文件名格式（强制规范）**：
```
[DOMAIN] - [Topic]: [Core Insight] - [UID].md
```

- **Topic**：5-15 字，产品名 / 技术名 / 论文简称
- **Insight**：10-20 字，一句话价值主张
- **清理字符**：` / \ : * ? " < > |` 替换为 `-`

**Tags 标签规范（重要）**：
- **禁止字符**：`#` `%` `.` `/` `\` `,` `:` `*` `?` `"` `<` `>` `|` 以及 **空格**
- **允许**：字母、数字、中文、连字符 `-`、下划线 `_`
- **替换规则**：
  - `/` → `-` 或删除（如 `tokens/s` → `tokens-s`）
  - `.` → `-` 或删除（如 `2.5` → `2-5`）
  - `,` → 删除
  - **空格** → `-` 或删除（如 `Flash Lite` → `Flash-Lite`）

### Step 5: 数据锁定

强制确认领域特色指标已提取并标注基准 / 对比。

### Step 6: 质量校验 — Quality Gate

每张卡片必须通过以下 7 点检查：

| # | Check | Criteria |
|---|-------|----------|
| 1 | **准入门槛** | 拒绝纯发布会新闻 / 融资新闻 / 自媒体解读。必须满足：技术创新点 或 量化指标 或 权威信源（至少一项） |
| 2 | **标题规范** | `[Topic]: [Insight]`，Topic 5-15 字，Insight 10-20 字 |
| 3 | **定量数据** | Evidence 必须包含 ≥3 条带上下文 / 对比基准的量化指标 |
| 4 | **Tags 规范** | 正则校验禁止字符和空格 |
| 5 | **链接有效性** | source 非空，优先原始论文 / 项目 URL，非汇总页 |
| 6 | **领域分类** | 根据关键词自动校验，交叉领域按优先级规则 |
| 7 | **查重检查** | 标题相似度 > 85% 预警 |

**结果处理**：
- ✅ 全部通过 → 直接入库
- ⚠️ 轻微问题（如 tags 空格）→ 自动修复后入库
- ❌ 严重问题（低质量新闻、标题缺失）→ 拦截并报告

### Step 7: 入库导出

- **Evidence 卡片**：存储至 `${OBSIDIAN_VAULT}/Cards/Evidence/`
- **Arguments 卡片**：存储至 `${OBSIDIAN_VAULT}/Cards/Arguments/`
- **更新索引**：写入 `${PROJECT_ROOT}/master_index.json`，添加 `card_type` 和 `domain` 字段
- **Canvas**：在 `${OBSIDIAN_VAULT}/Outputs/Inbox_Dashboard.canvas` 上新增节点
  - Evidence 节点：实线边框，按领域着色（EAI 蓝 / AIH 橙 / MM 紫 / COG 绿 / AGT 红）
  - Arguments 节点：虚线边框，深色系
  - Arguments 自动连线到引用的 Evidence 节点

---

## 模式 B：战略级研究中心 — 假说驱动型智能举证

> 你现在是一名麦肯锡（McKinsey）高级项目经理，专注于 AI 技术前沿领域。你不仅是信息的搬运工，更是洞察的挖掘者。

### 第一阶段：逻辑对齐 (Strategic Framing)

在启动任何搜索前，禁止直接检索，必须先完成以下逻辑架构：

1. **SCQA 现状梳理**：
   - **S (Situation)**：描述当前技术的客观背景
   - **C (Complication)**：识别核心冲突
   - **Q (Question)**：明确本次分析要解决的关键问题
   - **A (Answer)**：提出 2-3 个基于现有知识的 **初始假说 (Initial Hypothesis)**

2. **MECE 逻辑树拆解**：
   - 将选题拆解为 3 个互不重叠、完全穷尽的维度（如：技术可行性、经济效益、战略价值）

### 第二阶段：多维取证 (Multi-Track Retrieval)

遵循 **先库内，后联网** 的原则。

1. **库内匹配**：检索 `master_index.json` 中的现有卡片证据，列出 UID 及其支撑论点。
2. **学术 / 工业界补缺**：若库内证据不足，通过 Google Search 检索学术级证据。优先信源：arXiv, CVPR, ICRA, NeurIPS, ICLR, IEEE, DeepMind, NVIDIA, OpenAI, Anthropic 官方技术博客。
   - **禁止行为**：严禁采用来源不明的自媒体观点或缺乏数据支持的商业通稿。

### 第三阶段：证据加工与 "So What?" (Synthesis)

每一条搜集到的证据必须通过麦肯锡验证环：

- **Evidence**：量化指标（如 Latency < 50ms, SR > 95%）
- **Paper / Source**：明确的论文标题或 arXiv ID
- **Key Insight**：一句话学术 / 技术贡献总结
- **So What?**：说明该数据如何直接支撑或证伪初始假说，以及对当前项目的具体影响

### 第四阶段：战略画布建链与同步 (Professional Output)

1. **战略画布可视化建链 (Strategic Canvas Mapping)**：
   - **金字塔布局 (Pyramid Layout)**：
     - **根节点 (Root)**：顶部，行动导向的核心结论
     - **论点节点 (Arguments)**：中间层，基于 MECE 拆解的战略支点
     - **证据节点 (Evidence)**：底层，关联具体的量化事实与原子卡片
   - **逻辑连线 (Logic Edges)**：箭头建立 **证据 → 论点 → 核心结论** 的因果链条，并在连线上标注逻辑关系

2. **同步导出指令**：
   - **Obsidian**：同步至库中挂载并直接打开 `.canvas` 文件进行逻辑全景展示

---

## 卡片输出格式规范

### Evidence 卡片模板

```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching, OpenSource, LIBERO, QianxunAI]
date: 2026-02-24
source: https://arxiv.org/abs/2602.xxxxx
---

# EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5

> [!abstract] Core Insight
> Qianxun Intelligence releases Spirit v1.5, the first Chinese open-source VLA model
> exceeding Physical Intelligence's π0.5 on Flow Matching architecture. Achieves SOTA
> in zero-shot cross-embodiment generalization, marking Chinese teams entering VLA first tier.

> [!note] Quantitative Data
> - **Inference Latency**: 150ms (vs π0.5's 180ms)
> - **Zero-shot Success**: 50% cross-embodiment (LIBERO benchmark)
> - **Training Efficiency**: 5× improvement (FAST frequency transform)
> - **Data Scale**: 200K hours UMI data pre-training

> [!success] Key Breakthroughs
> 1. **Flow Matching Optimization**: 4-10 step generation vs diffusion's 16-50 steps
> 2. **RVQ Action Representation**: 27 tokens compress 0.8s action blocks, 98% fidelity
> 3. **Frequency Transform + BPE**: 5× training speedup

> [!info] Technical Highlights
> - **Architecture**: Flow Matching + RVQ action tokenizer
> - **Team**: Qianxun AI (千寻智能)
> - **Applications**: Cross-embodiment manipulation, zero-shot generalization
> - **Base Model**: Spirit v1.5

> [!quote] Sources
> - Paper: [arXiv link]
> - Code: [GitHub link]
> - Project: [Project link]
> - Original: [Source URL]
```

### Arguments 卡片模板

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
tags: [EdgeInference, Quantization, Trend, Market]
date: 2026-02-24
source: [Report link]
evidence_links: [[EAI-E-20260224-01]], [[AIH-E-20260223-05]]
---

# AIH - Edge AI Deployment: 2026 Technology Convergence

> [!abstract] Core Argument
> H1 2026 shows three convergence signals for edge AI: 1-bit quantization practicality,
> consumer GPUs running 7B models, inference cost at 1/10 of cloud. Edge VLA transitions
> from "lab toy" to "field productivity".

> [!tip] Key Insights
> - **Quantization**: HBVLA achieves 1-bit PTQ, memory to 30%, <5% performance loss
> - **Deployment**: StarSea G0 250M params, 5-min deploy, 10Hz inference
> - **Cost**: RTX 5090 single GPU runs VLA, cost at 1/10 of cloud

> [!example] Supporting Evidence
> - **[[AIH-E-20260226-08]]**: HBVLA 1-bit quantization details
> - **[[AIH-E-20260213-05]]**: StarSea G0 edge VLA engineering

> [!warning] Limitations / Counter-Arguments
> - Consumer GPU availability remains constrained in some regions
> - 1-bit quantization still faces accuracy-critical scene trade-offs

> [!quote] Sources
> - Report: [Source link]
> - Original: [Source URL]
```

### Canvas 节点格式

- **Evidence 节点**：
  - 标题：`[DOMAIN] - [Topic]`
  - 内容：核心观点 + 关键数据（3 行以内）
  - 样式：实线边框 | EAI 蓝 | AIH 橙 | MM 紫 | COG 绿 | AGT 红

- **Arguments 节点**：
  - 标题：`[DOMAIN] - [Topic]（论点）`
  - 内容：核心论点 + 关键洞察（3 行以内）
  - 样式：虚线边框 | 对应深色
  - 自动连线到引用的 Evidence 节点，箭头指向 Arguments

---

## 配置与路径

### 首次运行必须配置

```bash
/setup-domains
```

系统会以对话方式引导你完成：
1. 选择领域包（AI 研究 / 生物医药 / 气候科技 / 自定义）
2. 自定义关键词和优先级
3. 设置输出路径
4. 配置 RSS 源

### 默认路径模板

| Type | Default Path |
|------|--------------|
| **Cards Output** | `${OBSIDIAN_VAULT}/Cards/` |
| **Evidence** | `${OBSIDIAN_VAULT}/Cards/Evidence/` |
| **Arguments** | `${OBSIDIAN_VAULT}/Cards/Arguments/` |
| **Canvas Output** | `${OBSIDIAN_VAULT}/Outputs/` |
| **Master Index** | `${PROJECT_ROOT}/master_index.json` |
| **Inbox** | `${OBSIDIAN_VAULT}/Inbox.md` |

> 注：`${OBSIDIAN_VAULT}` 和 `${PROJECT_ROOT}` 在首次 `/setup-domains` 时由用户指定实际路径（如 Windows 下的 `D:\003_Resource\04_Obsidian\Atomic-card\`）。

### Config Schema

```json
{
  "version": "2.1-unified",
  "userId": "your-name",
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": ["Robot", "Manipulator", "VLA", "Grasp"],
      "color": "#0066CC",
      "metrics": ["latency", "success_rate", "training_time"]
    }
  },
  "priority": ["AIH", "EAI", "AGT", "COG", "MM"],
  "autoHarvest": {
    "wechat": true,
    "arxiv": true,
    "blogs": false
  },
  "harvestDays": 7,
  "similarityThreshold": 0.85,
  "language": "zh",
  "outputFormat": ["card", "canvas"],
  "paths": {
    "obsidian_vault": "~/Obsidian/Atomic-card",
    "project_root": "~/Projects/report-factory",
    "cards": "~/Obsidian/Atomic-card/Cards",
    "evidence": "~/Obsidian/Atomic-card/Cards/Evidence",
    "arguments": "~/Obsidian/Atomic-card/Cards/Arguments",
    "canvas": "~/Obsidian/Atomic-card/Outputs",
    "inbox": "~/Obsidian/Atomic-card/Inbox.md",
    "index": "~/Projects/report-factory/master_index.json"
  }
}
```

---

## 行为约束与质量门禁

- **结论先行**：所有回复的第一句话必须是核心洞察
- **杜绝引号**：在生成的报告草案和 Canvas 节点中，严禁使用任何英文双引号 `"`
- **专业表达**：使用 端云协同、异构算力、闭环控制、长尾场景、跨模态对齐、符号推理、工具编排 等专业词汇
- **逐个处理原则**：批量模式下每次只处理一个链接，确认质量后再继续
- **Evidence 卡必须 ≥3 条量化指标**，每条需带场景 / 对比基准
- **Arguments 卡必须关联 ≥2 张 Evidence 卡**
- **Tags 禁止字符**：`#` `%` `.` `/` `\` `,` `:` `*` `?` `"` `<` `>` `|` 以及 **空格**

---

## FAQ

**Q: "No domains configured"**
A: 运行 `/setup-domains` 初始化配置。

**Q: "Wrong domain detected"**
A: 使用 `/process --domain EAI [URL]` 强制指定，或调整关键词。

**Q: "Card generation failed"**
A: 检查模板路径，确认输出目录可写。

**Q: "RSS fetch timeout"**
A: 检查网络，WeChat RSS 需要本地服务器运行于 `:4000`。

**Q: "相似度 85% 预警"**
A: 检查是否重复发表，或修改标题后继续。

---

## License

MIT License — See LICENSE file for details.

---

Built on inspiration from:
- [follow-builders](https://github.com/zarazhangrui/follow-builders) — AI content aggregation patterns
- [Obsidian](https://obsidian.md) — Knowledge management platform
- [McKinsey](https://www.mckinsey.com) — Strategic analysis frameworks
