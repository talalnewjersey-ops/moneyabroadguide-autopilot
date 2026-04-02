import os
import base64
import requests
import json

print("🔒 SAFE MODE ACTIVATED (NO CONTENT CREATION)")

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

credentials = f"{WP_USER}:{WP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

POSTS_URL = f"{WP_URL}/wp-json/wp/v2/posts?per_page=10&_fields=id,title,content,excerpt,link"

START = "<!-- MAG_SAFE_BLOCK -->"
END = "<!-- /MAG_SAFE_BLOCK -->"


def get_posts():
    r = requests.get(POSTS_URL, headers=HEADERS)
    if r.status_code != 200:
        raise Exception("❌ Cannot fetch posts")
    return r.json()


def clean_title(title):
    title = title.strip()

    if "2026" not in title:
        title = title + " (2026 Guide)"

    if len(title) > 65:
        title = title[:64] + "…"

    return title


def build_excerpt(title):
    return f"{title}. Practical guide for newcomers to USA and Canada."[:150]


def remove_old_block(content):
    if START in content:
        return content.split(START)[0]
    return content


def build_block(post):
    return f"""
{START}
<p><strong>Author:</strong> Talal Eddaouahiri – Finance expert for newcomers in USA & Canada</p>
<p><strong>Disclaimer:</strong> Educational purposes only. Not financial advice.</p>
<p><a href="/">More guides on MoneyAbroadGuide.com</a></p>
{END}
"""


def backup(posts):
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/backup.json", "w") as f:
        json.dump(posts, f)


def update_post(post, all_posts):
    post_id = post["id"]

    old_title = post["title"]["rendered"]
    old_content = post["content"]["rendered"]

    new_title = clean_title(old_title)
    new_excerpt = build_excerpt(new_title)

    base_content = remove_old_block(old_content)
    new_content = base_content + build_block(post)

    payload = {
        "title": new_title,
        "excerpt": new_excerpt,
        "content": new_content
    }

    url = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"
    r = requests.post(url, headers=HEADERS, json=payload)

    print(f"Update {post_id} → {r.status_code}")


def main():
    posts = get_posts()
    print(f"Posts found: {len(posts)}")

    backup(posts)

    for post in posts:
        update_post(post, posts)

    print("✅ SAFE SEO DONE")


if __name__ == "__main__":
    main()
