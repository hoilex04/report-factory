---
name: report-factory
description: Universal Knowledge Card Factory — Transform articles/papers into standardized Obsidian cards. Supports custom domains, intelligent detection, and PPT/Canvas output.
user-invocable: true
version: 2.0-generic
---

# Report Factory: Universal Knowledge Card Generator

Transform any technical content into standardized knowledge cards for Obsidian. Built for researchers and analysts tracking fast-moving fields.

**Core Philosophy**: Evidence over opinions. Quantitative data over qualitative claims. **Your domains, your rules.**

---

## Quick Start

```bash
# First-time setup - choose your domains
/setup-domains

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

## Table of Contents

1. [Features](#features)
2. [Domain Setup (First Run)](#domain-setup-first-run)
3. [Pre-configured Domain Packs](#pre-configured-domain-packs)
4. [Workflow Overview](#workflow-overview)
5. [Input Modes](#input-modes)
6. [Card Generation](#card-generation)
7. [Output Formats](#output-formats)
8. [Configuration](#configuration)
9. [Examples](#examples)

---

## Features

| Feature | Description |
|---------|-------------|
| **Custom Domains** | Define your own research domains with keywords |
| **Auto Domain Detection** | Intelligent routing based on your keywords |
| **Dual Card Types** | Evidence (technical data) and Arguments (trend analysis) |
| **Deduplication** | URL/ID matching + 85% title similarity check |
| **Quality Gate** | 7-point validation before card acceptance |
| **PPT/Canvas Export** | McKinsey-style presentations + Obsidian Canvas visualizations |
| **RSS Integration** | WeChat, arXiv, blog dashboard auto-harvesting |

---

## Domain Setup (First Run)

### Step 1: Initialize Configuration

When you first run the skill, you'll be guided through domain setup:

```
System: Welcome to Report Factory! Let me set up your research domains.

I see you're interested in AI technologies. Here are pre-configured options:

1. **AI Research Pack** (Recommended for AI researchers)
   - Embodied AI (VLA, Robot, Manipulation)
   - AI Hardware (NPU, Edge AI, Quantization)
   - Multimodal (Vision-Language, Cross-modal)
   - Cognitive AI (Reasoning, Planning, CoT)
   - AI Agents (Tool Use, Multi-Agent, Function Calling)

2. **Bio/Medical Pack**
   - Drug Discovery
   - Genomics
   - Medical Imaging
   - Clinical AI

3. **Climate Tech Pack**
   - Renewable Energy
   - Carbon Capture
   - Battery Technology
   - Climate Modeling

4. **Custom Setup** - Define your own domains

Which pack would you like? (1/2/3/4):
```

### Step 2: Customize Keywords

For each domain, you can customize the keyword list:

```
System: Setting up Embodied AI domain...

Default keywords: Robot, Manipulator, Locomotion, VLA, Grasp, Navigation, Control

Add your keywords? (current: none, or 'skip'):
```

### Step 3: Set Priority Rules

When content matches multiple domains, define priority:

```
System: When an article matches multiple domains, which takes priority?

Current order: AIH > EAI > AGT > COG > MM

Reorder? (example: "MM first" or 'skip'):
```

### Step 4: Save Configuration

Configuration is saved to `~/.report-factory/config.json`:

```json
{
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": ["Robot", "Manipulator", "VLA", "Grasp"],
      "color": "blue"
    },
    "AIH": {
      "name": "AI Hardware",
      "keywords": ["NPU", "Chip", "Edge AI", "Quantization"],
      "color": "orange"
    }
  },
  "priority": ["AIH", "EAI", "AGT", "COG", "MM"],
  "userId": "your-name"
}
```

---

## Pre-configured Domain Packs

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

### Pack 4: Custom

Define completely custom domains for your research area.

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
📄 Title: Flow Matching for VLA Training
🏢 Institution: Physical Intelligence
📅 Date: 2026-02-15
━━━━━━━━━━━━━━━━━━

🔍 Domain Detection:
   Primary: EAI (Embodied AI)
   Secondary: MM (Multimodal)

✅ Starting Evidence card generation...
```

