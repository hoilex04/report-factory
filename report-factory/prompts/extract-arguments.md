# Arguments Card Extraction Prompt

Synthesize trends and arguments from multiple evidence cards.

## Input

Research question or topic + related evidence cards.

## Extraction Rules

### 1. Domain Detection

Use the same domain as primary evidence cards, or multiple if cross-domain.

### 2. Required Fields

```yaml
uid: "{DOMAIN}-A-YYYYMMDD-NN"  # Auto-generated
card_type: "Arguments"
domain: "{Domain-Name}"
title: "{Topic}: {Core Argument}"  # Format: [Topic]: [Argument]
tags: ["{Tag1}", "{Tag2}", "Trend"]  # Include "Trend"
date: "{YYYY-MM-DD}"
source: "{Report URL or synthesis}"
evidence_links:
  - "[[{EVIDENCE-UID-1}]]"
  - "[[{EVIDENCE-UID-2}]]"
  - "[[{EVIDENCE-UID-3}]]"

core_argument: "{Main thesis with 2-3 supporting points}"

key_insights:
  - point: "{Point 1}"
    evidence: "[[{EVIDENCE-1}]]"
  - point: "{Point 2}"
    evidence: "[[{EVIDENCE-2}]]"
  - point: "{Point 3}"
    evidence: "[[{EVIDENCE-3}]]"

counter_arguments:
  - "{Limitation or counter-evidence}"

predictions:
  - timeline: "{When}"
    prediction: "{What will happen}"
    confidence: "{High/Medium/Low}"
```

### 3. Evidence Linking Requirements

**Must cite ≥2 evidence cards:**

```markdown
> [!example] Supporting Evidence
> - **[[EAI-E-20260224-01]]**: Spirit v1.5 achieves 50% zero-shot
> - **[[AIH-E-20260226-08]]**: HBVLA 1-bit quantization details
```

### 4. Argument Structure

**Thesis Statement Template:**
```
[Time period] shows [number] [convergence signals/trends] for [topic]:
1) [Signal 1], 2) [Signal 2], 3) [Signal 3].
[Conclusion about state change].
```

**Example:**
> H1 2026 shows three convergence signals for edge AI: 1-bit quantization practicality, consumer GPUs running 7B models, inference cost at 1/10 of cloud. Edge VLA transitions from "lab toy" to "field productivity".

### 5. Key Insights Format

Each insight must:
- State a specific finding
- Link to supporting evidence card
- Include quantitative backing

```markdown
> [!tip] Key Insights
> - **Quantization**: HBVLA achieves 1-bit PTQ, memory to 30%, <5% performance loss
> - **Deployment**: StarSea G0 250M params, 5-min deploy, 10Hz inference
> - **Cost**: RTX 5090 single GPU runs VLA, cost at 1/10 of cloud
```

### 6. Counter-Arguments

Always include limitations:
- Technical constraints
- Market barriers
- Alternative interpretations

### 7. Predictions (Optional)

If making predictions:
- Timeline (Q3 2026, 2027, etc.)
- Specific claim
- Confidence level

### 8. Tag Format

**Required tag:** `Trend`
**Recommended:** Domain-specific tags

```yaml
# ✅ Good
tags: [EdgeInference, Quantization, Trend, Market]

# ❌ Bad
tags: [analysis, some trends, 2026 predictions]
```

### 9. Quality Checks

Before output, verify:
- [ ] Core argument states a clear thesis
- [ ] ≥2 evidence cards linked
- [ ] Each insight has evidence backing
- [ ] Counter-arguments included
- [ ] Tags include "Trend"
- [ ] All evidence UIDs are valid (check index)
- [ ] Title format: Topic: Argument

### 10. Output Format

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
tags: [EdgeInference, Quantization, Trend, Market]
date: 2026-02-24
source: https://example.com/report
evidence_links: [[AIH-E-20260226-08]], [[AIH-E-20260213-05]]
---

# AIH - Edge AI Deployment: 2026 Technology Convergence

> [!abstract] Core Argument
> H1 2026 shows three convergence signals for edge AI: 1-bit quantization
> practicality, consumer GPUs running 7B models, inference cost at 1/10 of cloud.
> Edge VLA transitions from "lab toy" to "field productivity".

## Supporting Evidence

### Signal 1: [Topic]

> [!tip] Key Insight
> [Specific finding with quantitative backing]

**Evidence:**
- **[[EVIDENCE-UID-1]]**: [Brief description]
- **[[EVIDENCE-UID-2]]**: [Brief description]

### Signal 2: [Topic]

> [!tip] Key Insight
> [Specific finding with quantitative backing]

**Evidence:**
- **[[EVIDENCE-UID-3]]**: [Brief description]

### Signal 3: [Topic]

> [!tip] Key Insight
> [Specific finding with quantitative backing]

**Evidence:**
- **[[EVIDENCE-UID-4]]**: [Brief description]

## Market Implications (Optional)

| Segment | Current | Projection | Driver |
|---------|---------|------------|--------|
| [Segment] | [Status] | [Forecast] | [Reason] |

## Counter-Arguments

> [!warning] Limitations
> - [Technical constraint]
> - [Market barrier]
> - [Alternative interpretation]

## Predictions (Optional)

| Timeline | Prediction | Confidence |
|----------|------------|------------|
| [When] | [What] | [High/Medium/Low] |

---

**Evidence Links:**
- Primary: [[UID-1]], [[UID-2]]
- Supporting: [[UID-3]], [[UID-4]]

**Related Arguments:**
- [[ARGUMENT-UID-1]]
```

## Example

**Input:**
Research question: "How has 1-bit quantization evolved in edge VLA deployment?"
Evidence cards: [[AIH-E-20260226-08]], [[AIH-E-20260213-05]], [[AIH-E-20260220-05]]

**Output:**
(See examples/arguments-card.md)

## Notes

- Arguments must be evidence-based, not speculation
- Every claim needs supporting evidence card
- Include counter-arguments for credibility
- Use callout blocks (!abstract, !tip, !warning)
- Link evidence with [[UID]] format
