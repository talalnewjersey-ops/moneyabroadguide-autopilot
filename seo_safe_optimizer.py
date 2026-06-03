import os
import base64
import requests
import json

print("🚀 SCHEMA + MONEY MODE ACTIVATED")

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

credentials = f"{WP_USER}:{WP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

POSTS_URL = f"{WP_URL}/wp-json/wp/v2/posts?per_page=10&_fields=id,title,content,link"

START = "<!-- MAG_SCHEMA_START -->"
END = "<!-- MAG_SCHEMA_END -->"


def get_posts():
    return requests.get(POSTS_URL, headers=HEADERS).json()


def clean_old(content):
    if START in content:
        return content.split(START)[0]
    return content


def generate_schema(post):
    title = post["title"]["rendered"]
    url = post["link"]

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "author": {
            "@type": "Person",
            "name": "Talal Eddaouahiri"
        },
        "publisher": {
            "@type": "Organization",
            "name": "MoneyAbroadGuide"
        },
        "mainEntityOfPage": url
    }

    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'


EBOOK_LANDING_URL = "https://moneyabroadguide.com/build-your-credit-score-in-the-usa-2026-edition/"
EBOOK_URL         = "https://moneyabroadguide.gumroad.com/l/vemvxw"  # Gumroad checkout


def generate_money_block():
    return f"""
<div style="border:2px solid #1a9e5f;padding:20px 24px;margin:28px 0;border-radius:10px;background:#f0fdf4;">
  <p style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#1a9e5f;margin:0 0 8px;">
    New for 2026
  </p>
  <h3 style="font-size:18px;font-weight:800;color:#111;margin:0 0 8px;line-height:1.3;">
    Build Your Credit Score in the USA
  </h3>
  <p style="color:#444;font-size:15px;margin:0 0 14px;line-height:1.6;">
    The complete step-by-step guide for newcomers — from zero credit to a strong score.
    184 pages, beginner-friendly, instant download.
  </p>
  <a href="{EBOOK_URL}"
     style="display:inline-block;background:#1a9e5f;color:#fff !important;font-weight:700;font-size:14px;
            padding:11px 24px;border-radius:6px;text-decoration:none;">
    Get Instant Access — $19.99
  </a>
</div>

<div style="border:1px solid #e5e7eb;padding:16px 20px;margin:20px 0;border-radius:8px;">
  <h3 style="font-size:16px;font-weight:700;color:#111;margin:0 0 8px;">
    &#128161; Recommended Tools for Newcomers
  </h3>
  <p style="color:#555;font-size:14px;margin:0 0 10px;">Compare the best money transfer services and save on fees.</p>
  <a href="/compare-fees/" style="color:#1a9e5f;font-weight:600;font-size:14px;text-decoration:none;">
    &#128073; Compare Best Services &#8594;
  </a>
</div>

<!-- ADSENSE PLACEHOLDER -->
<div style="margin:20px 0;text-align:center;">
<p>Advertisement</p>
</div>
"""


def update_post(post):
    post_id = post["id"]
    content = post["content"]["rendered"]

    base = clean_old(content)

    schema = generate_schema(post)
    money = generate_money_block()

    new_content = base + f"\n{START}\n{schema}\n{money}\n{END}"

    url = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"

    r = requests.post(url, headers=HEADERS, json={"content": new_content})

    print(f"Post {post_id} → {r.status_code}")


def main():
    posts = get_posts()

    print(f"Posts found: {len(posts)}")

    for post in posts:
        update_post(post)

    print("✅ SCHEMA + MONEY DONE")


if __name__ == "__main__":
    main()
