# Report Factory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Obsidian](https://img.shields.io/badge/Obsidian-1.x-purple.svg)](https://obsidian.md)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

**[中文介绍](#中文介绍)** | **[English](#english-introduction)**

---

## 中文介绍

**将任何技术内容转化为标准化的 Obsidian 知识卡片。**

Report Factory 是一个通用的知识卡片生成器，专为追踪快速发展的领域的研究人员和分析师而构建。定义你自己的研究领域，设置自定义关键词，让 AI 自动从论文、文章和 RSS 订阅源中提取证据。

![Report Factory 工作流](assets/workflow.png)

### ✨ 核心特性

- **🎯 自定义领域** — 用关键词定义你的研究领域（AI、生物医疗、气候科技或任何领域）
- **🤖 自动领域检测** — 根据配置的关键词智能路由
- **📇 双卡片类型** — Evidence（技术数据）和 Arguments（趋势分析）
- **🔍 去重检测** — URL/ID 匹配 + 85% 标题相似度检查
- **✅ 质量门控** — 7 点验证确保证卡质量
- **📊 PPT/Canvas 导出** — 麦肯锡风格演示文稿 + Obsidian Canvas 可视化
- **📡 RSS 集成** — 微信、arXiv、博客仪表板自动收割

### 🎯 适用人群

| 用户类型 | 使用场景 |
|----------|----------|
| **研究人员** | 追踪领域最新进展，自动提取关键数据 |
| **分析师** | 生成行业调研报告，快速产出洞察 |
| **学生** | 整理文献笔记，构建个人知识库 |
| **技术爱好者** | 收藏高质量文章，结构化存储 |

### 📦 预配置领域包

| 包名 | 领域 | 适用人群 |
|------|------|----------|
| **AI Research** | 具身智能、AI 硬件、多模态、认知 AI、智能体 | AI 研究者、工程师 |
| **Bio/Medical** | 药物发现、基因组学、医学影像、临床 AI | 生物医学研究者 |
| **Climate Tech** | 可再生能源、碳捕获、电池技术、气候模型 | 气候科技从业者 |

### 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/hoilex04/report-factory.git
cd report-factory

# 安装依赖
pip install -r requirements.txt

# 交互式领域设置
python -m report_factory setup
```

### 常用命令

```bash
# 处理单篇文章
rf process https://arxiv.org/abs/2602.12345

# 批量收割
rf harvest wechat    # 微信 RSS
rf harvest arxiv     # arXiv 论文

# 分析模式
rf analyze "端侧 AI 部署趋势"
```

### 卡片示例

**Evidence 卡片（论据卡）**：
```markdown
# EAI - Spirit v1.5: 首个超越π0.5 的中国开源 VLA

> [!abstract] 核心观点
> 千寻智能发布 Spirit v1.5，首个在 Flow Matching 架构上超越π0.5 的中国开源 VLA 模型。

> [!note] 定量数据
> - **推理延迟**: 150ms (vs π0.5 的 180ms)
> - **零样本成功率**: 50% 跨具身迁移
> - **训练效率**: 5×提升
```

**Arguments 卡片（论点卡）**：
```markdown
# AIH - 端侧 AI 部署：2026 年技术收敛

> [!abstract] 核心论点
> 2026 年上半年端侧 AI 部署出现三大收敛信号：1bit 量化实用化、消费级显卡可运行 7B 模型、推理成本降至云端 1/10。
```

---

## English Introduction

**Transform any technical content into standardized knowledge cards for Obsidian.**

Report Factory is a universal knowledge card generator built for researchers and analysts tracking fast-moving fields. Define your own research domains, set custom keywords, and let AI automatically extract evidence from papers, articles, and RSS feeds.

---

---

## ✨ Features

- **🎯 Custom Domains** — Define your own research domains with keywords (AI, Bio/Med, Climate Tech, or any field)
- **🤖 Auto Domain Detection** — Intelligent routing based on your configured keywords
- **📇 Dual Card Types** — Evidence (technical data) and Arguments (trend analysis)
- **🔍 Deduplication** — URL/ID matching + 85% title similarity check
- **✅ Quality Gate** — 7-point validation before card acceptance
- **📊 PPT/Canvas Export** — McKinsey-style presentations + Obsidian Canvas visualizations
- **📡 RSS Integration** — WeChat, arXiv, blog dashboard auto-harvesting

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/hoilex04/report-factory.git
cd report-factory

# Install dependencies (Python 3.10+)
pip install -r requirements.txt

# Initialize configuration
python scripts/setup.py
```

### First Run

```bash
# Start domain setup (interactive)
python -m report_factory setup

# Or use Claude Code with the skill
claude /setup-domains
```

### Basic Usage

```bash
# Process single article
python -m report_factory process https://arxiv.org/abs/2602.12345

# Batch harvest
python -m report_factory harvest wechat
python -m report_factory harvest arxiv

# Analysis mode
python -m report_factory analyze "Your research topic"
```

---

## 📦 Pre-configured Domain Packs

### Pack 1: AI Research (Default)

| Code | Domain | Keywords |
|------|--------|----------|
| **EAI** | Embodied AI | Robot, Manipulator, Locomotion, VLA, Grasp, Navigation |
| **AIH** | AI Hardware | NPU, Chip, AI PC, Edge Computing, Hardware, Sensor |
| **MM** | Multimodal | Vision-Language, Audio, Video, Cross-modal, CLIP |
| **COG** | Cognitive | Reasoning, Planning, Memory, Knowledge Graph, CoT |
| **AGT** | Agent | Autonomous Agent, Multi-Agent, Tool Use, ReAct |

### Pack 2: Bio/Medical

| Code | Domain | Keywords |
|------|--------|----------|
| **DRUG** | Drug Discovery | Drug Design, Molecular, Binding, Screening |
| **GENO** | Genomics | Sequencing, Genome, CRISPR, Gene Expression |
| **MIMG** | Medical Imaging | MRI, CT, Radiology, Pathology |
| **CLIN** | Clinical AI | EHR, Diagnosis, Prognosis, Clinical Trial |

### Pack 3: Climate Tech

| Code | Domain | Keywords |
|------|--------|----------|
| **REN** | Renewable Energy | Solar, Wind, Hydro, Geothermal, Storage |
| **CARB** | Carbon Capture | CCS, Direct Air Capture, Sequestration |
| **BATT** | Battery | Li-ion, Solid State, Energy Density |
| **CLIM** | Climate Modeling | Simulation, Weather Prediction, Risk |

---

## 📁 Project Structure

```
report-factory/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── setup.py                  # Installation script
├── config/
│   └── domain-packs.json     # Pre-configured domain packs
├── scripts/
│   ├── setup.py              # Interactive setup wizard
│   ├── setup.js              # Claude Code setup
│   └── validate.py           # Configuration validator
├── templates/
│   ├── evidence.md           # Evidence card template
│   └── arguments.md          # Arguments card template
├── examples/
│   ├── cards/                # Sample output cards
│   └── canvas/               # Sample Canvas files
└── src/
    └── report_factory/       # Main Python package
        ├── __init__.py
        ├── config.py         # Configuration handling
        ├── detector.py       # Domain detection
        ├── fetcher.py        # Content fetching
        ├── extractor.py      # Data extraction
        ├── validator.py      # Quality gate
        └── exporter.py       # PPT/Canvas export
```

---

## ⚙️ Configuration

### Config File Location

```
~/.report-factory/
├── config.json          # User preferences and domains
├── paths.json           # Custom paths (override defaults)
└── prompts/             # Custom extraction prompts
```

### Example config.json

```json
{
  "version": "2.0-generic",
  "userId": "your-name",
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": ["Robot", "Manipulator", "VLA"],
      "color": "#0066CC",
      "metrics": ["latency", "success_rate"]
    }
  },
  "priority": ["AIH", "EAI", "MM"],
  "autoHarvest": {
    "wechat": true,
    "arxiv": true
  },
  "paths": {
    "cards": "D:\\Cards",
    "index": "D:\\master_index.json"
  }
}
```

---

## 📝 Card Templates

### Evidence Card

```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching, Institution]
date: 2026-02-24
source: https://arxiv.org/abs/2602.xxxxx
---

# EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5

> [!abstract] Core Insight
> Qianxun Intelligence releases Spirit v1.5, first Chinese open-source VLA
> exceeding π0.5 on Flow Matching architecture. SOTA in zero-shot generalization.

> [!note] Quantitative Data
> - **Inference Latency**: 150ms (vs π0.5's 180ms)
> - **Zero-shot Success**: 50% cross-embodiment
> - **Training Efficiency**: 5× improvement
```

### Arguments Card

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
tags: [Trend, EdgeInference]
evidence_links: [[EAI-E-20260224-01]]
---

# AIH - Edge AI Deployment: 2026 Technology Convergence

> [!abstract] Core Argument
> H1 2026 shows three convergence signals: 1-bit quantization, consumer GPUs
> running 7B models, inference cost at 1/10 of cloud.
```

---

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `setup` | Interactive domain setup wizard |
| `process <URL>` | Process single article/paper |
| `harvest <source>` | Batch harvest (wechat/arxiv/inbox) |
| `analyze "<topic>"` | Hypothesis-driven analysis |
| `show-domains` | View current configuration |
| `add-domain <code> "<keywords>"` | Add new domain |
| `remove-domain <code>` | Remove domain |
| `validate` | Check configuration validity |

---

## 🔌 Integrations

### WeChat RSS

Using `wewerss` to build WeChat RSS feed:

```bash
# Your wewerss instance endpoint
# Example: http://localhost:4000/feeds/all.atom
```

**Config:** Update `config.json` with your wewerss endpoint:
```json
{
  "autoHarvest": {
    "wechat": true
  },
  "wechatEndpoint": "http://localhost:4000/feeds/all.atom"
}
```

### Obsidian RSS Dashboard

Edit `.obsidian/plugins/obsidian-rss-dashboard/data.json`

### arXiv

Auto-generated: `https://huggingface.co/papers/month/YYYY-MM`

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=report_factory tests/
```

---

## 🤝 Contributing

### Adding a Domain Pack

1. Create `config/domain-packs/<pack-name>.json`
2. Add domain definitions with keywords
3. Test with sample articles
4. Submit PR

Example:
```json
{
  "name": "Quantum Computing",
  "domains": {
    "QC": {
      "name": "Quantum Computing",
      "keywords": ["Qubit", "Entanglement", "Quantum Gate"]
    }
  }
}
```

### Development Workflow

```bash
# Fork and clone
git clone https://github.com/hoilex04/report-factory.git

# Create branch
git checkout -b feature/your-feature

# Make changes and test
git commit -m "Add your feature"

# Push and PR
git push origin feature/your-feature
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [follow-builders](https://github.com/zarazhangrui/follow-builders) — Content aggregation patterns
- [Obsidian](https://obsidian.md) — Knowledge management platform
- [McKinsey](https://www.mckinsey.com) — Strategic analysis frameworks

---

## 📬 Support

- **Issues**: [GitHub Issues](https://github.com/hoilex04/report-factory/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hoilex04/report-factory/discussions)

---

## 🗺️ Roadmap

- [ ] Web UI for configuration
- [ ] More domain packs (Neuroscience, Finance, Law)
- [ ] Multi-language support (Chinese, Spanish)
- [ ] Plugin for Obsidian mobile
- [ ] API for programmatic access
