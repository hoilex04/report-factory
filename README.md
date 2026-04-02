# Report Factory - 知识卡片工厂

> 追踪信息，沉淀知识 —— 将零散的技术内容转化为可复用、可关联、可溯源的 Obsidian 知识卡片。

## 三件套架构

```
用户输入/RSS定时触发
        ↓
┌─────────────────────────────────────────┐
│  report-factory (收割+制卡 Agent)        │
│  • 抓取微信/arXiv/博客内容                │
│  • 强制提取定量数据 (≥3条带对比基准)      │
│  • 生成高质量 Evidence/Arguments 卡片    │
└─────────────────────────────────────────┘
        ↓ 文件系统监听
┌─────────────────────────────────────────┐
│  report-factory-reviewer (单卡评审 Agent)│
│  • 7点质量检查                           │
│  • A/B/C 分级                           │
│  • 实时拦截低质量卡片                    │
└─────────────────────────────────────────┘
        ↓ 18:30 定时触发
┌─────────────────────────────────────────┐
│  report-factory-daily-reviewer (日报 Agent)│
│  • 批量评审今日所有卡片                  │
│  • 生成日报统计                          │
│  • 发送邮件报告                          │
└─────────────────────────────────────────┘
```

## 组件说明

| 组件 | 职责 | 触发方式 |
|------|------|---------|
| **report-factory** | 收割外部信息源，生成标准化知识卡片 | 手动 `/process`, `/harvest` 或 RSS 定时 |
| **report-factory-reviewer** | 单卡片质量评审，A/B/C 分级 | 被主 Skill 调用或独立运行 |
| **report-factory-daily-reviewer** | 每日定时汇总，生成日报并邮件推送 | 每天 18:30 定时执行 |

## 快速开始

### 1. 安装

```bash
# 复制到 OpenClaw skills 目录
cp -r report-factory ~/.claude/skills/
cp -r report-factory-reviewer ~/.claude/skills/
cp -r report-factory-daily-reviewer ~/.claude/skills/
```

### 2. 配置

**report-factory**：
```bash
# 在 OpenClaw 中运行
/setup-domains
```

**report-factory-daily-reviewer**：
```bash
# 复制配置模板
cp report-factory-daily-reviewer/config.template.json \
   ~/.report-factory/daily-reviewer-config.json

# 编辑配置（填入你的邮箱授权码，不是登录密码）
# 详见 report-factory-daily-reviewer/README.md
```

### 3. 使用

```bash
# 单篇处理
/process https://arxiv.org/abs/2602.xxxxx

# 批量收割
/harvest wechat    # 收割微信RSS
/harvest arxiv     # 收割arXiv

# 查看日报
/daily_report      # 手动生成日报
```

## 卡片质量标准

### Evidence 卡片（论据卡）

**必须包含**：
- ✅ ≥3 条带对比基准的定量数据
- ✅ 完整技术架构描述
- ✅ 核心突破点分析
- ✅ 实验验证（数据集/指标/对比）

**示例**：
```markdown
> [!note] 定量数据
> - **推理延迟**: 150ms (vs π0.5 的 180ms, -16.7%)
> - **零样本成功率**: 50% (LIBERO 基准)
> - **训练效率**: 5× 提升
```

### Arguments 卡片（论点卡）

**必须包含**：
- ✅ 核心论点陈述
- ✅ 关联 2-3 张 Evidence 卡片
- ✅ 趋势判断依据

## 核心价值

| 特性 | 说明 |
|------|------|
| **Evidence优先** | 拒绝简单剪藏，强制要求定量数据 |
| **领域自适应** | EAI/AIH/MM/COG/AGT 五大领域自动分类 |
| **质量可观测** | A/B/C 分级，数据质量一目了然 |
| **自动化** | RSS→制卡→评审→日报，全流程自动化 |
| **OpenClaw原生** | 三Agent协作，体现多Agent编排能力 |

## 安全提示

⚠️ **重要**：`daily-reviewer-config.json` 包含邮箱授权码，**切勿提交到 GitHub**！

- 本仓库已配置 `.gitignore` 排除敏感文件
- 使用 `config.template.json` 作为配置模板（不含真实凭证）
- 详见 [SECURITY.md](report-factory-daily-reviewer/SECURITY.md)

## 目录结构

```
.
├── report-factory/              # 主Skill（收割+制卡）
│   ├── skill.md
│   └── README.md
├── report-factory-reviewer/     # 单卡质量评审
│   ├── skill.md
│   ├── README.md
│   └── .gitignore
├── report-factory-daily-reviewer/  # 日报生成
│   ├── skill.md
│   ├── README.md
│   ├── SECURITY.md
│   ├── config.template.json
│   └── .gitignore
└── README.md                    # 本文件
```

## 许可证

MIT License

## 致谢

- [Obsidian](https://obsidian.md) - 知识管理平台
- [OpenClaw](https://github.com/your-openclaw-repo) - Agent 框架
- [Zettelkasten](https://zettelkasten.de) - 卡片盒笔记法
