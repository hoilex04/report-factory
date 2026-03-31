# WeWe RSS Integration for Report Factory

本目录包含与 [wewerss](https://github.com/cooderl/wewe-rss) 集成的辅助脚本，用于从微信 RSS Feed 自动获取、筛选并导入文章到 Report Factory 的工作流。

## 环境要求

```bash
pip install requests
# 可选：智能降级方案需要
pip install playwright
playwright install chromium
```

## 配置环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `WEWE_RSS_ENDPOINT` | wewerss Atom Feed 地址 | `http://localhost:4000/feeds/all.atom` |
| `REPORT_FACTORY_WORKSPACE` | 项目工作区路径 | `.` |
| `REPORT_FACTORY_OBSIDIAN_ROOT` | Obsidian 库根目录 | `~/Obsidian` |
| `REPORT_FACTORY_INBOX_PATH` | Inbox.md 路径 | `~/Obsidian/Atomic-card/Inbox.md` |
| `REPORT_FACTORY_OUTPUT_DIR` | 输出目录 | `.` |

## 脚本说明

### 1. `fetch_weixin.py`
基础版微信文章抓取器，仅使用 `urllib`，无额外依赖。

```bash
python fetch_weixin.py <URL>
```

### 2. `fetch_weixin_smart.py`
智能降级版。优先使用轻量级 HTTP，失败时降级到 Playwright 浏览器渲染。

```bash
python fetch_weixin_smart.py <URL>
```

### 3. `harvest_weixin_rss.py`
从 wewerss 获取最近 7 天的文章，按领域关键词分类，输出 `pending_weixin_articles.json`。

```bash
python harvest_weixin_rss.py
```

### 4. `morning_harvest.py`
每日早间收割脚本：自动抓取 arXiv 论文，去重后写入 Inbox.md，并提示用户手动补充微信/飞书链接。

```bash
python morning_harvest.py
```

### 5. `inbox_harvester.py`
提取 Inbox.md 中的待处理链接，供 Claude / AI Agent 批量制卡使用。

```bash
python inbox_harvester.py
```

## 工作流建议

1. 部署并运行 [wewerss](https://github.com/cooderl/wewe-rss)，确保本地服务可访问（如 `http://localhost:4000`）。
2. 运行 `morning_harvest.py` 获取 arXiv 新论文。
3. 运行 `harvest_weixin_rss.py` 获取微信文章并手动粘贴到 Inbox.md。
4. 在 Claude 中执行 `\u6536\u5272 Inbox` 或运行 `inbox_harvester.py` 后交给 AI 批量生成 Evidence 卡片。。
