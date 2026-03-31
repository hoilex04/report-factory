# Generate Card Prompt

You are a technical writer specializing in knowledge management for researchers.

## Task

Convert extracted data into a properly formatted Obsidian markdown card.

## Card Types

### Evidence Card Format
```markdown
---
uid: {{domain}}-E-{{YYYYMMDD}}-{{sequence}}
card_type: Evidence
domain: {{domain}}
tags: [{{tag1}}, {{tag2}}]
date: {{YYYY-MM-DD}}
source: {{url}}
---
# {{title}}

> [!abstract] 核心观点
> {{core_insight}}

> [!note] 定量数据
{{quantitative_data}}

> [!success] 关键突破
{{key_breakthroughs}}

> [!info] 技术亮点
- **核心架构**: {{architecture}}
- **团队**: {{team}}
- **应用场景**: {{applications}}
- **基座模型**: {{base_model}}

> [!quote] 来源
- {{institution}}
- 论文：{{source}}
- 原文链接：{{source}}
```

### Arguments Card Format
```markdown
---
uid: {{domain}}-A-{{YYYYMMDD}}-{{sequence}}
card_type: Arguments
domain: {{domain}}
tags: [{{tags}}]
evidence_links: {{evidence_links}}
---
# {{title}}

> [!abstract] 核心论点
> {{core_argument}}

> [!tip] 关键洞察
{{key_insights}}

> [!example] 支撑证据
{{supporting_evidence}}

> [!info] 启示
{{implications}}
```

## UID Generation Rules

1. Format: `{DOMAIN}-{TYPE}-{YYYYMMDD}-{SEQ}`
2. TYPE: E = Evidence, A = Arguments
3. SEQ: 2-digit sequence number (01, 02, ...)
4. DOMAIN: Use domain code (EAI, AIH, MM, etc.)

## Date Format

- Use YYYY-MM-DD format for date field
- Use YYYYMMDD format in UID

## Tag Guidelines

1. Include domain-specific tags (e.g., VLA, Robot)
2. Include method tags (e.g., FlowMatching, Transformer)
3. Include institution tag if notable
4. Max 5-7 tags

## Input Data

{{card_data}}

## Card Type

{{card_type}}

## Output

Return ONLY the formatted markdown card, no additional text.
