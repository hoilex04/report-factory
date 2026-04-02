# API Reference

Complete reference for all Report Factory commands and configuration options.

## Table of Contents

- [Commands](#commands)
- [Configuration Schema](#configuration-schema)
- [Card Templates](#card-templates)
- [Quality Gate](#quality-gate)
- [Output Formats](#output-formats)

---

## Commands

### `/setup-domains`

Initialize domain configuration for first-time users.

**Usage:**
```bash
/setup-domains
```

**Interactive Flow:**
1. Choose domain pack (AI Research / Bio-Medical / Climate Tech / Custom)
2. Customize keywords for each domain
3. Set priority order for multi-domain matches
4. Save configuration

**Output:**
```
✅ Configuration saved to ~/.report-factory/config.json
   Domains: EAI, AIH, MM, COG, AGT
   Priority: AIH > EAI > AGT > COG > MM
```

---

### `/process`

Process a single article or paper URL into a knowledge card.

**Usage:**
```bash
/process <URL>
/process <URL> --domain EAI
/process <URL> --type evidence
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `URL` | Yes | Article URL or PDF path |
| `--domain` | No | Force specific domain code |
| `--type` | No | Card type: `evidence` or `arguments` |

**Example:**
```bash
/process https://arxiv.org/abs/2602.12345
```

**Output:**
```
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

---

### `/harvest`

Batch process from RSS feeds.

**Usage:**
```bash
/harvest wechat    # WeChat RSS (last 7 days)
/harvest arxiv     # arXiv top 30 (current month)
/harvest inbox     # Pre-filtered links from Inbox.md
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| `wechat` | Process from WeChat RSS feed (localhost:4000) |
| `arxiv` | Process top 30 arXiv papers from current month |
| `inbox` | Process all links from Inbox.md (no time filter) |
| `--days N` | Override default harvest days |

**Example:**
```bash
/harvest wechat --days 3
```

**Output:**
```
📡 Fetching WeChat RSS (last 3 days)...
Found 12 new articles

Processing...
[████████░░] 80% (10/12)

✅ Results:
   - Passed: 8 cards
   - Duplicate: 2 skipped
   - Rejected: 2 (low quality)

Generated cards:
   - EAI-E-20260224-01: Spirit v1.5 VLA
   - AIH-E-20260224-03: Edge NPU Benchmark
   ...
```

---

### `/analyze`

Research mode with hypothesis-driven analysis.

**Usage:**
```bash
/analyze "Your research question"
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `question` | Yes | Research topic or question |

**Example:**
```bash
/analyze "How has 1-bit quantization evolved in edge VLA deployment?"
```

**Output:**
```
🔍 Research Mode: 1-bit quantization in edge VLA

Searching evidence cards...
Found 5 relevant Evidence cards:
- [[AIH-E-20260226-08]]: HBVLA 1-bit PTQ
- [[AIH-E-20260213-05]]: StarSea G0 edge deployment
- [[AIH-E-20260210-03]]: Binary neural networks survey

Generating Argument card...
✅ AIH-A-20260226-02: Edge VLA Quantization Trends 2026

Core argument: 1-bit quantization transitions from research concept
to production deployment in H1 2026, driven by 3 converging factors...

Evidence links:
- [[AIH-E-20260226-08]] (primary)
- [[AIH-E-20260213-05]] (supporting)
- [[AIH-E-20260210-03]] (background)
```

---

### `/show-domains`

Display current domain configuration.

**Usage:**
```bash
/show-domains
```

**Output:**
```
Your configured domains:

| Code | Name       | Keywords Count | Color |
|------|------------|----------------|-------|
| EAI  | Embodied AI| 8              | Blue  |
| AIH  | AI Hardware| 9              | Orange|
| MM   | Multimodal | 7              | Purple|

Priority order: AIH > EAI > MM

Config location: ~/.report-factory/config.json
```

---

### `/add-domain`

Add a new custom domain.

**Usage:**
```bash
/add-domain "Domain Name" "keyword1,keyword2,keyword3"
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Human-readable domain name |
| `keywords` | Yes | Comma-separated keywords |

**Example:**
```bash
/add-domain "Fintech" "Blockchain,DeFi,Crypto,Smart Contract"
```

**Output:**
```
✅ New domain added:
   Code: FIN
   Name: Fintech
   Keywords: Blockchain, DeFi, Crypto, Smart Contract

Save to config? (y/n): y
```

---

### `/remove-domain`

Remove an existing domain.

**Usage:**
```bash
/remove-domain <CODE>
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `CODE` | Yes | Domain code (e.g., EAI, AIH) |

**Example:**
```bash
/remove-domain MM
```

**Interactive Options:**
```
⚠️ Warning: You have 12 cards tagged with MM. What should I do with them?
1. Reassign to nearest domain (based on keyword overlap)
2. Keep as "UNC" (Uncategorized)
3. Cancel deletion

Your choice: 1

Cards reassigned to COG (highest keyword overlap).
✅ Domain MM removed.
```

---

### `/force-domain`

Force a specific domain for content processing.

**Usage:**
```bash
/force-domain <CODE> <URL>
```

**Example:**
```bash
/force-domain EAI https://arxiv.org/abs/2602.12345
```

---

## Configuration Schema

### Full Configuration Example

```json
{
  "version": "2.0-generic",
  "userId": "your-name",
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": [
        "Robot",
        "Manipulator",
        "Locomotion",
        "Embodied AI",
        "Grasp",
        "Navigation",
        "VLA",
        "Control"
      ],
      "color": "#0066CC",
      "metrics": [
        "latency",
        "success_rate",
        "training_time",
        "zero_shot_rate"
      ],
      "metricUnits": {
        "latency": "ms",
        "success_rate": "%",
        "training_time": "hours",
        "zero_shot_rate": "%"
      }
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
    "index": "D:\\master_index.json",
    "canvas": "D:\\Outputs"
  }
}
```

### Configuration Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | string | "2.0-generic" | Configuration version |
| `userId` | string | - | User identifier |
| `domains` | object | - | Domain definitions |
| `priority` | array | - | Domain priority order |
| `autoHarvest` | object | - | Auto-harvest settings |
| `harvestDays` | number | 7 | Default harvest window |
| `similarityThreshold` | number | 0.85 | Deduplication threshold |
| `language` | string | "en" | Output language |
| `outputFormat` | array | ["card"] | Output formats |
| `paths` | object | - | Custom paths |

---

## Card Templates

### Evidence Card

```markdown
---
uid: {DOMAIN}-E-{YYYYMMDD}-{NN}
card_type: Evidence
domain: {Domain-Name}
tags: [{Tag1}, {Tag2}, {Tag3}]
date: {YYYY-MM-DD}
source: {URL}
---

# {DOMAIN} - {Topic}: {Core Insight}

> [!abstract] Core Insight
> {One-sentence summary of the key contribution}

> [!note] Quantitative Data
> - **{Metric 1}**: {Value} ({context/baseline})
> - **{Metric 2}**: {Value} ({context/baseline})
> - **{Metric 3}**: {Value} ({context/baseline})

> [!success] Key Breakthroughs
> 1. **{Breakthrough 1}**: {Description}
> 2. **{Breakthrough 2}**: {Description}
> 3. **{Breakthrough 3}**: {Description}

> [!quote] Sources
> - Paper: [Link]
> - Code: [GitHub]
> - Project: [Website]
```

### Arguments Card

```markdown
---
uid: {DOMAIN}-A-{YYYYMMDD}-{NN}
card_type: Arguments
domain: {Domain-Name}
tags: [{Tag1}, {Tag2}]
date: {YYYY-MM-DD}
source: {URL}
evidence_links: [[{EVIDENCE-1}], [{EVIDENCE-2}]]
---

# {DOMAIN} - {Topic}: {Core Argument}

> [!abstract] Core Argument
> {Main thesis statement with supporting points}

> [!tip] Key Insights
> - **{Point 1}**: {Evidence-based detail}
> - **{Point 2}**: {Evidence-based detail}
> - **{Point 3}**: {Evidence-based detail}

> [!example] Supporting Evidence
> - **[[{EVIDENCE-1}]]**: {Brief description}
> - **[[{EVIDENCE-2}]]**: {Brief description}
> - **[[{EVIDENCE-3}]]**: {Brief description}
```

---

## Quality Gate

### 7-Point Validation

| Check | Criteria | Auto-fix |
|-------|----------|----------|
| **1. Entry Threshold** | Technical innovation OR quantitative metrics OR authoritative source | No |
| **2. Title Format** | [Topic]: 5-15 chars, [Insight]: 10-20 chars | Yes |
| **3. Quantitative Data** | Evidence requires ≥3 metrics with context | No |
| **4. Tags Format** | Regex validation for prohibited characters | Yes |
| **5. Source Link** | Non-empty, prefer original URL | No |
| **6. Domain Classification** | Auto-verify against keyword rules | Yes |
| **7. Deduplication** | >85% title similarity triggers warning | Yes |

### Result Handling

- ✅ **Pass all** → Accept to library
- ⚠️ **Minor issues** → Auto-fix then accept
- ❌ **Major issues** → Reject and report

---

## Output Formats

### Card (.md)

Standard Markdown with YAML frontmatter for Obsidian.

### Canvas (.canvas)

Obsidian Canvas visualization:

```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "file",
      "file": "Evidence/EAI-E-20260224-01.md",
      "x": 100,
      "y": 100,
      "width": 400,
      "height": 300
    }
  ],
  "edges": [
    {
      "fromNode": "node1",
      "toNode": "node2",
      "label": "supports"
    }
  ]
}
```

### PPT (.pptx)

McKinsey-style presentation:

| Slide | Content |
|-------|---------|
| 1 | Executive Summary |
| 2-3 | Background & Pain Points |
| 4-5 | Market & Applications |
| 6-7 | Technical Paths |
| 8 | Recommendations |

---

## UID Format

```
Evidence:   [DOMAIN]-E-YYYYMMDD-NN
Arguments:  [DOMAIN]-A-YYYYMMDD-NN

Examples:
- EAI-E-20260224-01  (Embodied AI Evidence)
- AIH-A-20260223-05  (AI Hardware Argument)
```

---

## Filename Convention

```
[DOMAIN] - [Topic]: [Core Insight] - [UID].md
```

**Sanitization Rules:**
- Replace `/ \ : * ? " < > |` with `-`
- Remove spaces (use `-` or concatenate)

**Examples:**
- `EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5 - EAI-E-20260224-01.md`
- `AIH - Edge Inference Cost: 10x Reduction vs Cloud - AIH-E-20260223-05.md`

---

## Tags Specification

### Allowed Characters

- Letters, numbers, Chinese
- No spaces (use CamelCase)

### Prohibited Characters

`#` `%` `.` `/` `\` `,` `:` `*` `?` `"` `<>` `|` **spaces**

### Examples

| ✅ Correct | ❌ Incorrect |
|-----------|-------------|
| `EdgeInference` | `350tokens/s` |
| `SOTA` | `Gemini2.5` |
| `NPU` | `#Edge` |
| `Gemini2-5` | `Flash Lite` |
| `8BParams` | `LLM, VLA` |

---

## Troubleshooting Commands

| Command | Purpose |
|---------|---------|
| `/show-domains` | Verify domain configuration |
| `/force-domain CODE URL` | Override auto-detection |
| Check `config.json` | Verify paths are correct |
| Check permissions | Ensure output directories are writable |
