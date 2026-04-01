import requests

url = "https://moneyabroadguide.com/wp-json/mag/v1/posts"

response = requests.get(url)

posts = response.json()

for post in posts:
    print("Optimizing:", post["title"])
