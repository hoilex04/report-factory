#!/usr/bin/env python3
"""
Simple URL content fetcher for Report Factory.
Fetches and cleans web content for card generation.
"""

import sys
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
import json


def fetch_url(url):
    """Fetch content from URL with basic cleaning."""
    try:
        # Set headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')

            # Basic HTML cleaning
            # Remove scripts and styles
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else ""

            # Extract meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)', html, re.IGNORECASE)
            if not desc_match:
                desc_match = re.search(r'<meta[^>]*content=["\']([^"\']*)[^>]*name=["\']description["\']', html, re.IGNORECASE)
            description = desc_match.group(1).strip() if desc_match else ""

            # Extract main content (basic)
            # Try to find article or main content
            content = html
            for tag in ['article', 'main', '[role="main"]', '.content', '#content', '.post', '.entry']:
                pattern = f'<{tag}[^>]*>(.*?)</{tag.split()[0].replace("[", "").replace("]", "").replace("=", "").replace('"', '')}>' if not tag.startswith('.') and not tag.startswith('#') else f'class=["\']{tag[1:]}["\'][^>]*>(.*?)<'
                match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
                if match:
                    content = match.group(1)
                    break

            # Clean HTML tags
            text = re.sub(r'<[^>]+>', ' ', content)
            # Clean extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()

            return {
                "success": True,
                "url": url,
                "title": title,
                "description": description,
                "content": text[:10000]  # Limit content length
            }

    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch-url.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    result = fetch_url(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
