#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信 RSS 文章收割脚本（带质量筛选）
从 wewerss 提供的 RSS feed 提取高质量文章，过滤短讯/融资快讯

用法:
    python harvest_weixin_rss.py

依赖:
    - requests: pip install requests
"""

import json
import os
import re
import ssl
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

# ==================== 配置区 ====================
# wewerss 服务地址
WEWE_RSS_ENDPOINT = os.environ.get("WEWE_RSS_ENDPOINT", "http://localhost:4000/feeds/all.atom")

# 输出目录
DEFAULT_OUTPUT_DIR = "D:\\003_Resource\\04_Obsidian\\Atomic-card"
OUTPUT_DIR = Path(os.environ.get("REPORT_FACTORY_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))

# 采集最近 N 天的文章
HARVEST_DAYS = 7

# 质量筛选配置
QUALITY_CONFIG = {
    # 标题过滤 - 包含这些关键词的文章会被标记为低质量
    "low_quality_title_keywords": [
        "速递｜", "融资", "获投", "估值", "IPO", "上市",
        "专访", "对话", "思考", "观点", "复盘",
        "饭局", "往事", "历史", "回顾"
    ],
    # 高质量标题关键词 - 包含这些词的文章优先保留
    "high_quality_title_keywords": [
        "发布", "提出", "实现", "突破", "攻克", "解决",
        "开源", "实测", "评测", "对比", "分析",
        "技术", "模型", "算法", "架构", "系统"
    ],
    # 内容质量阈值
    "min_content_length": 800,  # 最少字符数
    "min_data_points": 1,       # 最少数据点数量
}

# 领域关键词
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
        "Tool Use", "ReAct", "Function Calling", "MCP"
    ],
}


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
            id_elem = entry.find("atom:id", ns)

            if title_elem is not None and link_elem is not None and updated_elem is not None:
                title_text = title_elem.text or ""
                if "![CDATA[" in title_text:
                    m = re.search(r"\[CDATA\[(.*?)\]\]", title_text)
                    if m:
                        title_text = m.group(1)

                # 提取文章ID
                article_id = ""
                if id_elem is not None:
                    id_text = id_elem.text or ""
                    # 从 URL 中提取 ID
                    m = re.search(r"/s/([a-zA-Z0-9_-]+)", id_text)
                    if m:
                        article_id = m.group(1)

                articles.append({
                    "title": title_text.strip(),
                    "url": link_elem.get("href", ""),
                    "article_id": article_id,
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


def assess_title_quality(title):
    """
    评估标题质量
    返回: (quality_score, reason)
    quality_score: 0-10, 低于5分的文章会被过滤
    """
    score = 5  # 基础分
    reasons = []

    # 检查低质量关键词
    for kw in QUALITY_CONFIG["low_quality_title_keywords"]:
        if kw in title:
            score -= 2
            reasons.append(f"含低质量关键词'{kw}'")

    # 检查高质量关键词
    for kw in QUALITY_CONFIG["high_quality_title_keywords"]:
        if kw in title:
            score += 1
            reasons.append(f"含高质量关键词'{kw}'")

    # 标题长度评估
    if len(title) < 15:
        score -= 1
        reasons.append("标题过短")
    elif len(title) > 40:
        score += 1
        reasons.append("标题信息丰富")

    # 特殊标记
    if "实测" in title or "深度" in title:
        score += 2
        reasons.append("深度/实测内容")

    if "专访" in title or "对话" in title:
        score -= 1  # 专访通常是软广或观点，技术信息较少
        reasons.append("专访/对话类型")

    score = max(0, min(10, score))  # 限制在0-10之间

    reason_str = "; ".join(reasons) if reasons else "普通标题"
    return score, reason_str


def fetch_article_preview(article_id):
    """
    获取文章前500字用于质量评估
    返回: (content_preview, content_length) 或 (None, 0)
    """
    if not article_id:
        return None, 0

    url = f"https://mp.weixin.qq.com/s/{article_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://mp.weixin.qq.com/',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            html = response.read().decode('utf-8')

        # 提取内容
        content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
        if content_match:
            content_html = content_match.group(1)
            content = re.sub(r'<[^>]+>', ' ', content_html)
            content = re.sub(r'\s+', ' ', content).strip()
            return content[:500], len(content)

        return None, 0
    except Exception as e:
        return None, 0


def count_data_points(content):
    """统计内容中的数据点数量"""
    if not content:
        return 0

    data_patterns = [
        r'\d+[%％]',
        r'\d+[万亿亿美元￥]',
        r'\d+\s*(?:ms|毫秒|秒|分钟|小时)',
        r'(?:提升|下降|增长|减少|降低|增加).*?\d+',
        r'\d+\.?\d*\s*(?:TB|GB|MB|亿|万)',
    ]

    count = 0
    for pattern in data_patterns:
        matches = re.findall(pattern, content)
        count += len(matches)

    return count


def main():
    print("=" * 70)
    print("微信 RSS 文章收割（质量筛选版）")
    print(f"数据源: {WEWE_RSS_ENDPOINT}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"质量阈值: 标题得分≥5, 内容长度≥{QUALITY_CONFIG['min_content_length']}")
    print("=" * 70)

    # 1. 获取并解析 RSS
    print("\n[1/4] 获取并解析 RSS feed...")
    rss_content = fetch_rss_feed()
    if not rss_content:
        print("无法获取 RSS feed，退出")
        return

    articles = parse_rss_feed(rss_content)
    print(f"解析到 {len(articles)} 篇文章")

    # 2. 按时间过滤
    print(f"\n[2/4] 筛选最近 {HARVEST_DAYS} 天的文章...")
    recent_articles = filter_recent_articles(articles, days=HARVEST_DAYS)
    print(f"最近 {HARVEST_DAYS} 天有 {len(recent_articles)} 篇文章")

    # 3. 领域分类 + 标题质量评估
    print("\n[3/4] 领域分类与标题质量评估...")
    classified = []
    filtered = []

    for article in recent_articles:
        domains = classify_article(article["title"])
        if not domains:
            continue

        # 评估标题质量
        quality_score, quality_reason = assess_title_quality(article["title"])
        article["domains"] = domains
        article["quality_score"] = quality_score
        article["quality_reason"] = quality_reason

        if quality_score >= 5:
            classified.append(article)
            print(f"  [✓ 质量分:{quality_score}] [{'/'.join(domains)}] {article['title'][:50]}...")
        else:
            filtered.append(article)
            print(f"  [✗ 质量分:{quality_score} 已过滤] {article['title'][:50]}...")
            print(f"      原因: {quality_reason}")

    print(f"\n标题筛选: {len(classified)} 篇通过, {len(filtered)} 篇过滤")

    # 4. 内容质量预检
    print("\n[4/4] 内容质量预检（抓取预览）...")
    high_quality = []
    low_quality = []

    for article in classified:
        preview, length = fetch_article_preview(article.get("article_id", ""))

        if preview:
            data_points = count_data_points(preview)
            article["content_length"] = length
            article["data_points_preview"] = data_points

            # 质量判断
            if length >= QUALITY_CONFIG["min_content_length"]:
                high_quality.append(article)
                print(f"  [✓] {article['title'][:40]}... 长度:{length} 数据点:{data_points}")
            else:
                article["filter_reason"] = f"内容过短({length}字符)"
                low_quality.append(article)
                print(f"  [✗] {article['title'][:40]}... 长度:{length} 已过滤")
        else:
            # 无法抓取内容，但标题质量高，保留待人工确认
            article["content_length"] = 0
            article["data_points_preview"] = 0
            article["note"] = "内容预览抓取失败，需人工确认"
            high_quality.append(article)
            print(f"  [?] {article['title'][:40]}... 内容抓取失败，保留待确认")

    print(f"\n内容筛选: {len(high_quality)} 篇高质量, {len(low_quality)} 篇过滤")

    # 5. 输出结果
    print("\n" + "=" * 70)
    print("处理结果汇总")
    print("=" * 70)
    print(f"\n高质量文章（{len(high_quality)} 篇）:")
    for article in high_quality:
        print(f"  [{'/'.join(article['domains'])}] {article['title']}")

    if low_quality:
        print(f"\n因内容过短过滤（{len(low_quality)} 篇）:")
        for article in low_quality:
            print(f"  {article['title'][:50]}... ({article['filter_reason']})")

    if filtered:
        print(f"\n因标题质量低过滤（{len(filtered)} 篇）:")
        for article in filtered:
            print(f"  {article['title'][:50]}... (得分:{article['quality_score']})")

    # 保存高质量文章列表
    output_file = OUTPUT_DIR / "pending_weixin_articles.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(high_quality, f, ensure_ascii=False, indent=2)

    # 保存过滤报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_rss": len(articles),
            "recent": len(recent_articles),
            "high_quality": len(high_quality),
            "filtered_by_title": len(filtered),
            "filtered_by_content": len(low_quality)
        },
        "high_quality": high_quality,
        "filtered": filtered + low_quality
    }
    report_file = OUTPUT_DIR / "harvest_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n高质量文章已保存到: {output_file}")
    print(f"收割报告已保存到: {report_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
