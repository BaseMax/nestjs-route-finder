import json
import requests

REPO_OWNER = "xxxxxxxxx"
REPO_NAME = "backend-new"
GITHUB_TOKEN = "xxxxxxxxx"

with open("routes.json", "r", encoding="utf-8") as file:
    routes = json.load(file)

GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

for index, route in enumerate(routes):
    mention = "@xxxxxxxxx1" if index % 2 != 0 else "@xxxxxxxxx2"
    title = f"API `[{route['method']}]`: `{route['path']}`"
    
    body = f"""
### API Route Information
| Method | Path | File |
|--------|------|------|
| `{route['method']}` | `{route['path']}` | `{route['file']}` |

Tagging: {mention}
"""

    issue_data = {
        "title": title,
        "body": body,
        "labels": ["api-route", "method-" + route['method'].lower()]
    }
    
    response = requests.post(GITHUB_API_URL, json=issue_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Issue created: {title}")
    else:
        print(f"Failed to create issue: {title} - {response.status_code}: {response.text}")
