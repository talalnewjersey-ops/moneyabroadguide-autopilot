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


def generate_money_block():
    return """
<div style="border:1px solid #ddd;padding:15px;margin:20px 0;">
<h3>💡 Recommended Tools for Newcomers</h3>
<p>Compare the best money transfer services and save on fees.</p>
<a href="#" target="_blank">👉 Compare Best Services</a>
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
