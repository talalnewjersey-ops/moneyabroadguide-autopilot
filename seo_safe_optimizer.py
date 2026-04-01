import requests
import os
import base64

# ========================
# CONFIG
# ========================
WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

credentials = f"{WP_USER}:{WP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# ========================
# GET POSTS
# ========================
def get_posts():
    url = f"{WP_URL}/wp-json/wp/v2/posts?per_page=10"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("❌ Error fetching posts:", response.text)
        return []

    return response.json()

# ========================
# SEO OPTIMIZATION LOGIC
# ========================
def optimize_post(post):
    title = post["title"]["rendered"]
    content = post["content"]["rendered"]

    # SAFETY
    if len(content) < 800:
        print("⏭ Skipped (too short)")
        return None

    # ========================
    # NEW TITLE (CTR BOOST)
    # ========================
    if "2026" not in title:
        new_title = title + " (2026 Guide)"
    else:
        new_title = title

    # ========================
    # META DESCRIPTION
    # ========================
    meta_desc = f"Discover everything about {title.lower()} in this updated 2026 guide for newcomers in the USA and Canada. Save money and avoid costly mistakes."

    # ========================
    # INTRO IMPROVEMENT
    # ========================
    intro = f"""
<p><strong>Updated for 2026:</strong> If you're a newcomer in the USA or Canada, understanding {title.lower()} is essential to avoid costly mistakes and build a strong financial future.</p>
"""

    # ========================
    # INTERNAL LINKING (SAFE)
    # ========================
    internal_block = """
<h3>Related Guides</h3>
<ul>
<li><a href="/best-banks-for-newcomers-canada">Best Banks for Newcomers in Canada</a></li>
<li><a href="/build-credit-score-usa">How to Build Credit Score in the USA</a></li>
<li><a href="/money-transfer-apps-usa">Best Money Transfer Apps USA</a></li>
</ul>
"""

    # ========================
    # CTA (LIGHT)
    # ========================
    cta = """
<p><strong>💡 Tip:</strong> Always compare banking and transfer options to avoid hidden fees.</p>
"""

    # ========================
    # FINAL CONTENT
    # ========================
    new_content = intro + content + internal_block + cta

    return {
        "title": new_title,
        "content": new_content,
        "meta": {
            "_yoast_wpseo_metadesc": meta_desc
        }
    }

# ========================
# UPDATE POST
# ========================
def update_post(post_id, data):
    url = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"
    response = requests.post(url, headers=HEADERS, json=data)

    print(f"Status: {response.status_code}")

# ========================
# MAIN
# ========================
def main():
    print("🚀 START PRO SEO OPTIMIZER")

    print("WP_URL:", WP_URL)
    print("WP_USER:", WP_USER)
    print("WP_PASSWORD OK:", bool(WP_PASSWORD))

    posts = get_posts()

    print(f"Posts found: {len(posts)}")

    for post in posts:
        print("Updating:", post["title"]["rendered"])

        optimized = optimize_post(post)

        if not optimized:
            continue

        update_post(post["id"], optimized)

# ========================
if __name__ == "__main__":
    main()