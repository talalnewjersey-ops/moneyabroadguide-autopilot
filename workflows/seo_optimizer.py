import os
import json
import requests

BASE_URL = os.environ.get("WP_URL", "https://moneyabroadguide.com").rstrip("/")
HEADERS = {"User-Agent": "Mozilla/5.0"}
POSTS_URL = f"{BASE_URL}/wp-json/mag/v1/posts"


def suggest_title(title: str) -> str:
    title = (title or "").strip()
    if not title:
        return title
    if "2026" not in title:
        return f"{title} (2026 Guide)"
    return title


def suggest_meta(title: str) -> str:
    title = (title or "").strip()
    if not title:
        return ""
    meta = f"Learn about {title.lower()} with practical tips, mistakes to avoid, and newcomer-friendly guidance."
    return meta[:155]


def main():
    r = requests.get(POSTS_URL, headers=HEADERS, timeout=20, allow_redirects=True)
    posts = r.json()

    suggestions = []

    for post in posts[:10]:
        old_title = post.get("title", "")
        new_title = suggest_title(old_title)
        meta = suggest_meta(old_title)

        suggestions.append({
            "id": post.get("id"),
            "current_title": old_title,
            "suggested_title": new_title,
            "suggested_meta_description": meta,
            "recommended_actions": [
                "Check if article has one H1 only",
                "Add 4-5 internal links to related USA/Canada newcomer guides",
                "Ensure FAQ section exists",
                "Ensure educational disclaimer is visible near top",
                "Check image ALT text relevance",
            ],
        })

    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/seo_recommendations.json", "w", encoding="utf-8") as f:
        json.dump(suggestions, f, indent=2, ensure_ascii=False)

    lines = ["# MoneyAbroadGuide Safe SEO Recommendations", ""]
    for item in suggestions:
        lines.append(f"## Post ID {item['id']}")
        lines.append(f"- Current title: {item['current_title']}")
        lines.append(f"- Suggested title: {item['suggested_title']}")
        lines.append(f"- Suggested meta description: {item['suggested_meta_description']}")
        lines.append("- Recommended actions:")
        for action in item["recommended_actions"]:
            lines.append(f"  - {action}")
        lines.append("")

    with open("artifacts/seo_recommendations.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
