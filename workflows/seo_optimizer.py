import requests

GET_URL = "https://moneyabroadguide.com/wp-json/mag/v1/posts"
UPDATE_URL = "https://moneyabroadguide.com/wp-json/mag/v1/update-post"

posts = requests.get(GET_URL).json()

for post in posts:
    old_title = post["title"]
    new_title = old_title + " (2026 Guide)"

    print("Updating:", old_title)

    requests.post(UPDATE_URL, json={
        "id": post["id"],
        "title": new_title
    })
