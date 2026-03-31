#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文章抓取器 - 智能降级策略
优先使用轻量级 HTTP 方案，失败时尝试降级到 Playwright。

依赖（可选）:
    - playwright: pip install playwright && playwright install
"""

import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")


def fetch_with_urllib(url):
    """方案 1：轻量级 HTTP 请求（推荐，速度快）"""
    import re
    import ssl
    import urllib.error
    import urllib.request

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://mp.weixin.qq.com/",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        context = ssl._create_unverified_context()

        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            html = response.read().decode("utf-8")

        title_match = re.search(
            r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.DOTALL
        )
        if not title_match:
            title_match = re.search(
                r'<h2[^>]*class="rich_media_title"[^>]*>(.*?)</h2>', html, re.DOTALL
            )
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else "未找到标题"

        author_match = re.search(
            r'<a[^>]*class="rich_media_meta_link"[^>]*>(.*?)</a>', html, re.DOTALL
        )
        if not author_match:
            author_match = re.search(r'var\s+nickname\s*=\s*"([^"]+)"', html)
        author = re.sub(r"<[^>]+>", "", author_match.group(1)).strip() if author_match else "未知作者"

        time_match = re.search(
            r'<em[^>]*id="publish_time"[^>]*>(.*?)</em>', html, re.DOTALL
        )
        if not time_match:
            time_match = re.search(r'var\s+publish_time\s*=\s*"([^"]+)"', html)
        publish_time = re.sub(r"<[^>]+>", "", time_match.group(1)).strip() if time_match else ""

        content_match = re.search(
            r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL
        )
        if content_match:
            content_html = content_match.group(1)
            content = re.sub(r"<[^>]+>", "", content_html)
            content = re.sub(r"\s+", " ", content).strip()
        else:
            content = "未找到正文内容"

        return {
            "success": True,
            "title": title,
            "author": author,
            "publish_time": publish_time,
            "content": content,
            "full_length": len(content),
            "method": "urllib",
        }

    except Exception as e:
        return {"success": False, "error": str(e), "method": "urllib"}


def fetch_with_playwright(url):
    """方案 2：Playwright 浏览器（备用，慢但稳定）"""
    try:
        from playwright.async_api import async_playwright
        import asyncio

        async def fetch():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle", timeout=60000)
                title = await page.locator(".rich_media_title").inner_text(timeout=5000)
                content = await page.locator("#js_content").inner_text(timeout=5000)
                await browser.close()
                return {
                    "success": True,
                    "title": title.strip(),
                    "author": "未知作者",
                    "publish_time": "",
                    "content": content.strip(),
                    "full_length": len(content.strip()),
                    "method": "playwright",
                }

        return asyncio.run(fetch())

    except ImportError:
        return {
            "success": False,
            "error": "Playwright 未安装。请运行: pip install playwright && playwright install chromium",
            "method": "playwright",
        }
    except Exception as e:
        return {"success": False, "error": str(e), "method": "playwright"}


def fetch_weixin_article(url):
    """智能降级策略：优先 urllib，失败时降级到 playwright"""
    print("\ud83d\ude80 [方案 1] 使用轻量级 HTTP 请求...", file=sys.stderr)
    result = fetch_with_urllib(url)

    if result.get("success"):
        print("\u2705 [方案 1] 成功获取文章内容", file=sys.stderr)
        return result

    print(f"\u26a0\ufe0f [方案 1] 失败: {result.get('error')}", file=sys.stderr)
    print("\ud83d\udd04 [方案 2] 降级到 Playwright 浏览器...", file=sys.stderr)

    result = fetch_with_playwright(url)

    if result.get("success"):
        print("\u2705 [方案 2] 成功获取文章内容", file=sys.stderr)
    else:
        print(f"\u274c [方案 2] 失败: {result.get('error')}", file=sys.stderr)

    return result


if __name__ == "__main__":
    url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "https://mp.weixin.qq.com/s/Lxs9FvEkc5dC5MGNsj-8Cg"
    )
    result = fetch_weixin_article(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
