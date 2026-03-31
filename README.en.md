[中文](README.md) | **English**

# Report Factory — Knowledge Card Factory

> **Track Information, Accumulate Knowledge** — Transform scattered technical content into structured Obsidian knowledge cards

**Core Philosophy:** Not just clipping, but **reusable knowledge accumulation**. Transform every paper and article into traceable, interconnected, reusable knowledge units.

---

## What You Get

Report Factory is a Claude Code skill that helps you build a **personal knowledge management system**:

- 📄 **Standardized Knowledge Cards** — Unified format Evidence and Arguments cards
- 🔗 **Bidirectional Link Network** — Automatic connections between cards, forming a knowledge graph
- 📊 **Quantitative Data Extraction** — Automatically extract key metrics and experimental data from papers
- 🏷️ **Intelligent Domain Classification** — Auto-detect research domains based on keywords
- 🔄 **RSS Auto-Harvesting** — One-stop collection from WeChat, arXiv, and blogs
- ✅ **Quality Gate** — 7-point validation to ensure card quality

All cards are stored in your local Obsidian, **data completely belongs to you**.

---

## Quick Start

### 1. Installation

```bash
git clone https://github.com/hoilex04/report-factory.git ~/.claude/skills/report-factory
```

### 2. Initial Setup

Enter in Claude Code:

```
/setup domains
```

The Agent will guide you through:

- Selecting domain packs (AI Research, Bio/Medical, Climate Tech, etc.)
- Customizing keywords
- Setting card output paths
- Configuring RSS sources

**No manual configuration file editing required**.

### 3. Start Using

```bash
# Process a single paper
/process https://arxiv.org/abs/2602.12345

# Batch harvest from RSS
/harvest wechat --days 7
/harvest arxiv --limit 30

# Deep topic analysis
/analyze "Edge AI Deployment Trends"
```

Your first knowledge card will be generated immediately after setup.

---

## Two Card Types

### Evidence Card

For **technical papers, experimental data, product releases** with specific information.

```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching, Quantization]
date: 2026-02-24
source: https://arxiv.org/abs/2602.xxxxx
---

# EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5

> [!abstract] Core Insight
> Qianxun Intelligence releases Spirit v1.5, the first Chinese open-source VLA model surpassing Physical Intelligence π0.5 on Flow Matching architecture...

> [!note] Quantitative Data
> - **Inference Latency**: 150ms (vs π0.5's 180ms)
> - **Zero-shot Success Rate**: 50% cross-embodiment (LIBERO benchmark)
> - **Training Efficiency**: 5× improvement (FAST frequency domain transform)
```

### Arguments Card

For **trend analysis, strategic assessments, literature reviews** synthesizing multiple sources.

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
evidence_links: [[EAI-E-20260224-01]], [[AIH-E-20260223-05]]
---

# AIH - Edge AI Deployment: 2026 Technology Convergence Signals

> [!abstract] Core Argument
> H1 2026 shows three convergence signals: 1-bit quantization becoming practical, consumer GPUs running 7B models, inference costs dropping to 1/10 of cloud...

