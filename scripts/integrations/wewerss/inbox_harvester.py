#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inbox 收割脚本 - 自动提取 Obsidian 收件箱中的待处理链接

用法:
    python inbox_harvester.py
"""

import os
import re
import sys
from pathlib import Path

INBOX_PATH = Path(os.environ.get("REPORT_FACTORY_INBOX_PATH", "~/Obsidian/Atomic-card/Inbox.md"))


def extract_links_from_inbox():
    """从 Inbox.md 中提取所有待处理链接"""
    inbox = Path(INBOX_PATH).expanduser()
    if not inbox.exists():
        print(f"\u274c Inbox.md 不存在: {inbox}")
        return []

    with open(inbox, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取"待处理链接"区块的内容
    pattern = r"## 待处理链接\s*\n.*?\n(.*?)\n---"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("\u26a0\ufe0f 未找到待处理链接区块")
        return []

    links_section = match.group(1)
    url_pattern = r"https?://[^\s\)\"]+"

    valid_links = []
    for line in links_section.split("\n"):
        line = line.strip()
        if line and not line.startswith("<!--") and not line.startswith("##"):
            urls = re.findall(url_pattern, line)
            valid_links.extend(urls)

    return valid_links


def archive_processed_links(links, timestamp):
    """将已处理的链接归档到历史区，并清空待处理区"""
    inbox = Path(INBOX_PATH).expanduser()
    with open(inbox, "r", encoding="utf-8") as f:
        content = f.read()

    archive_entry = f"\n### {timestamp}\n"
    for link in links:
        archive_entry += f"- \u2705 {link}\n"

    content = content.replace(
        "<!-- Claude \u5904\u7406\u5b8c\u6210\u540e\u4f1a\u81ea\u52a8\u8bb0\u5f55\u5230\u8fd9\u91cc -->",
        f"<!-- Claude \u5904\u7406\u5b8c\u6210\u540e\u4f1a\u81ea\u52a8\u8bb0\u5f55\u5230\u8fd9\u91cc -->{archive_entry}",
    )

    content = re.sub(
        r"(## 待处理链接\s*\n.*?\n)(.*?)(\n---)",
        r"\1\n\n\3",
        content,
        flags=re.DOTALL,
    )

    with open(inbox, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    if sys.platform == "win32":
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

    links = extract_links_from_inbox()

    if not links:
        print("\ud83d\udced Inbox \u4e3a\u7a7a\uff0c\u6ca1\u6709\u5f85\u5904\u7406\u94fe\u63a5")
    else:
        print(f"\ud83d\udce5 \u53d1\u73b0 {len(links)} \u4e2a\u5f85\u5904\u7406\u94fe\u63a5\uff1a")
        for i, link in enumerate(links, 1):
            print(f"  {i}. {link}")
