[English](README.md) | **中文**

# Report Factory — 知识卡片工厂

> **追踪信息，沉淀知识** —— 将零散的技术内容转化为结构化的 Obsidian 知识卡片

**核心理念：** 不是简单的剪藏，而是**可复用的知识沉淀**。让每一篇论文、每一篇文章都能转化为可关联、可溯源、可复用的知识单元。

---

## 你会得到什么

Report Factory 是一个 Claude Code 技能，帮你建立**个人知识管理系统**：

- 📄 **标准化知识卡片** —— 统一格式的 Evidence（证据卡）和 Arguments（论证卡）
- 🔗 **双向链接网络** —— 卡片之间自动关联，形成知识图谱
- 📊 **定量数据提取** —— 自动提取论文中的关键指标、实验数据
- 🏷️ **智能领域分类** —— 基于关键词自动识别研究领域
- 🔄 **RSS 自动收割** —— WeChat、arXiv、博客一站式采集
- ✅ **质量门禁** —— 7 点检查确保卡片质量

所有卡片存储在你本地的 Obsidian 中，**数据完全属于你自己**。

---

## 快速开始

### 1. 安装

```bash
git clone https://github.com/hoilex04/report-factory.git ~/.claude/skills/report-factory
```

### 2. 初始化设置

在 Claude Code 中输入：

```
/setup domains
```

Agent 会以对话方式引导你完成：

- 选择领域包（AI 研究、生物医药、气候科技等）
- 自定义关键词
- 设置卡片输出路径
- 配置 RSS 源

**无需手动编辑配置文件**。

### 3. 开始使用

```bash
# 处理单篇论文
/process https://arxiv.org/abs/2602.12345

# 批量收割 RSS
/harvest wechat --days 7
/harvest arxiv --limit 30

# 深度分析主题
/analyze "端侧 AI 部署趋势"
```

设置完成后，你的第一张知识卡片会立即生成。

---

## 两种卡片类型

### Evidence Card — 证据卡

用于**技术论文、实验数据、产品发布**等包含具体信息的内容。

```markdown
---
uid: EAI-E-20260224-01
card_type: Evidence
domain: Embodied-AI
tags: [VLA, FlowMatching, Quantization]
date: 2026-02-24
source: https://arxiv.org/abs/2602.xxxxx
---

# EAI - Spirit v1.5: 首个超越 π0.5 的开源中文 VLA

> [!abstract] 核心洞察
> 千寻智能发布 Spirit v1.5，首个在 Flow Matching 架构上超越 Physical Intelligence π0.5 的中文开源 VLA 模型...

> [!note] 定量数据
> - **推理延迟**: 150ms (vs π0.5 的 180ms)
> - **零样本成功率**: 50% 跨具身迁移 (LIBERO 基准)
> - **训练效率**: 5× 提升 (FAST 频域变换)
```

### Arguments Card — 论证卡

用于**趋势分析、战略研判、综述总结**等需要综合多篇文献的内容。

```markdown
---
uid: AIH-A-20260224-01
card_type: Arguments
domain: AI-Hardware
evidence_links: [[EAI-E-20260224-01]], [[AIH-E-20260223-05]]
---

# AIH - 端侧 AI 部署：2026 技术收敛信号

> [!abstract] 核心论点
> 2026 年上半年显示三个收敛信号：1-bit 量化实用化、消费级 GPU 运行 7B 模型、推理成本降至云端 1/10...

> [!example] 支撑证据
> - **[[AIH-E-20260226-08]]**: HBVLA 1-bit 量化细节
> - **[[AIH-E-20260213-05]]**: 星海 G0 端侧 VLA 工程实践
```

---

## 预配置领域包

### AI 研究包（默认）

| 代码 | 领域 | 关键词 | 典型指标 |
|------|------|--------|----------|
| **EAI** | 具身智能 | Robot, VLA, Manipulator, Navigation, Grasp | 延迟、成功率、训练时长 |
| **AIH** | AI 硬件 | NPU, Chip, Edge Computing, Quantization | TOPS、功耗、内存占用 |
| **MM** | 多模态 | Vision-Language, Audio, Video, CLIP | CLIP Score、FID、准确率 |
| **COG** | 认知 AI | Reasoning, Planning, CoT, Knowledge Graph | 推理步数、规划成功率 |
| **AGT** | 智能体 | Agent, Multi-Agent, Tool Use, ReAct | 任务完成率、工具调用成功率 |

