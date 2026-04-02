# 📚 Report Factory

> **Universal Knowledge Card Generator** — Transform articles/papers into standardized Obsidian cards with domain intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://claude.ai)
[![Version](https://img.shields.io/badge/version-2.0--generic-green.svg)]()

---

## 🎯 What is Report Factory?

Report Factory is a **Claude Code Skill** that transforms any technical content into standardized knowledge cards for Obsidian. Built for researchers and analysts tracking fast-moving fields.

**Core Philosophy**: Evidence over opinions. Quantitative data over qualitative claims. **Your domains, your rules.**

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔧 **Custom Domains** | Define your own research domains with keywords |
| 🤖 **Auto Domain Detection** | Intelligent routing based on your keywords |
| 📄 **Dual Card Types** | Evidence (technical data) and Arguments (trend analysis) |
| 🔄 **Deduplication** | URL/ID matching + 85% title similarity check |
| ✅ **Quality Gate** | 7-point validation before card acceptance |
| 📊 **PPT/Canvas Export** | McKinsey-style presentations + Obsidian Canvas visualizations |
| 📡 **RSS Integration** | WeChat, arXiv, blog dashboard auto-harvesting |

---

## 🚀 Quick Start

### Installation

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/your-username/report-factory \
  ~/.claude/skills/report-factory
```

### First-Time Setup

```bash
# In Claude Code, run:
/setup-domains
```

### Usage

```bash
# Single article/paper
/process https://arxiv.org/abs/2602.xxxxx

# Batch process from RSS feeds
/harvest wechat    # WeChat RSS feeds (last 7 days)
/harvest arxiv     # arXiv top 30 papers (current month)
/harvest inbox     # Pre-filtered links from Inbox.md

# Analysis mode
/analyze "Your research topic"
```

---

## 📖 Documentation

- [Full Skill Documentation](./skill.md) - Complete usage guide
- [Domain Setup Guide](./docs/setup.md) - Configure your research domains
- [API Reference](./docs/api.md) - Commands and configuration
- [Examples](./examples/) - Sample cards and workflows

---

## 🎨 Pre-configured Domain Packs

### Pack 1: AI Research (Default)

| Code | Domain | Keywords |
|------|--------|----------|
| **EAI** | Embodied AI | Robot, Manipulator, Locomotion, Embodied AI, Grasp, Navigation, VLA, Control |
| **AIH** | AI Hardware | NPU, Chip, AI PC, Wearable, Edge Computing, Hardware, Sensor, ASIC, FPGA |
| **MM** | Multimodal | Vision-Language, Audio, Video, Cross-modal, CLIP, Flamingo, Image Generation |
| **COG** | Cognitive | Reasoning, Planning, Memory, Knowledge Graph, Symbolic AI, Chain-of-Thought |
| **AGT** | Agent | Autonomous Agent, Multi-Agent, Tool Use, ReAct, LangChain, Function Calling |

### Pack 2: Bio/Medical

| Code | Domain | Keywords |
|------|--------|----------|
| **DRUG** | Drug Discovery | Drug Design, Molecular, Binding, Screening, ADMET |
| **GENO** | Genomics | Sequencing, Genome, CRISPR, Gene Expression |
| **MIMG** | Medical Imaging | MRI, CT, Radiology, Pathology, Segmentation |
| **CLIN** | Clinical AI | EHR, Diagnosis, Prognosis, Clinical Trial |

### Pack 3: Climate Tech

| Code | Domain | Keywords |
|------|--------|----------|
| **REN** | Renewable Energy | Solar, Wind, Hydro, Geothermal, Energy Storage |
| **CARB** | Carbon Capture | CCS, Direct Air Capture, Carbon Sequestration |
| **BATT** | Battery | Li-ion, Solid State, Energy Density, BMS |
| **CLIM** | Climate Modeling | Climate Simulation, Weather Prediction, Risk Model |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Report Factory Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│  Input → Domain Detect → Fetch → Dedup → Extract → Quality  │
│                                                              │
│  Output → Card (.md) → Canvas (.canvas) → PPT (.pptx)       │
└─────────────────────────────────────────────────────────────┘
```

### Card Types

**Evidence Card** (for technical papers, experiments):
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
> Qianxun Intelligence releases Spirit v1.5, the first Chinese open-source VLA model...

> [!note] Quantitative Data
> - **Inference Latency**: 150ms (vs π0.5's 180ms)
> - **Zero-shot Success**: 50% cross-embodiment (LIBERO benchmark)
> - **Training Efficiency**: 5× improvement
```

**Arguments Card** (for trend analysis):
```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
evidence_links: [[EAI-E-20260224-01]], [[AIH-E-20260223-05]]
---

# AIH - Edge AI Deployment: 2026 Technology Convergence

> [!abstract] Core Argument
> H1 2026 shows three convergence signals for edge AI...

> [!example] Supporting Evidence
> - **[[AIH-E-20260226-08]]**: HBVLA 1-bit quantization details
> - **[[AIH-E-20260213-05]]**: StarSea G0 edge VLA engineering
```

---

## 📁 Directory Structure

```
report-factory/
├── skill.md              # Main skill documentation
├── README.md             # This file
├── .claude-plugin/       # Plugin configuration
│   └── plugin.json       # Plugin manifest
├── docs/                 # Additional documentation
│   ├── setup.md
│   ├── api.md
│   └── troubleshooting.md
├── examples/             # Sample outputs
│   ├── evidence-card.md
│   ├── arguments-card.md
│   └── canvas-example.canvas
├── prompts/              # Extraction prompts
│   ├── extract-evidence.md
│   └── extract-arguments.md
└── knowledge/            # Domain knowledge base
    ├── embodied_ai.md
    ├── ai_pc.md
    └── ai_wearables.md
```

---

## ⚙️ Configuration

Configuration is saved to `~/.report-factory/config.json`:

```json
{
  "version": "2.0-generic",
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
  "similarityThreshold": 0.85
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-domain-pack`)
3. Add domain pack to `config/domain-packs.json`
4. Test with sample articles
5. Submit PR with test cases

### Community Domain Packs

| Pack | Contributor | Domains |
|------|-------------|---------|
| AI Research | Default | 5 domains |
| Bio/Medical | Default | 4 domains |
| Climate Tech | Default | 4 domains |
| Quantum Computing | _Your name?_ | _Submit PR_ |

---

## 📄 License

MIT License — See [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

Built on inspiration from:
- [follow-builders](https://github.com/zarazhangrui/follow-builders) — AI content aggregation patterns
- [Obsidian](https://obsidian.md) — Knowledge management platform
- [McKinsey](https://www.mckinsey.com) — Strategic analysis frameworks

---

<div align="center">

**Made with ❤️ for researchers and knowledge workers**

[Documentation](./skill.md) • [Issues](../../issues) • [Discussions](../../discussions)

</div>