### Mode B: Batch Harvest

#### WeChat RSS
- **Endpoint**: `http://localhost:4000/feeds/all.atom`
- **Filter**: Last 7 days only
- **Domain Focus**: Based on your configured keywords

#### arXiv Papers
- **Endpoint**: `https://huggingface.co/papers/month/YYYY-MM`
- **Limit**: Top 30 by engagement
- **Filter**: AI categories (or your configured domains)

#### Blog Dashboard
- **Source**: `.obsidian/plugins/obsidian-rss-dashboard/data.json`
- **Filter**: `pubDate` within 7 days
- **Behavior**: Parse feeds array, fetch full content

### Mode C: Inbox Processing

**Input**: Configurable path (default: `Inbox.md`)

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

Domain codes: Your configured domain abbreviations
```

### Filename Convention

```
[DOMAIN] - [Topic]: [Core Insight] - [UID].md
```

**Examples**:
- `EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5 - EAI-E-20260224-01.md`
- `AIH - Edge Inference Cost: 10x Reduction vs Cloud - AIH-E-20260223-05.md`
- `DRUG - AlphaFold3: Binding Affinity Prediction at 95% Accuracy - DRUG-E-20260224-01.md`

**Sanitization Rules**:
- Replace `/ \ : * ? " < > |` with `-`
- Remove spaces (use `-` or concatenate)

### Tags Specification

| Allowed | Prohibited |
|---------|------------|
| Letters, numbers, Chinese | `#` `%` `.` `/` `\` `,` `:` `*` `?` `"` `<>` `|` **spaces** |

**Correct**: `EdgeInference`, `SOTA`, `NPU`, `Gemini2-5`, `8BParams`
**Incorrect**: `350tokens/s`, `Gemini2.5`, `#Edge`, `Flash Lite`

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
| **6. Domain Classification** | Auto-verify against your keyword rules |
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
tags: [VLA, FlowMatching, Institution]
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

> [!quote] Sources
> - Paper: [arXiv link]
> - Code: [GitHub link]
> - Project: [Project link]
```

### Arguments Card Template

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
tags: [Trend, EdgeInference, Market]
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
```

### Canvas Visualization

| Node Type | Style | Color |
|-----------|-------|-------|
| **Evidence** | Solid border | Configured per domain |
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
├── config.json          # User preferences and domains
├── paths.json           # Custom paths (override defaults)
└── prompts/             # Custom extraction prompts
```

### Default Paths (Configurable)

| Type | Default Path |
|------|--------------|
| **Cards Output** | `D:\003_Resource\04_Obsidian\Atomic-card\Cards\` |
| **Evidence** | `...\Cards\Evidence\` |
| **Arguments** | `...\Cards\Arguments\` |
| **Canvas Output** | `D:\003_Resource\04_Obsidian\Atomic-card\Outputs\` |
| **Master Index** | `D:\001_Project\Prj_claudecode\master_index.json` |

### Config Schema

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
    },
    "AIH": {
      "name": "AI Hardware",
      "keywords": ["NPU", "Chip", "Edge AI"],
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
  "language": "en",
  "outputFormat": ["card", "canvas"],
  "paths": {
    "cards": "D:\\Cards",
    "index": "D:\\master_index.json"
  }
}
```

---

## Examples

### Example 1: First-Time Setup

```
User: /setup-domains

System: Welcome to Report Factory! Let me set up your research domains.

Which domain pack would you like?
1. AI Research (EAI, AIH, MM, COG, AGT)
2. Bio/Medical (Drug, Genomics, Imaging, Clinical)
3. Climate Tech (Renewable, Battery, Carbon)
4. Custom - Define your own

Your choice (1/2/3/4): 4

System: Great! Let's create your custom domains.

Domain 1 name (e.g., "Quantum Computing"):
Domain 1 keywords (comma-separated):

Continue adding domains? (y/n): n

Configuration saved to ~/.report-factory/config.json
```

### Example 2: Single Paper Processing

