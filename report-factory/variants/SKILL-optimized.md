---
name: report-factory
description: AI Knowledge Card Factory — Auto-extracts evidence from papers/articles into standardized Obsidian cards with PPT/Canvas output. Supports 5 AI domains (EAI/AIH/MM/COG/AGT) with intelligent domain detection.
triggers:
  - "制卡"
  - "收割"
  - "处理"
  - "分析"
  - "report"
  - "生成卡片"
---

# Report Factory: AI Knowledge Card Generator

Transform AI research papers, articles, and RSS feeds into standardized knowledge cards for Obsidian. Built for researchers and analysts tracking fast-moving AI fields.

**Core Philosophy**: Evidence over opinions. Quantitative data over qualitative claims.

## Quick Start

```bash
# Single article/paper
/process https://arxiv.org/abs/2602.xxxxx

# Batch process from RSS feeds
/harvest wechat    # WeChat RSS feeds (last 7 days)
/harvest arxiv     # arXiv top 30 papers (current month)
/harvest inbox     # Pre-filtered links from Inbox.md

# Analysis mode
/analyze "端侧 AI 部署趋势"
```

---

## Table of Contents

1. [Features](#features)
2. [Domain Detection](#domain-detection)
3. [Workflow Overview](#workflow-overview)
4. [Input Modes](#input-modes)
5. [Card Generation](#card-generation)
6. [Output Formats](#output-formats)
7. [Configuration](#configuration)
8. [Examples](#examples)

---

## Features

| Feature | Description |
|---------|-------------|
| **5 AI Domains** | EAI (Embodied AI), AIH (AI Hardware), MM (Multimodal), COG (Cognitive), AGT (Agent) |
| **Auto Domain Detection** | Intelligent routing based on keywords with priority rules |
| **Dual Card Types** | Evidence (technical data) and Arguments (trend analysis) |
| **Deduplication** | URL/ID matching + 85% title similarity check |
| **Quality Gate** | 7-point validation before card acceptance |
| **PPT/Canvas Export** | McKinsey-style presentations + Obsidian Canvas visualizations |
| **RSS Integration** | WeChat, arXiv, blog dashboard auto-harvesting |

---

## Domain Detection

### Keyword Mapping

| Domain | Keywords | Example Topics |
|--------|----------|----------------|
| **EAI** (Embodied AI) | Robot, Manipulator, Locomotion, Grasp, Navigation, VLA, Control | 机器人操作、具身智能、VLA 模型 |
| **AIH** (AI Hardware) | NPU, Chip, AI PC, Edge Computing, Hardware, Sensor, ASIC, FPGA | 端侧推理、AI 芯片、模型量化 |
| **MM** (Multimodal) | Vision-Language, Audio, Video, Cross-modal, CLIP, Flamingo | 多模态理解、图文生成 |
| **COG** (Cognitive) | Reasoning, Planning, Memory, Knowledge Graph, Symbolic AI, CoT | 推理规划、符号推理 |
| **AGT** (Agent) | Autonomous Agent, Multi-Agent, Tool Use, ReAct, LangChain, Function Calling | 智能体框架、工具调用 |

### Priority Rules

When multiple domains match: `AIH > EAI > AGT > COG > MM`

**Examples**:
- "端侧多模态推理芯片" → AIH (hardware is core), tags include MM
- "视觉 - 语言模型驱动的机器人导航" → EAI (embodied is core), tags include MM, AGT
- "多智能体协作的符号推理系统" → AGT (agent framework is core), tags include COG

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Report Factory Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│  Input → Domain Detect → Fetch → Dedup → Extract → Quality  │
│                                                              │
│  Output → Card (.md) → Canvas (.canvas) → PPT (.pptx)       │
└─────────────────────────────────────────────────────────────┘
```

### Processing Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Production** | URL/PDF input, harvest commands | Direct card generation |
| **Research** | "分析", "为什么", "如何证明" | Hypothesis-driven analysis |

---

## Input Modes

### Mode A: Single Article/Paper

**Input**: Direct URL, PDF path, or article content

```
User: /process https://arxiv.org/abs/2602.12345

System:
✅ 成功抓取论文
━━━━━━━━━━━━━━━━━━
📄 标题：Flow Matching for VLA Training
🏢 机构：Physical Intelligence
📅 时间：2026-02-15
━━━━━━━━━━━━━━━━━━

🔍 领域识别：
   主领域：EAI (具身智能)
   交叉领域：MM (多模态)

✅ 开始生成 Evidence 卡片...
```

### Mode B: Batch Harvest

#### WeChat RSS
- **Endpoint**: `http://localhost:4000/feeds/all.atom`
- **Filter**: Last 7 days only
- **Domain Focus**: AI industry insights, Chinese tech blogs

#### arXiv Papers
- **Endpoint**: `https://huggingface.co/papers/month/YYYY-MM`
- **Limit**: Top 30 by engagement
- **Filter**: AI categories only

#### Blog Dashboard
- **Source**: `.obsidian/plugins/obsidian-rss-dashboard/data.json`
- **Filter**: `pubDate` within 7 days
- **Behavior**: Parse feeds array, fetch full content

### Mode C: Inbox Processing

**Input**: `D:\003_Resource\04_Obsidian\Atomic-card\Inbox.md`

- **Behavior**: Green channel — no time filter, process all links
- **Post-processing**: Move processed links to archive section

---

## Card Generation

### Card Types

| Type | Use Case | Requirements |
|------|----------|--------------|
| **Evidence** | Technical papers, experiments, product launches | ≥3 quantitative metrics, clear innovation |
| **Arguments** | Trends, strategic analysis, market reports | Must link 2-3 Evidence cards |

### UID Format

```
Evidence:   [DOMAIN]-E-YYYYMMDD-NN
Arguments:  [DOMAIN]-A-YYYYMMDD-NN

Domain codes: EAI | AIH | MM | COG | AGT
```

### Filename Convention

```
[DOMAIN] - [Topic]: [Core Insight] - [UID].md
```

**Examples**:
- `EAI - Spirit v1.5：首个超越π0.5 的中国开源 VLA - EAI-E-20260224-01.md`
- `AIH - 端侧推理成本：降至云端 1/10 部署门槛 - AIH-E-20260223-05.md`
- `MM - 多模态趋势：2026 年技术收敛方向 - MM-A-20260224-01.md`

**Sanitization Rules**:
- Replace `/ \ : * ? " < > |` with `-`
- Remove spaces (use `-` or concatenate)

### Tags Specification

| Allowed | Prohibited |
|---------|------------|
| Letters, numbers, Chinese | `#` `%` `.` `/` `\` `,` `:` `*` `?` `"` `<>` `|` **spaces** |

**Correct**: `端侧推理`, `SOTA`, `NPU`, `Gemini2-5`, `8B 参数`, `视觉 - 语言`
**Incorrect**: `350tokens/s`, `Gemini2.5`, `#端侧`, `Flash Lite`

---

## Quality Gate

Every card must pass 7-point validation:

| Check | Criteria |
|-------|----------|
| **1. Entry Threshold** | ✅ Technical innovation OR ✅ Quantitative metrics OR ✅ Authoritative source |
| **2. Title Format** | [Topic]: 5-15 chars, [Insight]: 10-20 chars |
| **3. Quantitative Data** | Evidence requires ≥3 metrics with context/baseline |
| **4. Tags Format** | Regex validation for prohibited characters |
| **5. Source Link** | Non-empty, prefer original paper/project URL |
| **6. Domain Classification** | Auto-verify against keyword rules |
| **7. Deduplication** | >85% title similarity triggers warning |

**Result Handling**:
- ✅ Pass all → Accept to library
- ⚠️ Minor issues (e.g., spaces in tags) → Auto-fix then accept
- ❌ Major issues (e.g., low-quality news, missing title) → Reject and report

---

## Output Formats

### Evidence Card Template

```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, Flow Matching, 千寻智能]
date: 2026-02-24
source: https://arxiv.org/abs/2602.xxxxx
---

# EAI - Spirit v1.5：首个超越π0.5 的中国开源 VLA

> [!abstract] 核心观点
> 千寻智能发布 Spirit v1.5，首个在 Flow Matching 架构上超越 Physical Intelligence π0.5 的中国开源 VLA 模型。
> 在零样本跨具身泛化任务上达到 SOTA，标志着中国团队首次进入 VLA 第一梯队。

> [!note] 定量数据
> - **推理延迟**: 150ms (vs π0.5 的 180ms)
> - **零样本成功率**: 50% 跨具身迁移 (LIBERO 基准)
> - **训练效率**: 5×提升 (FAST 频域变换技术)
> - **数据规模**: 20 万小时 UMI 数据预训练

> [!success] 关键突破
> 1. **Flow Matching 优化**: 4-10 步生成 vs 扩散模型 16-50 步
> 2. **RVQ 动作表征**: 27 tokens 压缩 0.8 秒动作块，98% 信息保真
> 3. **频域变换 +BPE 压缩**: 训练速度提升 5 倍

> [!quote] 来源
> - 论文：[arXiv 链接]
> - 代码：[GitHub 链接]
> - 项目主页：[项目链接]
```

### Arguments Card Template

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
tags: [趋势，端侧推理，市场]
date: 2026-02-24
source: [报告链接]
evidence_links: [[EAI-E-20260224-01]], [[AIH-E-20260223-05]]
---

# AIH - 端侧 AI 部署：2026 年技术收敛方向

> [!abstract] 核心论点
> 2026 年上半年端侧 AI 部署出现三大收敛信号：1bit 量化实用化、消费级显卡可运行 7B 模型、
> 推理成本降至云端 1/10。端侧 VLA 从"实验室玩具"转向"现场生产力"。

> [!tip] 关键洞察
> - **量化突破**: HBVLA 实现 1-bit 后训练量化，内存降至 30%，性能损失<5%
> - **部署门槛**: 星海图 G0 系列 250M 参数，5 分钟部署，10Hz 推理
> - **成本拐点**: RTX 5090 单卡可运行 VLA，成本降至云端方案 1/10

> [!example] 支撑证据
> - **[[AIH-E-20260226-08]]**: HBVLA 1-bit 量化技术细节
> - **[[AIH-E-20260213-05]]**: 星海图 G0 端侧 VLA 工程实践
```

### Canvas Visualization

| Node Type | Style | Color |
|-----------|-------|-------|
| **Evidence** | Solid border | EAI: Blue, AIH: Orange, MM: Purple, COG: Green, AGT: Red |
| **Arguments** | Dashed border | Darker shades of above |

**Layout**: Evidence nodes arranged left-to-right by date, Arguments nodes positioned above with arrows pointing to cited Evidence.

### PPT Export (McKinsey Style)

**Structure**:
1. Executive Summary (1 slide)
2. Background & Pain Points (1-2 slides)
3. Market & Applications (1-2 slides)
4. Technical Paths (2 slides)
5. Recommendations (1 slide)

**Visual Rules**:
- Title = Insight sentence (not topic phrase)
- Red (#C00000) for emphasis only, never bold+red together
- Source attribution: 9pt gray italic at bottom-left

---

## Configuration

### File Structure

```
~/.report-factory/
├── config.json          # User preferences
├── paths.json           # Custom paths (override defaults)
└── prompts/             # Custom extraction prompts
```

### Default Paths

| Type | Path |
|------|------|
| **Cards Output** | `D:\003_Resource\04_Obsidian\Atomic-card\Cards\` |
| **Evidence** | `...\Cards\Evidence\` |
| **Arguments** | `...\Cards\Arguments\` |
| **Canvas Output** | `D:\003_Resource\04_Obsidian\Atomic-card\Outputs\` |
| **Master Index** | `D:\001_Project\Prj_claudecode\master_index.json` |

### Config Schema

```json
{
  "defaultDomain": "EAI",
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
    "cards": "D:\\003_Resource\\04_Obsidian\\Atomic-card\\Cards",
    "index": "D:\\001_Project\\Prj_claudecode\\master_index.json"
  }
}
```

---

## Examples

### Example 1: Single Paper Processing

```
User: 处理这篇论文 https://arxiv.org/abs/2602.12345

System:
✅ 抓取成功
📄 标题：DreamZero: 38× Inference Acceleration for VLA
🏢 机构：NVIDIA
🔍 领域：EAI (命中：VLA, Robot, Navigation)

开始提取关键数据...
✅ 生成 Evidence 卡片：
   EAI - DreamZero:38×推理加速实现实时 VLA 控制 - EAI-E-20260209-02.md

关键指标：
   - 推理延迟：5.7s → 150ms (38×)
   - 闭环频率：7Hz
   - 泛化提升：2× vs SOTA VLA

是否入库？(y/n/edit):
```

### Example 2: Batch Harvest

```
User: 收割微信 RSS

System:
📡 正在抓取 WeChat RSS...
   发现 15 篇新文章 (最近 7 天)

⏳ AI 相关性分析...
   通过筛选：8 篇
   跳过：7 篇 (不相关/低质量)

📊 领域分布：
   - EAI (具身智能): 3 篇
   - AIH (端侧 AI): 3 篇
   - MM (多模态): 2 篇

开始处理第 1 篇：千寻智能 Spirit v1.5 技术解读
...
```

### Example 3: Analysis Mode

```
User: 分析一下端侧 AI 部署的必要性

System:
🔍 启动【麦肯锡研究中心】模式

第一步：逻辑对齐 (SCQA)
- S: 大模型从云端向端侧迁移是全球趋势
- C: 端侧部署面临延迟、功耗、成本三重瓶颈
- Q: 端侧 AI 部署是否具备经济/技术可行性？
- A: 初始假说 — 1bit 量化 + 边缘优化已突破临界点

第二步：库内取证
检索 master_index.json...
找到 12 张相关 Evidence 卡片：
- AIH-E-20260226-08: HBVLA 1-bit 量化
- AIH-E-20260213-05: 星海图 G0 端侧部署
...

需要我补充外部搜索吗？(y/n):
```

---

## Integration

### RSS Feed Setup

**WeChat RSS** (requires local server):
```bash
# Install WeChat MCP
git clone https://github.com/your-username/weixin-read-mcp
python server.py
# Access at http://localhost:4000/feeds/all.atom
```

**arXiv RSS**:
```
https://huggingface.co/papers/month/YYYY-MM
```

**Blog Dashboard** (Obsidian plugin):
```json
// .obsidian/plugins/obsidian-rss-dashboard/data.json
{
  "feeds": [
    {"url": "https://blog.example.com/rss", "pubDate": "2026-03-20"}
  ]
}
```

### Custom Prompts

Override default extraction prompts:
```bash
mkdir -p ~/.report-factory/prompts
cp .claude/skills/report-factory/prompts/extract-evidence.md ~/.report-factory/prompts/
# Edit to customize extraction rules
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "无法打开网页" | 检查网络连接，WeChat RSS 需要本地服务器运行 |
| "相似度 85% 预警" | 检查是否重复发表，或修改标题后继续 |
| "领域识别错误" | 手动指定：`/process --domain EAI [URL]` |
| "卡片生成失败" | 检查模板路径，确认输出目录可写 |

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-domain`)
3. Add domain keywords to `domain-detection.py`
4. Test with sample articles
5. Submit PR with test cases

---

## License

MIT License — See LICENSE file for details.

---

## Acknowledgments

Built on inspiration from:
- [follow-builders](https://github.com/zarazhangrui/follow-builders) — AI content aggregation patterns
- [Obsidian](https://obsidian.md) — Knowledge management platform
- [McKinsey](https://www.mckinsey.com) — Strategic analysis frameworks
