import os
import base64
import requests

print("🔗 INTERNAL LINKING MODE ACTIVATED")

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

START = "<!-- MAG_LINKS_START -->"
END = "<!-- MAG_LINKS_END -->"


def get_posts():
    r = requests.get(POSTS_URL, headers=HEADERS)
    return r.json()


def remove_old_links(content):
    if START in content:
        return content.split(START)[0]
    return content


def generate_links(current_post, all_posts):
    links = []

    for post in all_posts:
        if post["id"] != current_post["id"]:
            title = post["title"]["rendered"]
            url = post["link"]
            links.append(f'<li><a href="{url}">{title}</a></li>')

    return links[:4]


def build_block(post, all_posts):
    links = generate_links(post, all_posts)

    return f"""
{START}
<h3>Related Guides</h3>
<ul>
{''.join(links)}
</ul>
{END}
"""


def update_post(post, all_posts):
    post_id = post["id"]
    content = post["content"]["rendered"]

    base = remove_old_links(content)
    new_content = base + build_block(post, all_posts)

    url = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"

    r = requests.post(url, headers=HEADERS, json={"content": new_content})

    print(f"Post {post_id} → {r.status_code}")


def main():
    posts = get_posts()

    print(f"Posts found: {len(posts)}")

    for post in posts:
        update_post(post, posts)

    print("✅ INTERNAL LINKING DONE")


if __name__ == "__main__":
    main()
