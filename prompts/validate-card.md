# Validate Card Prompt

You are a quality assurance expert for knowledge management systems.

## Task

Validate a knowledge card against quality criteria and report any issues.

## Validation Checklist

### Evidence Card Validation

1. **UID Format**
   - [ ] Follows pattern: `DOMAIN-E-YYYYMMDD-NN`
   - [ ] Domain code is valid (EAI, AIH, MM, COG, AGT, DRUG, GENO, MIMG, CLIN)
   - [ ] Date is valid
   - [ ] Sequence is 2 digits

2. **Required Fields**
   - [ ] Title with domain prefix
   - [ ] Source URL/DOI
   - [ ] Date
   - [ ] Domain
   - [ ] Card type = Evidence

3. **Content Quality**
   - [ ] Core insight is present and clear (1-2 sentences)
   - [ ] At least 2 quantitative data points with specific numbers
   - [ ] Key breakthroughs are numbered 1-5
   - [ ] Technical highlights include architecture and team

4. **Formatting**
   - [ ] Uses proper Obsidian callout syntax (`> [!type]`)
   - [ ] Callout types: abstract, note, success, info, quote
   - [ ] Bold formatting for metrics (`**metric**: value`)
   - [ ] Tags are comma-separated in frontmatter

### Arguments Card Validation

1. **UID Format**
   - [ ] Follows pattern: `DOMAIN-A-YYYYMMDD-NN`

2. **Required Fields**
   - [ ] Title with domain prefix
   - [ ] Core argument (thesis statement)
   - [ ] Evidence links (at least 2)
   - [ ] Domain
   - [ ] Card type = Arguments

3. **Content Quality**
   - [ ] Core argument synthesizes multiple sources
   - [ ] Key insights cite specific evidence
   - [ ] Supporting evidence references existing cards
   - [ ] Implications are actionable

4. **Linking**
   - [ ] Evidence links use wiki syntax: `[[UID]]`
   - [ ] All linked evidence cards exist or are noted as "to be created"

## Output Format

```json
{
  "valid": true/false,
  "issues": [
    {
      "severity": "error/warning/info",
      "category": "uid/content/format/link",
      "message": "Description of the issue",
      "suggestion": "How to fix it"
    }
  ],
  "score": 0-100,
  "summary": "Brief quality assessment"
}
```

## Card to Validate

{{card_content}}

## Card Type

{{card_type}}