### 生物医药包

| 代码 | 领域 | 关键词 |
|------|------|--------|
| **DRUG** | 药物发现 | Drug Design, Molecular, Binding, Screening, ADMET |
| **GENO** | 基因组学 | Sequencing, Genome, CRISPR, Gene Expression |
| **MIMG** | 医学影像 | MRI, CT, Radiology, Pathology, Segmentation |
| **CLIN** | 临床 AI | EHR, Diagnosis, Prognosis, Clinical Trial |

### 气候科技包

| 代码 | 领域 | 关键词 |
|------|------|--------|
| **REN** | 可再生能源 | Solar, Wind, Hydro, Energy Storage |
| **CARB** | 碳捕获 | CCS, Direct Air Capture, Carbon Sequestration |
| **BATT** | 电池技术 | Li-ion, Solid State, Energy Density, BMS |
| **CLIM** | 气候建模 | Climate Simulation, Weather Prediction |

---

## 核心功能

### 智能领域检测

基于关键词自动识别文章所属领域，支持多领域交叉内容。

```
输入: https://arxiv.org/abs/2602.11832
检测: EAI (主要) + AIH (次要)
关键词匹配: VLA, Edge Deployment, Quantization
```

### 去重机制

- **URL/ID 匹配** —— 同一来源自动去重
- **标题相似度检测** —— 85% 以上相似度触发警告
- **内容指纹** —— 防止重复处理同一事件的不同报道

### 质量门禁

每张卡片必须通过 7 点检查：

| 检查项 | 标准 |
|--------|------|
| 准入门槛 | 技术创新 OR 定量数据 OR 权威来源 |
| 标题格式 | [主题]: 5-15 字 + [洞察]: 10-20 字 |
| 定量数据 | Evidence 卡至少 3 个带上下文的指标 |
| 标签格式 | 禁止特殊字符和空格 |
| 来源链接 | 非空，优先原始论文/项目 URL |
| 领域分类 | 自动验证关键词匹配 |
| 去重检查 | 标题相似度 < 85% |

---

## 修改设置

通过对话即可修改配置，无需手动编辑文件：

```
"添加量子计算领域"
"修改卡片输出路径"
"更改质量阈值"
"显示当前配置"
```

---

## 自定义提取风格

Skill 使用纯文本 prompt 文件控制内容提取方式。

### 通过对话（推荐）

直接告诉 Agent：
- "提取时重点关注实验方法"
- "多关注商业应用场景"
- "用更简洁的语气写摘要"

Agent 会自动更新 prompt。

### 直接编辑（高级用户）

编辑 `prompts/` 文件夹：

- `extract-evidence.md` —— 技术数据提取方式
- `extract-arguments.md` —— 趋势洞察提取方式
- `generate-card.md` —— 卡片生成格式
- `validate-card.md` —— 质量验证规则
- `detect-domain.md` —— 领域检测逻辑

这些都是纯文本指令，修改后下次处理即生效。

---

## 安装

### Claude Code

```bash
git clone https://github.com/hoilex04/report-factory.git ~/.claude/skills/report-factory
```

### OpenClaw

```bash
clawhub install report-factory
# 或手动安装
git clone https://github.com/hoilex04/report-factory.git ~/skills/report-factory
```

---

## 系统要求

- Claude Code 或 OpenClaw
- Obsidian（用于查看知识卡片）
- 网络连接（用于获取 RSS 和网页内容）

无需 API key —— 网页内容由本地脚本获取。

---

