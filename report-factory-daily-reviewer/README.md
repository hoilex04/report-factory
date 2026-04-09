# Report Factory Daily Reviewer

Report Factory 日报生成 Agent —— 每晚自动评审当日卡片并发送邮件日报。

## 功能特性

- 🕡 **定时执行**：每天 18:30 自动扫描、评审、发送日报
- 📊 **批量评审**：对当日所有卡片进行 A/B/C 质量分级
- 📝 **50字摘要**：自动提取每张卡片的核心洞察
- 📧 **邮件推送**：美观的 HTML 格式日报
- 🏷️ **领域统计**：按 EAI/AIH/MM/COG/AGT 分布统计

## 安装

### 1. 复制 Skill 到 OpenClaw

```bash
cp -r report-factory-daily-reviewer ~/.claude/skills/
```

### 2. 安装依赖

```bash
pip install pyyaml
```

### 3. 配置

**方式一：交互式配置（推荐）**

```bash
# 在 OpenClaw 中运行
/daily_report --setup
```

按提示输入：
- Obsidian Vault 路径
- 邮箱 SMTP 配置
- 日报发送时间

**方式二：手动配置**

1. 复制配置模板：
```bash
cp config.template.json ~/.report-factory/daily-reviewer-config.json
```

2. 编辑 `~/.report-factory/daily-reviewer-config.json`，填入你的配置：

```json
{
  "vault_path": "/path/to/your/Obsidian/Vault",
  "email": {
    "to": "your-email@example.com",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password"  // 不是登录密码，是授权码
  }
}
```

### 4. 设置定时任务

**macOS (launchd)**：
```bash
cp com.report-factory.daily-reviewer.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.report-factory.daily-reviewer.plist
```

**Linux (cron)**：
```bash
# crontab -e
30 18 * * * python3 ~/.report-factory/scripts/daily_reviewer.py
```

**Windows (Task Scheduler)**：
```powershell
# 以管理员身份运行 PowerShell
$action = New-ScheduledTaskAction -Execute "python3" -Argument "$env:USERPROFILE\.report-factory\scripts\daily_reviewer.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 18:30
Register-ScheduledTask -TaskName "ReportFactory-DailyReport" -Action $action -Trigger $trigger
```

## 使用

### 手动执行

```bash
# 在 OpenClaw 中
/daily_report              # 生成并发送今日日报
/daily_report --preview    # 预览但不发送邮件
/daily_report --setup      # 重新配置
```

### 邮件配置说明

**Gmail**：
- SMTP: smtp.gmail.com:587
- 密码：需要使用「应用专用密码」（不是 Gmail 登录密码）
- 开启：两步验证 → 应用专用密码

**163邮箱**：
- SMTP: smtp.163.com:465 (SSL)
- 密码：需要使用「授权码」（不是邮箱登录密码）
- 获取：设置 → POP3/SMTP/IMAP → 开启授权码

**QQ邮箱**：
- SMTP: smtp.qq.com:465 (SSL)
- 密码：需要使用「授权码」

## 日报内容示例

```
# Report Factory 日报 —— 2026-04-02

## 今日概览
- 生成卡片总数: 5 张
- Evidence: 4 张 | Arguments: 1 张
- 质量评级: A级 3 张 | B级 1 张 | C级 1 张

## 领域分布
| 领域 | 数量 | 占比 |
|------|------|------|
| EAI  | 2    | 40%  |
| AIH  | 2    | 40%  |
| MM   | 1    | 20%  |

## 卡片列表
### ✅ 优质卡片 (A级)
1. [EAI-E] Spirit v1.5: 首个超越 π0.5 的中文开源 VLA
   - 摘要: 首个超越π0.5的中文开源VLA，推理延迟150ms...

### ⚠️ 合格卡片 (B级)
...

### ❌ 待改进卡片 (C级)
...
```

## 与 report-factory 的协作

```
report-factory (收割制卡)
        ↓
   生成 .md 卡片
        ↓
daily-reviewer (定时扫描)
        ↓
   评审 + 生成日报
        ↓
   发送邮件
```

## 安全提示

⚠️ **重要**：`config.json` 包含邮箱密码/授权码，**切勿提交到 GitHub**！

本仓库已配置 `.gitignore` 排除敏感文件：
- `daily-reviewer-config.json`
- `email-config.json`
- `config.json`

## 配置参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `vault_path` | Obsidian Vault 路径 | `~/Obsidian/Vault` |
| `email.to` | 接收日报的邮箱 | `your@email.com` |
| `email.smtp_host` | SMTP 服务器 | `smtp.gmail.com` |
| `email.smtp_port` | SMTP 端口 | `587` |
| `email.username` | 发送邮箱 | `sender@gmail.com` |
| `email.password` | 授权码/应用密码 | `xxxx xxxx xxxx xxxx` |
| `schedule.time` | 发送时间 | `18:30` |

## 许可证

MIT License
