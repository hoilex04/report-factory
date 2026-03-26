# Report Factory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Obsidian](https://img.shields.io/badge/Obsidian-1.x-purple.svg)](https://obsidian.md)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

**Transform any technical content into standardized knowledge cards for Obsidian.**

Report Factory is a universal knowledge card generator built for researchers and analysts tracking fast-moving fields. Define your own research domains, set custom keywords, and let AI automatically extract evidence from papers, articles, and RSS feeds.

![Report Factory Workflow](assets/workflow.png)

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

```bash
# Install WeChat MCP
git clone https://github.com/hoilex04/weixin-read-mcp
python server.py
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
