import base64

credentials = f"{WP_USER}:{WP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=data)
