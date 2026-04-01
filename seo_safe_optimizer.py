import os
import base64
import requests

# ==============================
# 🔐 LOAD ENV VARIABLES (GitHub Secrets)
# ==============================

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

# Debug (important au début)
print("WP_URL:", WP_URL)
print("WP_USER:", WP_USER)
print("WP_PASSWORD OK:", bool(WP_PASSWORD))

# ==============================
# 🔐 AUTH (Basic Header)
# ==============================

credentials = f"{WP_USER}:{WP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# ==============================
# 📥 GET POSTS (SAFE LIMIT)
# ==============================

def get_posts():
    url = f"{WP_URL}/wp-json/wp/v2/posts?per_page=10"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("❌ Error fetching posts:", response.status_code)
        return []

    return response.json()

# ==============================
# ✏️ SAFE UPDATE FUNCTION
# ==============================

def update_post(post):
    post_id = post["id"]
    title = post["title"]["rendered"]

    print(f"Updating: {title}")

    # 👉 SAFE SEO improvement (no content overwrite)
    new_data = {
        "title": title.strip(),  # nettoyage simple
    }

    url = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"

    response = requests.post(url, headers=HEADERS, json=new_data)

    print("Status:", response.status_code)

# ==============================
# 🚀 MAIN
# ==============================

def main():
    posts = get_posts()

    print(f"Posts found: {len(posts)}")

    for post in posts:
        update_post(post)

# ==============================
# ▶️ RUN
# ==============================

if __name__ == "__main__":
    main()
