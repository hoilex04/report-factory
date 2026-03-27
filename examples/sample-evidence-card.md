---
uid: AGT-E-20260227-12
card_type: Evidence
domain: Agent
tags: [Agent-World-Model, Snowflake, 合成环境, GRPO, Qwen3, 工具调用, OOD泛化, 强化学习]
date: 2026-02-27
source: https://arxiv.org/abs/2602.10090
---
# AGT - Agent World Model：千环境合成训练实现Agent跨分布泛化

> [!abstract] 核心观点
> Snowflake提出Agent World Model（AWM），构建全合成环境生成管线，扩展至1000个日常场景环境（平均35个工具/环境），通过代码驱动+数据库状态转换提供可靠交互。基于GRPO在Qwen3 4B/8B/14B上训练，是唯一在BFCLv3、τ²-bench、MCP-Universe三个OOD基准上全面提升的方法。

> [!note] 定量数据
> - **合成环境数量**: 1000个日常场景
> - **工具密度**: 平均35个工具/环境
> - **并行实例**: 1024个/训练步
> - **BFCLv3提升**: 8B模型 53.83 → 65.94（+12.11）
> - **τ²-bench**: 14B达39.03 Pass@1
> - **MCP-Universe**: 8B模型 6.70 → 11.17（+66.7%）

> [!success] 关键突破
> 1. **全合成环境管线**: 1000个代码驱动环境，数据库支撑状态转换，比LLM模拟环境更可靠一致
> 2. **唯一全面提升方法**: 在三个OOD基准上均优于基线，证明合成训练的泛化能力
> 3. **高效并行训练**: 1024个并行环境实例/步，混合奖励（步级格式检查+任务级结果验证）
> 4. **历史感知训练**: 训练与推理间滑动窗口截断对齐，提升长上下文Agent能力
> 5. **多规模验证**: 在Qwen3 4B/8B/14B三个规模上均验证有效性

> [!info] 技术亮点
> - **核心架构**: 合成环境生成 + GRPO强化学习 + 代码驱动状态转换
> - **团队**: Snowflake
> - **应用场景**: Agent训练、工具调用、多轮交互任务
> - **基座模型**: Qwen3 4B/8B/14B

> [!quote] 来源
> - Snowflake
> - 论文：https://arxiv.org/abs/2602.10090
> - 原文链接：https://arxiv.org/abs/2602.10090
