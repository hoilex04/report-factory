---
name: report-factory-daily-reviewer
description: Report Factory 日报生成 Agent —— 每晚自动评审当日卡片并发送邮件日报
user-invocable: true
triggers:
  - daily_report
  - "日报"
  - "卡片日报"
  - "review daily"
version: 1.0.0
parent_skill: report-factory
tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Report Factory Daily Reviewer —— 卡片日报生成器

> 自动扫描当日生成的知识卡片，执行质量评审，生成摘要，并发送邮件日报。

## 前置检查

执行前必须确认以下配置已设置：

1. **检查配置文件是否存在**：
   ```bash
   cat ~/.report-factory/daily-reviewer-config.json
   ```

2. **如果配置不存在，引导用户初始化**：
   - 询问 Obsidian Vault 路径
   - 询问接收邮箱地址
   - 询问 SMTP 配置（或使用默认）
   - 保存配置

## 执行流程

### Step 1: 加载配置

读取 `~/.report-factory/daily-reviewer-config.json`：

```json
{
  "vault_path": "/path/to/Obsidian/Vault",
  "cards_path": "/path/to/Obsidian/Vault/Cards",
  "evidence_path": "/path/to/Obsidian/Vault/Cards/Evidence",
  "arguments_path": "/path/to/Obsidian/Vault/Cards/Arguments",
  "email": {
    "to": "your-email@example.com",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "sender@gmail.com",
    "password": "app-password"
  },
  "review_criteria": {
    "min_quantitative_data": 2,
    "grade_threshold_a": 5,
    "grade_threshold_b": 3
  }
}
```

### Step 2: 扫描当日卡片

使用 Glob 查找当天创建的 `.md` 文件：

```python
# 查找 Evidence 和 Arguments 目录下的所有 .md 文件
evidence_files = glob(f"{config['evidence_path']}/**/*.md", recursive=True)
arguments_files = glob(f"{config['arguments_path']}/**/*.md", recursive=True)

# 过滤出今天创建的文件
today = datetime.now().date()
today_cards = []

for file_path in evidence_files + arguments_files:
    file_stat = os.stat(file_path)
    file_date = datetime.fromtimestamp(file_stat.st_ctime).date()
    if file_date == today:
        today_cards.append(file_path)
```

### Step 3: 评审每张卡片

对每张卡片执行质量检查：

#### 3.1 读取卡片内容

```python
with open(card_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

#### 3.2 解析 Frontmatter

提取 YAML frontmatter：

```python
import re
import yaml

# 提取 frontmatter
frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
if frontmatter_match:
    frontmatter = yaml.safe_load(frontmatter_match.group(1))
else:
    frontmatter = {}
```

#### 3.3 执行 5 点质量检查

**Check 1: 准入门槛**
- 检查是否有定量数据（正则匹配数字+单位）
- 检查是否有 source 字段
- 检查内容长度（>500 字符为合格）

**Check 2: 标题规范**
- 检查文件名格式：`[DOMAIN] - [Topic]: [Insight] - [UID].md`
- 检查标题长度

**Check 3: 定量数据**
- Evidence 卡：检查是否有 ≥2 条带单位的数据
- Arguments 卡：检查是否有关联的 Evidence 卡片

**Check 4: 标签格式**
- 检查 tags 是否有空格或特殊字符
- 检查是否有重复标签

**Check 5: 来源有效性**
- 检查 source URL 格式是否有效
- 检查是否为原始来源（非汇总页）

#### 3.4 生成分级

```python
def grade_card(checks):
    passed = sum([1 for c in checks.values() if c['passed']])

    if passed >= 5:
        return 'A', '优质'
    elif passed >= 3:
        return 'B', '合格'
    else:
        return 'C', '待改进'