```
User: /process https://arxiv.org/abs/2602.12345

System:
✅ Fetch successful
📄 Title: DreamZero: 38× Inference Acceleration for VLA
🏢 Institution: NVIDIA
🔍 Domain: EAI (matched: VLA, Robot, Navigation)

Extracting key metrics...
✅ Generated Evidence card:
   EAI - DreamZero:38× Inference Acceleration for Real-time VLA - EAI-E-20260209-02.md

Key metrics:
   - Inference: 5.7s → 150ms (38×)
   - Closed-loop: 7Hz
   - Generalization: 2× vs SOTA VLA

Save to library? (y/n/edit):
```

### Example 3: Domain Change Request

```
User: I want to add "LLM" to my Multimodal domain

System:
Current MM keywords: Vision-Language, Audio, Video, Cross-modal, CLIP

Updated MM keywords: Vision-Language, Audio, Video, Cross-modal, CLIP, LLM

Save changes? (y/n): y

Configuration updated. Domain detection will use new keywords immediately.
```

---

## Changing Your Setup

### View Current Configuration

```
User: /show-domains

System:
Your configured domains:

| Code | Name       | Keywords Count | Color |
|------|------------|----------------|-------|
| EAI  | Embodied AI| 8              | Blue  |
| AIH  | AI Hardware| 9              | Orange|
| MM   | Multimodal | 7              | Purple|

Priority order: AIH > EAI > MM
```

### Add New Domain

```
User: /add-domain Fintech "Blockchain,DeFi,Crypto,Smart Contract"

System:
✅ New domain added:
   Code: FIN
   Name: Fintech
   Keywords: Blockchain, DeFi, Crypto, Smart Contract

Save to config? (y/n): y
```

### Remove Domain

```
User: /remove-domain MM

System:
⚠️ Warning: You have 12 cards tagged with MM. What should I do with them?
1. Reassign to nearest domain
2. Keep as "UNC" (Uncategorized)
3. Cancel deletion

Your choice: 1

System: Cards reassigned to COG (highest keyword overlap).
✅ Domain MM removed.
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
| "No domains configured" | Run `/setup-domains` to initialize |
| "Wrong domain detected" | Use `/force-domain EAI [URL]` or adjust keywords |
| "Card generation failed" | Check template paths, verify output directory writable |
| "RSS fetch timeout" | Check network, increase timeout in config.json |

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-domain-pack`)
3. Add domain pack to `config/domain-packs.json`
4. Test with sample articles
5. Submit PR with test cases

### Sharing Domain Packs

Community-contributed domain packs:

| Pack | Contributor | Domains |
|------|-------------|---------|
| AI Research | Default | 5 domains |
| Bio/Medical | Default | 4 domains |
| Climate Tech | Default | 4 domains |
| Quantum Computing | _Your name?_ | _Submit PR_ |

---

## License

MIT License — See LICENSE file for details.

---

## Acknowledgments

Built on inspiration from:
- [follow-builders](https://github.com/zarazhangrui/follow-builders) — AI content aggregation patterns
- [Obsidian](https://obsidian.md) — Knowledge management platform
- [McKinsey](https://www.mckinsey.com) — Strategic analysis frameworks

---

## Appendix: Domain-Specific Metrics

### AI Research Metrics (Default)

| Domain | Typical Metrics |
|--------|-----------------|
| EAI | Latency, Success Rate, Training Hours, Zero-shot % |
| AIH | TOPS, Power (W), Memory (GB), Quantization bits |
| MM | CLIP Score, FID, Accuracy, Modality Count |
| COG | Reasoning Steps, Planning Success, Memory Capacity |
| AGT | Task Completion, Tool Success, Collaboration Efficiency |

### Your Custom Metrics

Define domain-specific metrics in config:

```json
{
  "domains": {
    "YOUR": {
      "name": "Your Domain",
      "metrics": ["metric1", "metric2", "metric3"],
      "metricUnits": {
        "metric1": "ms",
        "metric2": "%",
        "metric3": "hours"
      }
    }
  }
}
```
