import os
import re
import json
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = os.environ.get("WP_URL", "https://moneyabroadguide.com").rstrip("/")
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 20


def clean_text(value):
    return " ".join((value or "").split())


def is_internal(href: str) -> bool:
    if not href:
        return False
    if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return False
    parsed = urlparse(href)
    if not parsed.netloc:
        return True
    return parsed.netloc.endswith("moneyabroadguide.com")


def absolute(base, href):
    return urljoin(base, href)


def fetch(url):
    return requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)


def audit_url(url):
    result = {
        "url": url,
        "status_code": None,
        "title": "",
        "meta_description": "",
        "h1_count": 0,
        "internal_links": 0,
        "empty_links": 0,
        "word_count": 0,
        "issues": [],
    }

    try:
        r = fetch(url)
        result["status_code"] = r.status_code
        html = r.text

        if "Checking your browser before accessing" in html or "Bot Verification" in html:
            result["issues"].append("Bot protection challenge visible.")
            return result

        if r.status_code >= 400:
            result["issues"].append(f"HTTP {r.status_code}")
            return result

        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("title")
        title = clean_text(title_tag.get_text(" ", strip=True) if title_tag else "")
        result["title"] = title
        if not title:
            result["issues"].append("Missing title.")
        elif len(title) > 60:
            result["issues"].append(f"Title too long ({len(title)} chars).")

        meta = soup.find("meta", attrs={"name": "description"})
        meta_desc = clean_text(meta.get("content", "") if meta else "")
        result["meta_description"] = meta_desc
        if not meta_desc:
            result["issues"].append("Missing meta description.")
        elif len(meta_desc) > 160:
            result["issues"].append(f"Meta description too long ({len(meta_desc)} chars).")

        h1s = soup.find_all("h1")
        result["h1_count"] = len(h1s)
        if len(h1s) == 0:
            result["issues"].append("Missing H1.")
        elif len(h1s) > 1:
            result["issues"].append(f"Multiple H1 tags ({len(h1s)}).")

        body_text = clean_text(soup.body.get_text(" ", strip=True) if soup.body else "")
        result["word_count"] = len(re.findall(r"\w+", body_text))
        if "/wp-json/" not in url and result["word_count"] < 300:
            result["issues"].append(f"Very thin content ({result['word_count']} words).")

        links = [a.get("href", "").strip() for a in soup.find_all("a")]
        result["empty_links"] = sum(1 for x in links if x in ("", "#"))
        if result["empty_links"] > 0:
            result["issues"].append(f"Empty/hash links found ({result['empty_links']}).")

        internal_links = [absolute(url, href) for href in links if is_internal(href)]
        result["internal_links"] = len(internal_links)
        if "/wp-json/" not in url and result["internal_links"] < 3:
            result["issues"].append(f"Low internal linking ({result['internal_links']}).")

        return result

    except Exception as exc:
        result["issues"].append(f"Request failed: {exc}")
        return result


def get_posts():
    endpoint = f"{BASE_URL}/wp-json/mag/v1/posts"
    r = fetch(endpoint)
    if r.status_code != 200:
        return [], f"Posts endpoint returned HTTP {r.status_code}"
    try:
        return r.json(), None
    except Exception as exc:
        return [], f"Posts endpoint JSON parse failed: {exc}"


def main():
    os.makedirs("artifacts", exist_ok=True)

    report = []
    report.append(audit_url(BASE_URL + "/"))

    posts, err = get_posts()
    if err:
        report.append({
            "url": f"{BASE_URL}/wp-json/mag/v1/posts",
            "status_code": None,
            "title": "",
            "meta_description": "",
            "h1_count": 0,
            "internal_links": 0,
            "empty_links": 0,
            "word_count": 0,
            "issues": [err],
        })
    else:
        for post in posts[:5]:
            report.append(audit_url(f"{BASE_URL}/?p={post['id']}"))

    with open("artifacts/site_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    lines = ["# MoneyAbroadGuide Safe Technical Audit", ""]
    for item in report:
        lines.append(f"## {item['url']}")
        lines.append(f"- HTTP status: {item['status_code']}")
        lines.append(f"- Title: {item['title']}")
        lines.append(f"- Meta description: {item['meta_description']}")
        lines.append(f"- H1 count: {item['h1_count']}")
        lines.append(f"- Word count: {item['word_count']}")
        lines.append(f"- Internal links: {item['internal_links']}")
        if item["issues"]:
            lines.append("- Issues:")
            for issue in item["issues"]:
                lines.append(f"  - {issue}")
        else:
            lines.append("- Issues: none detected")
        lines.append("")

    with open("artifacts/site_audit_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
