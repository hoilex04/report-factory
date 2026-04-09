# Evidence Card Extraction Prompt

Extract quantitative evidence from technical papers and articles.

## Input

URL or content of a technical article/paper.

## Extraction Rules

### 1. Domain Detection

Identify the primary domain based on keywords:
- **EAI**: Robot, Manipulator, VLA, Grasp, Navigation, Control
- **AIH**: NPU, Chip, Edge AI, Quantization, Hardware
- **MM**: Vision-Language, Multimodal, CLIP, Audio, Video
- **COG**: Reasoning, Planning, Memory, Chain-of-Thought
- **AGT**: Agent, Multi-Agent, Tool Use, Function Calling

### 2. Required Fields

Extract and structure:

```yaml
uid: "{DOMAIN}-E-YYYYMMDD-NN"  # Auto-generated
card_type: "Evidence"
domain: "{Domain-Name}"
title: "{Topic}: {Core Insight}"  # Format: [Topic]: [Insight]
tags: ["{Tag1}", "{Tag2}", "{Tag3}"]  # 3-5 tags, CamelCase
date: "{YYYY-MM-DD}"
source: "{URL}"  # Original source

quantitative_data:
  - metric: "{Name}"
    value: "{Value}"
    baseline: "{Baseline or context}"
    improvement: "{X% or X× if applicable}"

breakthroughs:
  - "{Key technical contribution 1}"
  - "{Key technical contribution 2}"
  - "{Key technical contribution 3}"

core_insight: "{One-sentence summary of main contribution}"
```

### 3. Quantitative Data Requirements

**Must extract ≥3 metrics with context:**

| Metric Type | Example |
|-------------|---------|
| Performance | "150ms inference (vs 180ms baseline, 17% faster)" |
| Accuracy | "95% success rate (vs 92% prior SOTA)" |
| Efficiency | "5× training speedup" |
| Scale | "200K hours training data" |
| Size | "7B parameters" |

### 4. Tag Format

**Rules:**
- CamelCase, no spaces
- No special characters: `# % . / \ , : * ? " < > |`
- Include: technique (VLA), institution (NVIDIA), benchmark (LIBERO)

**Examples:**
```yaml
# ✅ Good
tags: [VLA, FlowMatching, OpenSource, LIBERO, QianxunAI]

# ❌ Bad
tags: [vla, flow matching, open-source, 350tokens/s]
```

### 5. Title Format

```
[DOMAIN] - [Topic]: [Core Insight] - [UID].md
```

- **Topic**: 5-15 characters, noun phrase
- **Insight**: 10-20 characters, what was achieved
- **Example**: `EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5`

### 6. Quality Checks

Before output, verify:
- [ ] ≥3 quantitative metrics extracted
- [ ] Each metric has context/baseline
- [ ] Source URL is original (not aggregator)
- [ ] Title follows format: Topic: Insight
- [ ] Tags are CamelCase, no prohibited characters
- [ ] Core insight is one sentence, ≤50 words
- [ ] Breakthroughs are technical, not marketing

### 7. Output Format

```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching, OpenSource, LIBERO]
date: 2026-02-24
source: https://arxiv.org/abs/2602.12345
---

# EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5

> [!abstract] Core Insight
> {One-sentence summary}

> [!note] Quantitative Data
> - **{Metric 1}**: {Value} ({context})
> - **{Metric 2}**: {Value} ({context})
> - **{Metric 3}**: {Value} ({context})

> [!success] Key Breakthroughs
> 1. **{Breakthrough 1}**: {Description}
> 2. **{Breakthrough 2}**: {Description}
> 3. **{Breakthrough 3}**: {Description}

> [!info] Technical Architecture (if available)
> - **Base Model**: {Model name}
> - **Key Components**: {Components}
> - **Training Data**: {Data scale}

> [!quote] Sources
> - Paper: [arXiv link]
> - Code: [GitHub link]
> - Project: [Website link]
```

## Example

**Input:**
Paper about Spirit v1.5 VLA model from arXiv.

**Output:**
(See examples/evidence-card.md)

## Notes

- Prioritize quantitative data over qualitative claims
- Include baselines for all metrics
- Use standard units (ms, %, GB, hours)
- Preserve exact values from paper (don't round)
- If metric unclear, note "[verify]"