## 工作原理

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   输入源     │ → │  处理管道     │ → │   输出卡片    │
├─────────────┤    ├──────────────┤    ├──────────────┤
│ • 单篇 URL  │    │ 1. 领域检测   │    │ Evidence 卡  │
│ • RSS 订阅  │    │ 2. 内容抓取   │    │ Arguments 卡 │
│ • 本地文件  │    │ 3. 去重检查   │    │              │
│             │    │ 4. 数据提取   │    │ Canvas 图谱  │
│             │    │ 5. 质量验证   │    │ PPT 报告     │
│             │    │ 6. 卡片生成   │    │              │
└─────────────┘    └──────────────┘    └──────────────┘
```

1. **输入** —— 单篇 URL、RSS 订阅、本地文件
2. **领域检测** —— 基于关键词自动识别研究领域
3. **内容抓取** —— 提取正文、元数据、引用信息
4. **去重检查** —— URL/标题相似度双重检查
5. **数据提取** —— LLM 提取关键指标和洞察
6. **质量验证** —— 7 点检查确保卡片质量
7. **卡片生成** —— 输出标准化 Markdown 卡片
8. **图谱构建** —— 自动生成 Obsidian Canvas 关联图谱

---

## 项目结构

```
report-factory/
├── README.md                 # 项目说明
├── SKILL.md                  # Claude Skill 定义
├── requirements.txt          # Python 依赖
├── config/
│   └── domain-packs.json     # 预配置领域包
├── prompts/                  # LLM 提示词
│   ├── extract-evidence.md
│   ├── extract-arguments.md
│   ├── generate-card.md
│   ├── validate-card.md
│   └── detect-domain.md
├── templates/                # 卡片模板
│   ├── evidence.md
│   └── arguments.md
├── scripts/                  # 辅助脚本
│   ├── fetch-url.py
│   └── rss-harvest.py
└── examples/                 # 示例卡片
    ├── sample-evidence-card.md
    └── sample-arguments-card.md
```

---

## 配置说明

用户配置存储在 `~/.report-factory/config.json`：

```json
{
  "version": "2.0-generic",
  "userId": "your-name",
  "domains": {
    "EAI": {
      "name": "Embodied AI",
      "keywords": ["Robot", "VLA", "Manipulation", "Grasp"],
      "color": "#0066CC",
      "metrics": ["latency", "success_rate", "training_time"]
    },
    "AIH": {
      "name": "AI Hardware",
      "keywords": ["NPU", "Chip", "Edge Computing", "Quantization"],
      "color": "#FF6600",
      "metrics": ["TOPS", "power", "memory"]
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
  "paths": {
    "cards": "~/Obsidian/Cards",
    "canvas": "~/Obsidian/Canvas",
    "index": "~/master_index.json"
  }
}
```

---

## 输出示例

查看示例卡片：

- [Evidence Card 示例](examples/sample-evidence-card.md)
- [Arguments Card 示例](examples/sample-arguments-card.md)

---

## 隐私与数据安全

- **数据本地存储** —— 所有卡片保存在你自己的 Obsidian 中
- **无需 API key** —— 网页内容通过本地脚本获取
- **配置本地保存** —— 用户偏好存储在 `~/.report-factory/`
- **只读取公开内容** —— 处理公开可访问的网页和 RSS
- **你的知识图谱属于你** —— 随时可以导出、迁移

---

## 贡献

欢迎贡献新的领域包！查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何：

- 提交新的领域包
- 改进提取提示词
- 修复 bug

### 社区领域包

| 领域包 | 贡献者 | 领域数 |
|--------|--------|--------|
| AI Research | 官方 | 5 |
| Bio/Medical | 官方 | 4 |
| Climate Tech | 官方 | 4 |
| 量子计算 | _你的名字？_ | _提交 PR_ |
| 金融科技 | _你的名字？_ | _提交 PR_ |

---

## 致谢

灵感来源于：

- [follow-builders](https://github.com/zarazhangrui/follow-builders) —— AI 内容聚合模式
- [Obsidian](https://obsidian.md) —— 知识管理平台
- [Zettelkasten](https://zettelkasten.de) —— 卡片盒笔记法

---

## 许可证

MIT License —— 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**用 Report Factory，把信息流转化为知识资产**

[快速开始](#快速开始) • [功能特性](#核心功能) • [示例卡片](examples/)

</div>
