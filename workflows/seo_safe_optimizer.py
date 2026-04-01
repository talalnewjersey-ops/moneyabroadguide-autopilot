import requests
import os

WP_URL = "https://moneyabroadguide.com/wp-json/wp/v2/posts"
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

def get_posts():
    response = requests.get(WP_URL, auth=(WP_USER, WP_PASSWORD))
    return response.json()

def update_post(post_id, data):
    url = f"{WP_URL}/{post_id}"
    response = requests.post(url, json=data, auth=(WP_USER, WP_PASSWORD))
    return response.status_code

def optimize_title(title):
    if len(title) < 50:
        return title + " (2026 Guide)"
    return title[:60]

def optimize_meta(title):
    return f"{title} - Complete guide for newcomers in USA & Canada. Updated 2026."

def run():
    posts = get_posts()

    for post in posts:
        post_id = post["id"]
        title = post["title"]["rendered"]

        new_title = optimize_title(title)
        new_meta = optimize_meta(title)

        print(f"Optimizing: {title}")

        update_post(post_id, {
            "title": new_title,
            "meta": {
                "description": new_meta
            }
        })

if __name__ == "__main__":
    run()
