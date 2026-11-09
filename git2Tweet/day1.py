import os

import requests
from dotenv import load_dotenv

load_dotenv(r"F:\Vedant\Projects\AgenticAI\git2tweet\.env")

TOKEN = os.environ["GITHUB_TOKEN"]
OWNER = "Vex-15"
REPO = "Go-shop"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}
# 1. list the latest commit
url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"
resp = requests.get(url, headers=headers, params={"per_page": 1})
resp.raise_for_status()
sha = resp.json()[0]["sha"]

# 2. fetch that commit in full (this includes the diff)
resp = requests.get(f"{url}/{sha}", headers=headers)
resp.raise_for_status()
commit = resp.json()

print("SHA:", sha[:7])
print("Message:", commit["commit"]["message"])
print("Author:", commit["commit"]["author"]["name"])
print()
for f in commit["files"]:
    print(
        f"--- {f['filename']} ({f['status']}, +{f['additions']} -{f['deletions']})")
    print(f.get("patch", "(no patch, probably binary)"))
