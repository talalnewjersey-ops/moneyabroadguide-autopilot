import requests
import os

WP_URL = "https://moneyabroadguide.com/wp-json/wp/v2/posts"
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

def run():
    try:
        response = requests.get(WP_URL, auth=(WP_USER, WP_PASSWORD))
        posts = response.json()

        print(f"Posts found: {len(posts)}")

        for post in posts:
            post_id = post["id"]
            title = post["title"]["rendered"]

            if "2026" not in title:
                new_title = title.strip() + " (2026 Guide)"

                print(f"Updating: {title}")

                r = requests.post(
                    f"{WP_URL}/{post_id}",
                    json={"title": new_title},
                    auth=(WP_USER, WP_PASSWORD)
                )

                print(f"Status: {r.status_code}")

    except Exception as e:
        print("ERROR:", str(e))

if __name__ == "__main__":
    run()
