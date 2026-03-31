#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文章抓取器 - 基础版
使用 urllib 轻量级抓取微信公众号文章，无需额外依赖。
"""

import json
import re
import ssl
import sys
import urllib.error
import urllib.request


def fetch_weixin_article(url):
    """抓取微信公众号文章"""
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

        # 提取标题
        title_match = re.search(
            r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.DOTALL
        )
        if not title_match:
            title_match = re.search(
                r'<h2[^>]*class="rich_media_title"[^>]*>(.*?)</h2>', html, re.DOTALL
            )
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else "未找到标题"

        # 提取作者
        author_match = re.search(
            r'<a[^>]*class="rich_media_meta_link"[^>]*>(.*?)</a>', html, re.DOTALL
        )
        if not author_match:
            author_match = re.search(r'var\s+nickname\s*=\s*"([^"]+)"', html)
        author = re.sub(r"<[^>]+>", "", author_match.group(1)).strip() if author_match else "未知作者"

        # 提取发布时间
        time_match = re.search(
            r'<em[^>]*id="publish_time"[^>]*>(.*?)</em>', html, re.DOTALL
        )
        if not time_match:
            time_match = re.search(r'var\s+publish_time\s*=\s*"([^"]+)"', html)
        publish_time = re.sub(r"<[^>]+">", "", time_match.group(1)).strip() if time_match else ""

        # 提取正文
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
            "content": content[:5000],
            "full_length": len(content),
            "method": "urllib",
        }

    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}", "method": "urllib"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"URL Error: {e.reason}", "method": "urllib"}
    except Exception as e:
        return {"success": False, "error": str(e), "method": "urllib"}


if __name__ == "__main__":
    if sys.platform == "win32":
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

    url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "https://mp.weixin.qq.com/s/Lxs9FvEkc5dC5MGNsj-8Cg"
    )
    result = fetch_weixin_article(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
