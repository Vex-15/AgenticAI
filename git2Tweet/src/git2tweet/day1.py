import os

import requests

TOKEN = os.environ("GITHUB_TOKEN")
OWNER = "Vex-15"
REPO = "Go-shop"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

url = f"https://www.github.com/{OWNER}/{REPO}/commits"
resp = requests.get(url, headers=headers, params={"per_page":1})
resp.raise_for_status
commit = resp.json();