```

### Step 4: 生成 50 字摘要

提取核心内容生成摘要：

```python
def generate_summary(content, frontmatter):
    # 提取 abstract 或核心段落
    abstract_match = re.search(r'> \[!abstract\].*?\n> (.*?)(?:\n|$)', content)
    if abstract_match:
        summary = abstract_match.group(1)
    else:
        # 提取第一段非空文本
        text_match = re.search(r'# .*\n\n(.{50,200})', content)
        summary = text_match.group(1) if text_match else ""

    # 截断到 50 字
    summary = summary[:50] + "..." if len(summary) > 50 else summary

    return summary
```

### Step 5: 生成日报 Markdown

```markdown
# Report Factory 日报 —— {{YYYY年MM月DD日}}

## 今日概览

- **生成卡片总数**: {{total}} 张
- **Evidence**: {{evidence_count}} 张 | **Arguments**: {{arguments_count}} 张
- **质量评级**: A级 {{grade_a}} 张 | B级 {{grade_b}} 张 | C级 {{grade_c}} 张

## 领域分布

{{domain_distribution}}

## 卡片列表

### ✅ 优质卡片 (A级)

{{#each grade_a_cards}}
1. **[{{domain}}-{{type}}]** {{title}}
   - 摘要: {{summary}}
   - UID: {{uid}}
   - 来源: {{source}}

{{/each}}

### ⚠️ 合格卡片 (B级)

{{#each grade_b_cards}}
1. **[{{domain}}-{{type}}]** {{title}}
   - 摘要: {{summary}}
   - UID: {{uid}}
   - 改进建议: {{improvement}}

{{/each}}

### ❌ 待改进卡片 (C级)

{{#each grade_c_cards}}
1. **[{{domain}}-{{type}}]** {{title}}
   - 摘要: {{summary}}
   - UID: {{uid}}
   - 问题: {{issues}}

{{/each}}

## 行动建议

{{action_items}}

---
*Report Factory Daily Reviewer | 自动生成于 {{datetime}}*
```

### Step 6: 发送邮件

使用 Python 发送 HTML 邮件：

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_daily_report(config, report_md, stats):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"[RF日报] {datetime.now().strftime('%Y-%m-%d')} 生成 {stats['total']} 张卡片"
    msg['From'] = config['email']['username']
    msg['To'] = config['email']['to']

    # 转换为 HTML
    html_content = markdown_to_html(report_md)

    msg.attach(MIMEText(report_md, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 发送
    with smtplib.SMTP(config['email']['smtp_host'], config['email']['smtp_port']) as server:
        server.starttls()
        server.login(config['email']['username'], config['email']['password'])
        server.send_message(msg)

    return True
```

## 具体实现脚本

创建 `~/.report-factory/scripts/daily_reviewer.py`：

```python
#!/usr/bin/env python3
"""
Report Factory Daily Reviewer
自动评审当日卡片并发送邮件日报
"""

import os
import sys
import json
import re
import yaml
from datetime import datetime, date
from pathlib import Path
from glob import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DailyReviewer:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.today = date.today()
        self.cards = []

    def scan_today_cards(self):
        """扫描今日生成的卡片"""
        paths = [
            self.config['evidence_path'],
            self.config['arguments_path']
        ]

        for base_path in paths:
            if not os.path.exists(base_path):
                continue

            for md_file in glob(f"{base_path}/**/*.md", recursive=True):
                stat = os.stat(md_file)
                file_date = date.fromtimestamp(stat.st_ctime)

                if file_date == self.today:
                    self.cards.append({
                        'path': md_file,
                        'type': 'Evidence' if 'Evidence' in md_file else 'Arguments'
                    })

        return len(self.cards)

    def review_card(self, card_path):
        """评审单张卡片"""
        with open(card_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析 frontmatter
        frontmatter = {}
        content_body = content
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            try:
                frontmatter = yaml.safe_load(fm_match.group(1))
                content_body = content[fm_match.end():]
            except:
                pass

        # 执行质量检查
        checks = {
            'entry_threshold': self._check_entry_threshold(content, frontmatter),
            'title_format': self._check_title_format(card_path, frontmatter),
            'quantitative_data': self._check_quantitative_data(content, frontmatter),
            'tags_format': self._check_tags_format(frontmatter),
            'source_validity': self._check_source_validity(frontmatter)
        }

        # 计算等级
        passed = sum(1 for c in checks.values() if c['passed'])
        if passed >= 5:
            grade = 'A'
        elif passed >= 3:
            grade = 'B'
        else:
            grade = 'C'

        # 生成摘要
        summary = self._generate_summary(content_body, frontmatter)

        return {
            'path': card_path,
            'filename': os.path.basename(card_path),
            'type': 'Evidence' if 'Evidence' in card_path else 'Arguments',
            'domain': frontmatter.get('domain', 'Unknown'),
            'uid': frontmatter.get('uid', 'N/A'),
            'title': frontmatter.get('title', self._extract_title(content_body)),
            'source': frontmatter.get('source', 'N/A'),
            'checks': checks,
            'grade': grade,
            'summary': summary,
            'issues': [c['message'] for c in checks.values() if not c['passed']]
        }

    def _check_entry_threshold(self, content, fm):
        """检查准入门槛"""
        has_data = bool(re.search(r'\d+\s*(ms|fps|Hz|%|MB|GB|TOPS|params)', content))
        has_source = bool(fm.get('source'))
        is_long_enough = len(content) > 500

        passed = (has_data or has_source) and is_long_enough
        return {
            'passed': passed,
            'message': '' if passed else '内容过短或缺乏数据/来源'
        }

    def _check_title_format(self, path, fm):
        """检查标题格式"""
        filename = os.path.basename(path)
        pattern = r'^\[\w+\] - .+: .+ - \w+-\w-\d{8}-\d{2}\.md$'
        passed = bool(re.match(pattern, filename))
        return {
            'passed': passed,
            'message': '' if passed else '文件名格式不符合规范'
        }

    def _check_quantitative_data(self, content, fm):
        """检查定量数据"""
        if fm.get('card_type') == 'Arguments':
            # Arguments 卡检查是否有关联 Evidence
            has_links = bool(re.search(r'\[\[\w+-\w-\d{8}-\d{2}\]\]', content))
            passed = has_links
            message = '' if passed else '缺少关联的 Evidence 卡片'
        else:
            # Evidence 卡检查数据条数
            data_count = len(re.findall(r'\*\*[\w\s]+\*\*:?\s*\d+', content))
            passed = data_count >= 2
            message = '' if passed else f'定量数据不足 ({data_count}/2)'

        return {'passed': passed, 'message': message}

    def _check_tags_format(self, fm):
        """检查标签格式"""
        tags = fm.get('tags', [])
        if not tags:
            return {'passed': True, 'message': ''}

        invalid_chars = r'[#%./\\,:*?"<>| ]'
        has_invalid = any(re.search(invalid_chars, str(tag)) for tag in tags)

        return {
            'passed': not has_invalid,
            'message': '' if not has_invalid else 'Tags 包含空格或特殊字符'
        }

    def _check_source_validity(self, fm):
        """检查来源有效性"""
        source = fm.get('source', '')
        if not source:
            return {'passed': False, 'message': '缺少 source 字段'}

        # 检查是否为有效 URL
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        passed = bool(re.match(url_pattern, source))

        return {
            'passed': passed,
            'message': '' if passed else 'Source URL 格式无效'
        }

    def _generate_summary(self, content, fm):
        """生成 50 字摘要"""
        # 尝试提取 abstract
        abstract_match = re.search(r'> \[!abstract\].*?\n> (.+?)(?:\n|$)', content, re.DOTALL)
        if abstract_match:
            summary = abstract_match.group(1).strip()
            # 清理 markdown 标记
            summary = re.sub(r'[#\*\[\]]', '', summary)
        else:
            # 提取第一段
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
            summary = lines[0] if lines else "无摘要"

        # 截断到 50 字
        if len(summary) > 50:
            summary = summary[:47] + "..."

        return summary

    def _extract_title(self, content):
        """从内容提取标题"""
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        return match.group(1) if match else "未命名"

    def generate_report(self, reviews):
        """生成日报"""
        stats = {
            'total': len(reviews),
            'evidence': len([r for r in reviews if r['type'] == 'Evidence']),
            'arguments': len([r for r in reviews if r['type'] == 'Arguments']),
            'grade_a': len([r for r in reviews if r['grade'] == 'A']),
            'grade_b': len([r for r in reviews if r['grade'] == 'B']),
            'grade_c': len([r for r in reviews if r['grade'] == 'C'])
        }

        # 按领域统计
        domains = {}
        for r in reviews:
            d = r['domain']
            domains[d] = domains.get(d, 0) + 1

        # 生成报告
        report = f"""# Report Factory 日报 —— {self.today.strftime('%Y年%m月%d日')}

## 今日概览

- **生成卡片总数**: {stats['total']} 张
- **Evidence**: {stats['evidence']} 张 | **Arguments**: {stats['arguments']} 张
- **质量评级**: A级 {stats['grade_a']} 张 | B级 {stats['grade_b']} 张 | C级 {stats['grade_c']} 张

## 领域分布

| 领域 | 数量 | 占比 |
|------|------|------|
"""

        for domain, count in sorted(domains.items(), key=lambda x: -x[1]):
            pct = count / stats['total'] * 100
            report += f"| {domain} | {count} | {pct:.0f}% |\n"

        # 分级列表
        for grade, label, emoji in [('A', '优质', '✅'), ('B', '合格', '⚠️'), ('C', '待改进', '❌')]:
            cards = [r for r in reviews if r['grade'] == grade]
            if cards:
                report += f"\n### {emoji} {label}卡片 ({grade}级)\n\n"
                for i, c in enumerate(cards, 1):
                    report += f"{i}. **[{c['domain']}-{c['type'][0]}]** {c['title']}\n"
                    report += f"   - 摘要: {c['summary']}\n"
                    report += f"   - UID: {c['uid']}\n"
                    if c['issues']:
                        report += f"   - 注意: {'; '.join(c['issues'])}\n"
                    report += "\n"

        # 行动建议
        report += "## 行动建议\n\n"
        if stats['grade_c'] > 0:
            report += f"- 有 {stats['grade_c']} 张卡片质量较低，建议手动复查\n"
        if stats['grade_b'] > 0:
            report += f"- 有 {stats['grade_b']} 张卡片有改进空间\n"
        if stats['total'] == 0:
            report += "- 今日未生成新卡片\n"

        report += f"\n---\n*Report Factory Daily Reviewer | 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*"

        return report, stats

    def send_email(self, report, stats):
        """发送邮件"""
        email_cfg = self.config['email']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[RF日报] {self.today.strftime('%Y-%m-%d')} 生成 {stats['total']} 张卡片"
        msg['From'] = email_cfg['username']
        msg['To'] = email_cfg['to']

        # 简化版 HTML
        html = f"""<html><body>
<h2>Report Factory 日报 —— {self.today.strftime('%Y年%m月%d日')}</h2>
<p>今日生成 <strong>{stats['total']}</strong> 张卡片</p>
<p>A级: {stats['grade_a']} | B级: {stats['grade_b']} | C级: {stats['grade_c']}</p>
<hr/>
<pre>{report}</pre>
</body></html>"""

        msg.attach(MIMEText(report, 'plain', 'utf-8'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        with smtplib.SMTP(email_cfg['smtp_host'], email_cfg['smtp_port']) as server:
            server.starttls()
            server.login(email_cfg['username'], email_cfg['password'])
            server.send_message(msg)

        return True

    def run(self):
        """主流程"""
        # 扫描卡片
        count = self.scan_today_cards()
        print(f"发现 {count} 张今日卡片")

        if count == 0:
            print("今日无新卡片，跳过日报生成")
            return

        # 评审
        reviews = []
        for card in self.cards:
            review = self.review_card(card['path'])
            reviews.append(review)
            print(f"评审完成: {review['filename']} -> {review['grade']}")

        # 生成报告
        report, stats = self.generate_report(reviews)

        # 保存报告
        report_path = f"{self.config['vault_path']}/Outputs/daily-report-{self.today.strftime('%Y%m%d')}.md"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存: {report_path}")

        # 发送邮件
        self.send_email(report, stats)
        print("邮件已发送")

if __name__ == '__main__':
    config_path = os.path.expanduser('~/.report-factory/daily-reviewer-config.json')

    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        print("请先运行初始化: /daily_report --setup")
        sys.exit(1)

    reviewer = DailyReviewer(config_path)
    reviewer.run()
```

## 初始化脚本

创建 `~/.report-factory/scripts/setup_daily_reviewer.py`：

```python
#!/usr/bin/env python3
"""初始化 Daily Reviewer 配置"""

import json
import os
from getpass import getpass

def setup():
    print("=== Report Factory Daily Reviewer 初始化 ===\n")

    config = {}

    # Vault 路径
    config['vault_path'] = input("Obsidian Vault 路径: ").strip()
    config['cards_path'] = f"{config['vault_path']}/Cards"
    config['evidence_path'] = f"{config['cards_path']}/Evidence"
    config['arguments_path'] = f"{config['cards_path']}/Arguments"

    # 邮件配置
    print("\n--- 邮件配置 ---")
    config['email'] = {
        'to': input("接收邮箱: ").strip(),
        'smtp_host': input("SMTP 服务器 [smtp.gmail.com]: ").strip() or "smtp.gmail.com",
        'smtp_port': int(input("SMTP 端口 [587]: ").strip() or "587"),
        'username': input("发送邮箱: ").strip(),
        'password': getpass("邮箱密码/App Password: ")
    }

    # 评审标准
    config['review_criteria'] = {
        'min_quantitative_data': 2,
        'grade_threshold_a': 5,
        'grade_threshold_b': 3
    }

    # 保存配置
    config_dir = os.path.expanduser('~/.report-factory')
    os.makedirs(config_dir, exist_ok=True)

    config_path = f"{config_dir}/daily-reviewer-config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"\n配置已保存: {config_path}")
    print("可以运行: /daily_report")

if __name__ == '__main__':
    setup()
```

## 定时任务配置

### macOS (launchd)

创建 `~/Library/LaunchAgents/com.report-factory.daily-reviewer.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.report-factory.daily-reviewer</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>~/.report-factory/scripts/daily_reviewer.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
</dict>
</plist>
```

加载：
```bash
launchctl load ~/Library/LaunchAgents/com.report-factory.daily-reviewer.plist
```

### Linux (cron)

```bash
# 编辑 crontab
crontab -e

# 添加行
30 18 * * * python3 ~/.report-factory/scripts/daily_reviewer.py
```

### Windows (Task Scheduler)

```powershell
$action = New-ScheduledTaskAction -Execute "python3" -Argument "$env:USERPROFILE\.report-factory\scripts\daily_reviewer.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 18:30
Register-ScheduledTask -TaskName "ReportFactory-DailyReport" -Action $action -Trigger $trigger
```

## 使用方式

### 1. 初始化配置

```bash
/daily_report --setup
```

这会运行 setup 脚本，引导输入配置信息。

### 2. 手动执行日报

```bash
/daily_report           # 生成并发送今日日报
/daily_report --preview # 预览但不发送
```

### 3. 自动定时执行

按上述方式配置定时任务，每天 18:30 自动执行。

## 与 report-factory 的协作

在 report-factory 生成卡片后，可以主动触发日报更新：

```python
# 在 report-factory 的入库步骤后添加
subprocess.run(['python3', '~/.report-factory/scripts/daily_reviewer.py'])
```

或者仅更新待办列表，等 18:30 统一处理。

---

**这是一个完整的、可独立运行的 OpenClaw Skill。**
