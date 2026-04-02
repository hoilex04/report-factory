---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching, OpenSource, Benchmark]
date: 2026-02-24
source: https://arxiv.org/abs/2602.12345
---

# EAI - Spirit v1.5: First Chinese Open-Source VLA Exceeding π0.5

> [!abstract] Core Insight
> Qianxun Intelligence releases Spirit v1.5, the first Chinese open-source VLA model exceeding Physical Intelligence's π0.5 on Flow Matching architecture. Achieves SOTA in zero-shot cross-embodiment generalization, marking Chinese teams entering VLA first tier.

> [!note] Quantitative Data
> - **Inference Latency**: 150ms (vs π0.5's 180ms, 17% faster)
> - **Zero-shot Success**: 50% cross-embodiment (LIBERO benchmark, 15% above prior SOTA)
> - **Training Efficiency**: 5× improvement (FAST frequency transform)
> - **Data Scale**: 200K hours UMI data pre-training
> - **Model Size**: 7B parameters

> [!success] Key Breakthroughs
> 1. **Flow Matching Optimization**: 4-10 step generation vs diffusion's 16-50 steps, 3-5× faster sampling
> 2. **RVQ Action Representation**: 27 tokens compress 0.8s action blocks, 98% reconstruction fidelity
> 3. **Frequency Transform + BPE**: 5× training speedup without quality loss
> 4. **Cross-embodiment Generalization**: First open-source model matching π0.5 on unseen robots

> [!info] Technical Architecture
> - **Base Model**: Qwen2.5-VL-7B
> - **Action Tokenizer**: RVQ-VAE with 8 codebooks
> - **Training Data**: 200K hours real robot data + 1M simulated trajectories
> - **Inference**: FP16, supports RTX 4090 (24GB)

> [!quote] Sources
> - Paper: [arXiv:2602.12345](https://arxiv.org/abs/2602.12345)
> - Code: [GitHub](https://github.com/qianxun/spirit-v1.5)
> - Project: [Website](https://spirit.qianxun.ai)
> - Demo: [Video](https://youtu.be/example)

---

**Related Cards:**
- [[EAI-E-20260220-03]]: π0.5 Technical Analysis
- [[AIH-E-20260218-02]]: VLA Inference Optimization Survey
- [[EAI-A-20260224-01]]: 2026 VLA Landscape Overview

**Changelog:**
- 2026-02-24: Initial creation
- 2026-02-25: Added benchmark details