> [!example] Supporting Evidence
> - **[[AIH-E-20260226-08]]**: HBVLA 1-bit quantization details
> - **[[AIH-E-20260213-05]]**: StarSea G0 edge VLA engineering practice
```

---

## Pre-configured Domain Packs

### AI Research Pack (Default)

| Code | Domain | Keywords | Typical Metrics |
|------|--------|----------|-----------------|
| **EAI** | Embodied AI | Robot, VLA, Manipulator, Navigation, Grasp | Latency, Success Rate, Training Time |
| **AIH** | AI Hardware | NPU, Chip, Edge Computing, Quantization | TOPS, Power, Memory Usage |
| **MM** | Multimodal | Vision-Language, Audio, Video, CLIP | CLIP Score, FID, Accuracy |
| **COG** | Cognitive AI | Reasoning, Planning, CoT, Knowledge Graph | Reasoning Steps, Planning Success Rate |
| **AGT** | Agent | Agent, Multi-Agent, Tool Use, ReAct | Task Completion Rate, Tool Call Success |

### Bio/Medical Pack

| Code | Domain | Keywords |
|------|--------|----------|
| **DRUG** | Drug Discovery | Drug Design, Molecular, Binding, Screening, ADMET |
| **GENO** | Genomics | Sequencing, Genome, CRISPR, Gene Expression |
| **MIMG** | Medical Imaging | MRI, CT, Radiology, Pathology, Segmentation |
| **CLIN** | Clinical AI | EHR, Diagnosis, Prognosis, Clinical Trial |

### Climate Tech Pack

| Code | Domain | Keywords |
|------|--------|----------|
| **REN** | Renewable Energy | Solar, Wind, Hydro, Energy Storage |
| **CARB** | Carbon Capture | CCS, Direct Air Capture, Carbon Sequestration |
| **BATT** | Battery Tech | Li-ion, Solid State, Energy Density, BMS |
| **CLIM** | Climate Modeling | Climate Simulation, Weather Prediction |

---

## Core Features

### Intelligent Domain Detection

Auto-detect article domains based on keywords, supporting multi-domain intersection content.

```
Input: https://arxiv.org/abs/2602.11832
Detection: EAI (Primary) + AIH (Secondary)
Keyword Match: VLA, Edge Deployment, Quantization
```

### Deduplication Mechanism

- **URL/ID Matching** — Automatic deduplication for same sources
- **Title Similarity Detection** — Warning triggered at 85%+ similarity
- **Content Fingerprint** — Prevent duplicate processing of different reports on same event

### Quality Gate

Each card must pass 7 validation points:

| Check Item | Standard |
|------------|----------|
| Entry Threshold | Tech Innovation OR Quantitative Data OR Authoritative Source |
| Title Format | [Topic]: 5-15 chars + [Insight]: 10-20 chars |
| Quantitative Data | Evidence cards need at least 3 metrics with context |
| Tag Format | No special characters or spaces |
| Source Link | Non-empty, prefer original paper/project URL |
| Domain Classification | Auto-validate keyword matching |
| Deduplication Check | Title similarity < 85% |

---

## Modifying Settings

Modify configuration through conversation, no manual file editing needed:

```
"Add Quantum Computing domain"
"Change card output path"
"Modify quality threshold"
"Show current configuration"
```

---

## Custom Extraction Style

The skill uses plain text prompt files to control content extraction.

### Through Conversation (Recommended)

Directly tell the Agent:
- "Focus on experimental methods when extracting"
- "Pay more attention to commercial application scenarios"
- "Write summaries in a more concise tone"

The Agent will automatically update the prompts.

### Direct Editing (Advanced Users)

Edit files in the `prompts/` folder:

- `extract-evidence.md` — Technical data extraction method
- `extract-arguments.md` — Trend insight extraction method
- `generate-card.md` — Card generation format
- `validate-card.md` — Quality validation rules
- `detect-domain.md` — Domain detection logic

These are plain text instructions that take effect immediately after modification.

---

## Installation

### Claude Code

```bash
git clone https://github.com/hoilex04/report-factory.git ~/.claude/skills/report-factory
```

### OpenClaw

```bash
clawhub install report-factory
# Or manual install
git clone https://github.com/hoilex04/report-factory.git ~/skills/report-factory
```

---

## System Requirements

- Claude Code or OpenClaw
- Obsidian (for viewing knowledge cards)
- Network connection (for fetching RSS and web content)

No API key required — web content is fetched through local scripts.

---

## How It Works

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   Input     │ →  │  Pipeline    │ →  │   Output     │
├─────────────┤    ├──────────────┤    ├──────────────┤
│ • Single URL│    │ 1. Domain    │    │ Evidence Card│
│ • RSS Feed  │    │    Detection │    │ ArgumentsCard│
│ • Local File│    │ 2. Content   │    │              │
│             │    │    Fetching  │    │ Canvas Graph │
│             │    │ 3. Deduplicate│   │ PPT Report   │
│             │    │ 4. Extraction│    │              │
│             │    │ 5. Quality   │    │              │
│             │    │    Validation│    │              │
│             │    │ 6. Card Gen  │    │              │
└─────────────┘    └──────────────┘    └──────────────┘
```

