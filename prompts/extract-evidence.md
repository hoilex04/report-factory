# Extract Evidence Prompt

You are an expert at extracting technical evidence from research papers and articles.

## Task

Extract structured technical evidence from the provided content and format it according to the Evidence Card schema.

## Domain Detection

First, determine which domain this content belongs to based on keywords:

| Domain Code | Keywords |
|-------------|----------|
| EAI | Robot, Manipulator, VLA, Grasp, Navigation, Locomotion |
| AIH | NPU, Chip, AI PC, Edge Computing, Hardware, Sensor, Quantization |
| MM | Vision-Language, Audio, Video, Cross-modal, CLIP, Multimodal |
| COG | Reasoning, Planning, Memory, Knowledge Graph, CoT, Chain-of-Thought |
| AGT | Agent, Autonomous Agent, Multi-Agent, Tool Use, ReAct, Function Calling |
| DRUG | Drug Design, Molecular, Binding, Screening, Drug Discovery |
| GENO | Sequencing, Genome, CRISPR, Gene Expression, Genomics |
| MIMG | MRI, CT, Radiology, Pathology, Medical Imaging |
| CLIN | EHR, Diagnosis, Prognosis, Clinical Trial, Clinical AI |

## Extraction Rules

Extract the following:

1. **Title**: Paper/article title (with domain prefix, e.g., "EAI - Title")
2. **Source**: URL or DOI
3. **Institution**: Research institution or company
4. **Core Insight**: 1-2 sentence summary of main contribution
5. **Quantitative Data**:
   - Metrics with specific numbers
   - Benchmark results
   - Performance comparisons
   - Format: `**Metric Name**: value (context)`
6. **Key Breakthroughs**:
   - Numbered list of 3-5 major contributions
   - Each should be specific and actionable
7. **Technical Highlights**:
   - Core architecture/method
   - Team/organization
   - Application scenarios
   - Base model (if applicable)

## Output Format

Return a JSON object:

```json
{
  "title": "Domain - Paper Title",
  "source": "https://...",
  "institution": "Organization Name",
  "domain": "EAI",
  "tags": ["Tag1", "Tag2", "Tag3"],
  "core_insight": "Main contribution summary...",
  "quantitative_data": [
    "**Metric**: value (comparison)",
    "**Metric2**: value2"
  ],
  "key_breakthroughs": [
    "1. First breakthrough...",
    "2. Second breakthrough..."
  ],
  "technical_highlights": {
    "architecture": "Method name",
    "team": "Organization",
    "applications": ["App1", "App2"],
    "base_model": "Model name (if any)"
  }
}
```

## Content to Process

{{content}}

## Domain Hint (if provided)

{{domain_hint}}
