import requests
import os

WP_URL = "https://moneyabroadguide.com/wp-json/wp/v2/posts"
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

def get_posts():
    response = requests.get(WP_URL, auth=(WP_USER, WP_PASSWORD))
    return response.json()

def update_post(post_id, new_title):
    url = f"{WP_URL}/{post_id}"

    data = {
        "title": new_title
    }

    response = requests.post(url, json=data, auth=(WP_USER, WP_PASSWORD))

    print(f"Update {post_id}: {response.status_code}")
    print(response.text)

def optimize_title(title):
    title = title.strip()

    if "2026" not in title:
        title += " (2026 Guide)"

    return title[:60]

def run():
    posts = get_posts()

    for post in posts:
        post_id = post["id"]
        title = post["title"]["rendered"]

        new_title = optimize_title(title)

        if new_title != title:
            print(f"Optimizing: {title}")
            update_post(post_id, new_title)

if __name__ == "__main__":
    run()
