#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Morning Harvest Script
自动抓取 arXiv 论文，并提醒用户补充微信 / 飞书链接。
将结果写入 Obsidian Inbox.md 的"待处理链接"区域。

依赖:
    - requests: pip install requests
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

# ==================== 配置区（请自行修改） ====================
WORKSPACE = Path(os.environ.get("REPORT_FACTORY_WORKSPACE", "."))
OBSIDIAN_ROOT = Path(os.environ.get("REPORT_FACTORY_OBSIDIAN_ROOT", "~/Obsidian"))
INBOX_PATH = OBSIDIAN_ROOT / "Atomic-card" / "Inbox.md"
MASTER_INDEX_PATH = WORKSPACE / "master_index.json"

# arXiv 分类与领域映射
ARXIV_CATEGORIES = {
    "EAI": ["cs.RO"],
    "AIH": ["cs.AR", "cs.DC"],
    "MM": ["cs.CV", "cs.MM"],
    "COG": ["cs.AI", "cs.LG"],
    "AGT": ["cs.MA", "cs.AI"],
}

# 每个领域抓取的最大结果数
MAX_RESULTS_PER_DOMAIN = 5
# 每个领域写入 Inbox 的最大条目数
TOP_N_PER_DOMAIN = 3

# ==================== Utility Functions ====================

def load_master_index():
    if MASTER_INDEX_PATH.exists():
        with open(MASTER_INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def check_duplicate(url, title, index_data):
    for item in index_data:
        if url in item.get("source", ""):
            return True
        existing_title = item.get("title", "")
        if existing_title and title:
            from difflib import SequenceMatcher
            if SequenceMatcher(None, title.lower(), existing_title.lower()).ratio() > 0.85:
                return True
    return False


def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ==================== arXiv API Fetch ====================
def fetch_arxiv_papers():
    print("\n[1/2] Fetching arXiv papers...")
    papers = []
    seen_ids = set()

    try:
        import requests
    except ImportError:
        print("缺少 requests 依赖，请运行: pip install requests")
        return papers

    base_url = "http://export.arxiv.org/api/query"

    for domain, categories in ARXIV_CATEGORIES.items():
        category_query = " OR ".join([f"cat:{cat}" for cat in categories])

        try:
            url = (
                f"{base_url}?search_query=({category_query})"
                f"&sortBy=submittedDate&sortOrder=descending&max_results={MAX_RESULTS_PER_DOMAIN}"
            )
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}

            for entry in root.findall("atom:entry", ns)[:TOP_N_PER_DOMAIN]:
                id_elem = entry.find("atom:id", ns)
                title_elem = entry.find("atom:title", ns)

                if id_elem is None or title_elem is None:
                    continue

                arxiv_id = id_elem.text.split("/abs/")[-1]
                if arxiv_id in seen_ids:
                    continue
                seen_ids.add(arxiv_id)

                title = title_elem.text.strip() if title_elem.text else ""
                if title and len(title) > 10:
                    papers.append({
                        "title": title,
                        "url": id_elem.text,
                        "domains": [domain],
                        "source": "arxiv",
                    })

        except Exception as e:
            print(f"       {domain} error: {e}")

    print(f"       Found {len(papers)} papers")
    return papers


# ==================== Write to Inbox ====================
def write_to_inbox(papers):
    print("\n[2/2] Writing to Inbox...")

    inbox = Path(INBOX_PATH).expanduser()
    if not inbox.exists():
        print(f"       Error: Inbox not found at {inbox}")
        return False

    with open(inbox, "r", encoding="utf-8") as f:
        content = f.read()

    index_data = load_master_index()
    new_links = []
    duplicate_count = 0

    for paper in papers:
        if not check_duplicate(paper["url"], paper["title"], index_data):
            domain_str = "/".join(paper["domains"])
            new_links.append({
                "type": "arxiv",
                "domain": domain_str,
                "title": paper["title"],
                "url": paper["url"],
            })
        else:
            duplicate_count += 1

    if not new_links:
        print("       No new links (all duplicates)")
        return True

    today = get_today_date()
    timestamp = get_timestamp()

    new_section = f"\n### {today} Morning Harvest ({timestamp})\n\n"
    new_section += "**arXiv Papers** (自动抓取)\n"
    for link in new_links:
        new_section += f"- [ ] **{link['domain']}** {link['title']}\n  - {link['url']}\n"
    new_section += "\n"

    new_section += "**Weixin Articles** (请手动添加)\n"
    new_section += "- [ ] 粘贴微信文章链接 1\n"
    new_section += "- [ ] 粘贴微信文章链接 2\n\n"

    new_section += "**Feishu News** (请手动添加)\n"
    new_section += "- [ ] 粘贴飞书新闻链接 1\n"
    new_section += "- [ ] 粘贴飞书新闻链接 2\n\n"

    # 尝试在"待处理链接"区块追加
    pattern = r"(## 待处理链接\s*\n.*?\n)(.*?)(\n---|\n## )"

    def replace_func(match):
        prefix = match.group(1)
        existing = match.group(2).strip()
        suffix = match.group(3)
        if existing:
            return f"{prefix}{existing}\n{new_section}{suffix}"
        return f"{prefix}{new_section}{suffix}"

    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

    with open(inbox, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"       Wrote {len(new_links)} arXiv papers")
    if duplicate_count > 0:
        print(f"       Skipped {duplicate_count} duplicates")

    return True


# ==================== Main ====================
def main():
    if sys.platform == "win32":
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

    print("=" * 50)
    print(f"Morning Harvest - {get_today_date()}")
    print("=" * 50)

    papers = fetch_arxiv_papers()
    success = write_to_inbox(papers)

    print("\n" + "=" * 50)
    print("\u2705 MORNING HARVEST COMPLETE!")
    print("=" * 50)
    print(f"arXiv: {len(papers)} papers fetched")
    print("\n\ud83d\udcdd Please add manually:")
    print("  1. Weixin article links")
    print("  2. Feishu news links")
    print("\n\ud83d\udcac Then tell Claude: '\u6536\u5272 Inbox'")
    print("=" * 50)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