1. **Input** — Single URL, RSS feeds, local files
2. **Domain Detection** — Auto-identify research domain based on keywords
3. **Content Fetching** — Extract body, metadata, citation info
4. **Deduplication** — URL/title similarity dual check
5. **Data Extraction** — LLM extracts key metrics and insights
6. **Quality Validation** — 7-point validation ensures card quality
7. **Card Generation** — Output standardized Markdown cards
8. **Graph Construction** — Auto-generate Obsidian Canvas relationship graphs

---

## Project Structure

```
report-factory/
├── README.md                 # Project documentation
├── SKILL.md                  # Claude Skill definition
├── requirements.txt          # Python dependencies
├── config/
│   └── domain-packs.json     # Pre-configured domain packs
├── prompts/                  # LLM prompts
│   ├── extract-evidence.md
│   ├── extract-arguments.md
│   ├── generate-card.md
│   ├── validate-card.md
│   └── detect-domain.md
├── templates/                # Card templates
│   ├── evidence.md
│   └── arguments.md
├── scripts/                  # Helper scripts
│   ├── fetch-url.py
│   └── rss-harvest.py
└── examples/                 # Sample cards
    ├── sample-evidence-card.md
    └── sample-arguments-card.md
```

---

## Configuration

User configuration is stored in `~/.report-factory/config.json`:

```json
{
  "version": "2.0-generic",
  "userId": "your-name",
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": ["Robot", "VLA", "Manipulation", "Grasp"],
      "color": "#0066CC",
      "metrics": ["latency", "success_rate", "training_time"]
    },
    "AIH": {
      "name": "AI Hardware",
      "keywords": ["NPU", "Chip", "Edge Computing", "Quantization"],
      "color": "#FF6600",
      "metrics": ["TOPS", "power", "memory"]
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
  "paths": {
    "cards": "~/Obsidian/Cards",
    "canvas": "~/Obsidian/Canvas",
    "index": "~/master_index.json"
  }
}
```

---

## Output Examples

View sample cards:

- [Evidence Card Example](examples/sample-evidence-card.md)
- [Arguments Card Example](examples/sample-arguments-card.md)

---

## Privacy & Data Security

- **Local Data Storage** — All cards saved in your own Obsidian
- **No API Key Required** — Web content fetched through local scripts
- **Local Configuration** — User preferences stored in `~/.report-factory/`
- **Public Content Only** — Process publicly accessible web pages and RSS
- **Your Knowledge Graph Belongs to You** — Export and migrate anytime

---

## Contributing

Contributions for new domain packs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Submitting new domain packs
- Improving extraction prompts
- Bug fixes

### Community Domain Packs

| Domain Pack | Contributor | Domain Count |
|-------------|-------------|--------------|
| AI Research | Official | 5 |
| Bio/Medical | Official | 4 |
| Climate Tech | Official | 4 |
| Quantum Computing | _Your name?_ | _Submit PR_ |
| FinTech | _Your name?_ | _Submit PR_ |

---

## Acknowledgments

Inspired by:

- [follow-builders](https://github.com/zarazhangrui/follow-builders) — AI content aggregation patterns
- [Obsidian](https://obsidian.md) — Knowledge management platform
- [Zettelkasten](https://zettelkasten.de) — Slip-box note-taking method

---

## License

MIT License — See [LICENSE](LICENSE) file

---

<div align="center">

**Use Report Factory to transform information streams into knowledge assets**

[Quick Start](#quick-start) • [Features](#core-features) • [Examples](examples/)

</div>
