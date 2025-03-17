import json
import requests

REPO_OWNER = "xxxxxxxxx"
REPO_NAME = "backend-new"
GITHUB_TOKEN = "xxxxxxxxx"

GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def load_routes(file_path="routes.json"):
    """Load routes from the JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_existing_issue_titles():
    """Fetch existing issue titles from GitHub."""
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        return {issue["title"] for issue in response.json()}
    print(f"Failed to fetch existing issues: {response.status_code}: {response.text}")
    return set()


def create_issue(title, body, labels):
    """Create a new GitHub issue."""
    issue_data = {"title": title, "body": body, "labels": labels}
    response = requests.post(GITHUB_API_URL, json=issue_data, headers=HEADERS)
    if response.status_code == 201:
        print(f"Issue created: {title}")
    else:
        print(f"Failed to create issue: {title} - {response.status_code}: {response.text}")


def format_issue_body(route, mention):
    """Format the issue body with API route details."""
    return f"""
### API Route Information
| Method | Path | File |
|--------|------|------|
| `{route['method']}` | `{route['path']}` | `{route['file']}` |

Tagging: {mention}
"""


def main():
    routes = load_routes()
    existing_titles = get_existing_issue_titles()

    for index, route in enumerate(routes):
        mention = "@user1" if index % 2 != 0 else "@user2"
        title = f"API `[{route['method']}]`: `{route['path']}`"
        
        if title in existing_titles:
            print(f"Skipping existing issue: {title}")
            continue
        
        body = format_issue_body(route, mention)
        labels = ["api-route", "method-" + route['method'].lower()]
        create_issue(title, body, labels)


if __name__ == "__main__":
    main()
