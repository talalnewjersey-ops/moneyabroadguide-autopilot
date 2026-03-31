import requests
from bs4 import BeautifulSoup

url = "https://moneyabroadguide.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)

if "Checking your browser" in response.text:
    print("❌ Bot protection active")
else:
    print("✅ Site accessible")

soup = BeautifulSoup(response.text, "html.parser")

title = soup.title.string if soup.title else "No title"
print("TITLE:", title)

meta = soup.find("meta", attrs={"name": "description"})
if meta:
    print("META:", meta.get("content"))
else:
    print("❌ No meta description")

h1 = soup.find_all("h1")
print("H1 COUNT:", len(h1))
