# Report Factory Skill

**Transform any technical content into standardized Obsidian knowledge cards.**

## Overview

Report Factory is a Claude Code skill that converts technical articles, papers, and RSS feeds into structured knowledge cards for Obsidian. It supports two card types:

- **Evidence Cards**: Technical data, metrics, and findings
- **Arguments Cards**: Trend analysis and synthesized insights

## Installation

```bash
git clone https://github.com/hoilex04/report-factory.git ~/.claude/skills/report-factory
```

## Usage

Invoke the skill with natural language or slash commands:

### Basic Commands

```
/process https://arxiv.org/abs/2602.12345
/harvest wechat
/analyze "端侧AI部署趋势"
/setup domains
```

### Natural Language

- "处理这篇文章 https://arxiv.org/abs/xxx"
- "收割微信RSS本周的内容"
- "分析一下具身智能的最新趋势"
- "添加一个新领域：量子计算"

## Commands

### /process <url>
Process a single article or paper into knowledge cards.

**Parameters:**
- `url`: Article URL (arXiv, WeChat, blog, etc.)

**Example:**
```
/process https://arxiv.org/abs/2602.12345
```

### /harvest <source>
Batch harvest from RSS feeds.

**Sources:**
- `wechat`: WeChat RSS feeds
- `arxiv`: arXiv papers
- `inbox`: Local inbox folder

**Options:**
- `--days`: Number of days to harvest (default: 7)
- `--limit`: Max items to process (default: 30)

**Example:**
```
/harvest wechat --days 3 --limit 10
```

### /analyze <topic>
Deep analysis on a research topic.

**Parameters:**
- `topic`: Research question or topic
- `--depth`: Analysis depth 1-5 (default: 3)

**Example:**
```
/analyze "端侧AI部署趋势" --depth 4
```

### /setup
Interactive setup wizard for domains and preferences.

**Example:**
```
/setup domains
/setup preferences
```

### /domains
Manage research domains.

**Subcommands:**
- `list`: Show configured domains
- `add <code> <keywords>`: Add a new domain
- `remove <code>`: Remove a domain

**Example:**
```
/domains list
/domains add QC "Quantum Computing, Qubit, Quantum Algorithm"
/domains remove QC
```

## Configuration

User configuration is stored in `~/.report-factory/`:

```
~/.report-factory/
├── config.json          # User preferences and domains
├── paths.json           # Custom paths
└── prompts/             # Custom extraction prompts
```

### Domain Configuration

Domains define your research areas with keywords for auto-detection.

**Example config.json:**
```json
{
  "version": "2.0-generic",
  "userId": "your-name",
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": ["Robot", "Manipulator", "VLA", "Locomotion"],
      "color": "#0066CC",
      "metrics": ["latency", "success_rate"]
    },
    "AIH": {
      "name": "AI Hardware",
      "keywords": ["NPU", "Chip", "Edge Computing"],
      "color": "#FF6600"
    }
  },
  "priority": ["AIH", "EAI"],
  "paths": {
    "cards": "~/Cards",
    "index": "~/master_index.json"
  }
}
```

## Prompt Files

The skill uses prompt files in `prompts/` to control content extraction:

| File | Purpose |
|------|---------|
| `extract-evidence.md` | Extract technical data and metrics |
| `extract-arguments.md` | Extract trends and insights |
| `generate-card.md` | Generate final card markdown |
| `validate-card.md` | Quality validation rules |
| `detect-domain.md` | Auto-detect research domain |

Customize these prompts by editing them directly or asking Claude to modify them.

## Card Templates

Templates are in `templates/`:

- `evidence.md`: Evidence card format
- `arguments.md`: Arguments card format

## Output Format

### Evidence Card Example
```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching]
date: 2026-02-24
source: https://arxiv.org/abs/xxx
---
# EAI - Spirit v1.5: First Chinese Open-Source VLA

> [!abstract] Core Insight
> Qianxun Intelligence releases Spirit v1.5...

> [!note] Quantitative Data
> - **Inference Latency**: 150ms
> - **Zero-shot Success**: 50%
```

### Arguments Card Example
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
> H1 2026 shows three convergence signals...

> [!tip] Key Insights
> - **Quantization**: HBVLA achieves 1-bit PTQ
```

## Helper Scripts

Optional Python scripts in `scripts/` for advanced use:

- `fetch-url.py`: Fetch and clean web content
- `rss-harvest.py`: Batch RSS harvesting
- `validate-cards.py`: Batch card validation

## License

MIT
