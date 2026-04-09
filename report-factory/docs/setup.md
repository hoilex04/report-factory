# Domain Setup Guide

This guide walks you through setting up Report Factory for your research needs.

## Table of Contents

- [First-Time Setup](#first-time-setup)
- [Pre-configured Domain Packs](#pre-configured-domain-packs)
- [Custom Domain Configuration](#custom-domain-configuration)
- [Managing Your Domains](#managing-your-domains)
- [RSS Integration](#rss-integration)

---

## First-Time Setup

When you first run the skill, you'll be guided through domain setup:

```bash
/setup-domains
```

### Step 1: Choose Your Domain Pack

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

### Step 4: Verify Configuration

```bash
/show-domains
```

Output:
```
Your configured domains:

| Code | Name       | Keywords Count | Color |
|------|------------|----------------|-------|
| EAI  | Embodied AI| 8              | Blue  |
| AIH  | AI Hardware| 9              | Orange|
| MM   | Multimodal | 7              | Purple|

Priority order: AIH > EAI > MM
```

---

## Pre-configured Domain Packs

### AI Research Pack (Default)

| Code | Domain | Default Keywords |
|------|--------|------------------|
| **EAI** | Embodied AI | Robot, Manipulator, Locomotion, Embodied AI, Grasp, Navigation, VLA, Control |
| **AIH** | AI Hardware | NPU, Chip, AI PC, Wearable, Edge Computing, Hardware, Sensor, ASIC, FPGA |
| **MM** | Multimodal | Vision-Language, Audio, Video, Cross-modal, CLIP, Flamingo, Image Generation |
| **COG** | Cognitive | Reasoning, Planning, Memory, Knowledge Graph, Symbolic AI, Chain-of-Thought |
| **AGT** | Agent | Autonomous Agent, Multi-Agent, Tool Use, ReAct, LangChain, Function Calling |

### Bio/Medical Pack

| Code | Domain | Default Keywords |
|------|--------|------------------|
| **DRUG** | Drug Discovery | Drug Design, Molecular, Binding, Screening, ADMET |
| **GENO** | Genomics | Sequencing, Genome, CRISPR, Gene Expression |
| **MIMG** | Medical Imaging | MRI, CT, Radiology, Pathology, Segmentation |
| **CLIN** | Clinical AI | EHR, Diagnosis, Prognosis, Clinical Trial |

### Climate Tech Pack

| Code | Domain | Default Keywords |
|------|--------|------------------|
| **REN** | Renewable Energy | Solar, Wind, Hydro, Geothermal, Energy Storage |
| **CARB** | Carbon Capture | CCS, Direct Air Capture, Carbon Sequestration |
| **BATT** | Battery | Li-ion, Solid State, Energy Density, BMS |
| **CLIM** | Climate Modeling | Climate Simulation, Weather Prediction, Risk Model |

---

## Custom Domain Configuration

### Creating a New Domain

```bash
/add-domain "Quantum Computing" "Qubit, Quantum Gate, Superposition, Entanglement, Quantum ML"
```

### Domain Schema

```json
{
  "domains": {
    "YOUR": {
      "name": "Your Domain",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "color": "#FF6600",
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

### Color Coding

Each domain has a color for visual organization:

| Domain | Color | Hex |
|--------|-------|-----|
| EAI | Blue | #0066CC |
| AIH | Orange | #FF6600 |
| MM | Purple | #9933CC |
| COG | Green | #339966 |
| AGT | Red | #CC3333 |

---

## Managing Your Domains

### View Current Configuration

```bash
/show-domains
```

### Add Keywords to Existing Domain

```bash
User: I want to add "LLM" to my Multimodal domain

System:
Current MM keywords: Vision-Language, Audio, Video, Cross-modal, CLIP

Updated MM keywords: Vision-Language, Audio, Video, Cross-modal, CLIP, LLM

Save changes? (y/n): y
```

### Remove a Domain

```bash
/remove-domain MM

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

## RSS Integration

### WeChat RSS Setup

Requires local server:

```bash
# Install WeChat MCP
git clone https://github.com/your-username/weixin-read-mcp
python server.py

# Access at http://localhost:4000/feeds/all.atom
```

### arXiv RSS

```
https://huggingface.co/papers/month/YYYY-MM
```

### Blog Dashboard (Obsidian Plugin)

Configure in `.obsidian/plugins/obsidian-rss-dashboard/data.json`:

```json
{
  "feeds": [
    {"url": "https://blog.example.com/rss", "pubDate": "2026-03-20"}
  ]
}
```

### Auto-Harvest Configuration

In `config.json`:

```json
{
  "autoHarvest": {
    "wechat": true,
    "arxiv": true,
    "blogs": false
  },
  "harvestDays": 7
}
```

---

## Configuration File Location

```
~/.report-factory/
├── config.json          # Main configuration
├── paths.json           # Custom paths (optional)
└── prompts/             # Custom extraction prompts (optional)
```

### Default Paths

| Type | Default Path |
|------|--------------|
| **Cards Output** | `D:\003_Resource\04_Obsidian\Atomic-card\Cards\` |
| **Evidence** | `...\Cards\Evidence\` |
| **Arguments** | `...\Cards\Arguments\` |
| **Canvas Output** | `D:\003_Resource\04_Obsidian\Atomic-card\Outputs\` |
| **Master Index** | `D:\001_Project\Prj_claudecode\master_index.json` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No domains configured" | Run `/setup-domains` |
| "Wrong domain detected" | Adjust keywords or use `/force-domain` |
| "Card generation failed" | Check paths, verify output directory writable |
| "RSS fetch timeout" | Check network, increase timeout in config |

---

## Next Steps

- Read the [API Reference](./api.md) for all available commands
- Check [Examples](./../examples/) for sample cards
- See [Troubleshooting](./troubleshooting.md) for common issues
