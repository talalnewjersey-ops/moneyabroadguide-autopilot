import os
import json
import requests

BASE_URL = os.environ.get("WP_URL", "https://moneyabroadguide.com")
POSTS_URL = BASE_URL + "/wp-json/mag/v1/posts"

response = requests.get(POSTS_URL)
posts = response.json()

results = []

for post in posts:
    title = post["title"]

    # Suggestions SEO SAFE
    suggestion = title
    if "2026" not in title:
        suggestion = title + " (2026 Guide)"

    results.append({
        "id": post["id"],
        "current_title": title,
        "suggested_title": suggestion
    })

# 📁 créer dossier
os.makedirs("artifacts", exist_ok=True)

# 📄 sauvegarder rapport
with open("artifacts/seo_report.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ SEO SAFE REPORT GENERATED")
