# 具身智能 (Embodied-AI) 核心关注点与硬核指标

作为“加工厂”的领域大脑，在提炼 EAI 论文或动态时，请务必锁定并对比以下指标：

## 1. 核心量化指标 (Hard Metrics)
- **推理时延 (Inference Latency)**: 目标 < 100ms (确保动作不卡顿，这是实现丝滑交互的红线)。
- **动作控制频率 (Action Frequency)**: 目标 25Hz+ (通常 20Hz-50Hz 是主流高性能机器人的标准)。
- **任务成功率 (Success Rate/SR)**: 区分“实验室环境”与“开放场景”下的 SR。
- **自由度 (DoF)**: 关注末端执行器或手臂的有效自由度配置。
- **训练数据量**: 关注训练所用的真实轨迹 (Real-world trajectories) 与 仿真数据 (Synthetic data) 的比例。

## 2. 技术关键词 (Tech Keywords)
- **VLA 模型**: Vision-Language-Action (视觉-语言-动作) 统一建模。
- **Sim-to-Real**: 仿真到现实的迁移效率与泛化误差。
- **端云协同 (Edge-Cloud Collaboration)**: 区分 System 1 (端侧实时反应) 与 System 2/3 (云端长程规划)。
- **异构数据融合**: 多源传感器（力觉、触觉、视觉）的同步处理。
- **零样本泛化 (Zero-shot Generalization)**: 在未见过的场景/物体上的表现。

## 3. 评价逻辑 (Evaluation Logic)
- **实时性优先**: 若推理时延 > 100ms，需在“豆腐块”中指出其在高速动态任务中的局限性。
- **成本敏感**: 关注是否使用了低成本方案（如 D-O-G Love, 消费级摄像头）实现了高性能。