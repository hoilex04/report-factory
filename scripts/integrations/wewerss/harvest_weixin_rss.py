#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信 RSS 文章收割脚本
从 wewerss 提供的 RSS feed 提取最近 N 天的相关文章并输出待处理列表。

用法:
    python harvest_weixin_rss.py

依赖:
    - requests: pip install requests
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

# ==================== 配置区（请自行修改） ====================
# wewerss 服务地址，默认本地 4000 端口
WEWE_RSS_ENDPOINT = os.environ.get("WEWE_RSS_ENDPOINT", "http://localhost:4000/feeds/all.atom")

# 输出目录，用于保存待处理文章列表
OUTPUT_DIR = Path(os.environ.get("REPORT_FACTORY_OUTPUT_DIR", "."))

# 关联领域的关键词词典：key 为领域代码，value 为关键词列表
DOMAIN_KEYWORDS = {
    "EAI": [
        "机器人", "Robot", "具身", "Embodied", "VLA", "Manipulator",
        "操作", "抓取", "世界模型", "World Model", "强化学习", "RL",
        "仿真", "Simulation", "跨具身", "策略学习"
    ],
    "AIH": [
        "NPU", "芯片", "Chip", "AI PC", "算力", "Hardware",
        "端侧", "推理", "Inference", "显存", "GPU", "加速",
        "忆阻器", "ASIC", "存算一体"
    ],
    "MM": [
        "多模态", "Multimodal", "视觉语言", "Vision-Language",
        "CLIP", "图文", "Audio", "视频生成"
    ],
    "COG": [
        "推理", "Reasoning", "规划", "Planning", "记忆", "Memory",
        "知识图谱", "Knowledge Graph", "思维链", "CoT"
    ],
    "AGT": [
        "智能体", "Agent", "多智能体", "Multi-Agent", "工具调用",
        "Tool Use", "ReAct", "Function Calling"
    ],
}

# 采集最近 N 天的文章
HARVEST_DAYS = 7

# ==================== 工具函数 ====================

def fetch_rss_feed():
    """获取 RSS feed"""
    try:
        import requests
        response = requests.get(WEWE_RSS_ENDPOINT, timeout=10)
        response.raise_for_status()
        return response.text
    except ImportError:
        print("缺少 requests 依赖，请运行: pip install requests")
        return None
    except Exception as e:
        print(f"获取 RSS feed 失败: {e}")
        return None


def parse_rss_feed(rss_content):
    """解析 Atom RSS feed"""
    articles = []
    try:
        root = ET.fromstring(rss_content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        for entry in root.findall("atom:entry", ns):
            title_elem = entry.find("atom:title", ns)
            link_elem = entry.find("atom:link", ns)
            updated_elem = entry.find("atom:updated", ns)

            if title_elem is not None and link_elem is not None and updated_elem is not None:
                title_text = title_elem.text or ""
                if "![CDATA[" in title_text:
                    m = re.search(r"\[CDATA\[(.*?)\]\]", title_text)
                    if m:
                        title_text = m.group(1)

                articles.append({
                    "title": title_text.strip(),
                    "url": link_elem.get("href", ""),
                    "updated": updated_elem.text or "",
                })
    except Exception as e:
        print(f"解析 RSS 失败: {e}")

    return articles


def filter_recent_articles(articles, days=HARVEST_DAYS):
    """筛选最近 N 天的文章"""
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_articles = []

    for article in articles:
        try:
            updated_date = datetime.fromisoformat(article["updated"].replace("Z", "+00:00"))
            if updated_date.replace(tzinfo=None) >= cutoff_date:
                recent_articles.append(article)
        except Exception as e:
            print(f"日期解析失败: {article['title']} - {e}")

    return recent_articles


def classify_article(title):
    """根据标题关键词判断文章所属领域"""
    title_lower = title.lower()
    matched_domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in title_lower:
                matched_domains.append(domain)
                break
    return matched_domains


def main():
    print("=" * 60)
    print("微信 RSS 文章收割开始")
    print(f"数据源: {WEWE_RSS_ENDPOINT}")
    print("=" * 60)

    # 1. 获取并解析 RSS
    print("\n[1/3] 获取并解析 RSS feed...")
    rss_content = fetch_rss_feed()
    if not rss_content:
        print("无法获取 RSS feed，退出")
        return

    articles = parse_rss_feed(rss_content)
    print(f"解析到 {len(articles)} 篇文章")

    # 2. 按时间过滤
    print(f"\n[2/3] 筛选最近 {HARVEST_DAYS} 天的文章...")
    recent_articles = filter_recent_articles(articles, days=HARVEST_DAYS)
    print(f"最近 {HARVEST_DAYS} 天有 {len(recent_articles)} 篇文章")

    # 3. 领域分类
    print("\n[3/3] 领域分类与输出...")
    classified = []
    for article in recent_articles:
        domains = classify_article(article["title"])
        if domains:
            article["domains"] = domains
            classified.append(article)
            print(f"  [{'/'.join(domains)}] {article['title']}")

    print(f"\n共找到 {len(classified)} 篇相关文章")

    # 保存待处理列表
    output_file = OUTPUT_DIR / "pending_weixin_articles.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(classified, f, ensure_ascii=False, indent=2)

    print(f"\n待处理文章已保存到: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
