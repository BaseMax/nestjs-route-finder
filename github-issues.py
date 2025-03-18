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


def get_all_issues():
    """Fetch all existing issues from GitHub using pagination."""
    issues = []
    page = 1

    while True:
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params={"state": "open", "per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Failed to fetch issues: {response.status_code}: {response.text}")
            break

        batch = response.json()
        if not batch:
            break

        issues.extend(batch)
        page += 1

    return issues


def delete_issue(issue_number):
    """Delete an issue by its number."""
    url = f"{GITHUB_API_URL}/{issue_number}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Issue #{issue_number} deleted successfully.")
    else:
        print(f"Failed to delete issue #{issue_number} - {response.status_code}: {response.text}")


def close_issue(issue_number):
    """Close an issue instead of deleting it."""
    url = f"{GITHUB_API_URL}/{issue_number}"
    issue_data = {"state": "closed"}
    response = requests.patch(url, json=issue_data, headers=HEADERS)

    if response.status_code == 200:
        print(f"Issue #{issue_number} closed successfully.")
    else:
        print(f"Failed to close issue #{issue_number} - {response.status_code}: {response.text}")


def remove_duplicate_issues():
    """Find and close duplicate issues, keeping only the first occurrence."""
    existing_issues = get_all_issues()
    issue_titles = {}

    for issue in existing_issues:
        title = issue["title"]
        issue_number = issue["number"]

        if title in issue_titles:
            print(f"Closing duplicate issue: {title} (#{issue_number})")
            close_issue(issue_number)
        else:
            issue_titles[title] = issue_number


def create_issue(title, body, labels, assignees):
    """Create a new GitHub issue and assign users."""
    issue_data = {
        "title": title,
        "body": body,
        "labels": labels,
        "assignees": assignees,
    }
    response = requests.post(GITHUB_API_URL, json=issue_data, headers=HEADERS)
    if response.status_code == 201:
        print(f"Issue created: {title}")
    else:
        print(f"Failed to create issue: {title} - {response.status_code}: {response.text}")


def update_issue(issue_number, body, assignees):
    """Update an existing issue to assign users."""
    url = f"{GITHUB_API_URL}/{issue_number}"
    issue_data = {"assignees": assignees, "body": body}
    response = requests.patch(url, json=issue_data, headers=HEADERS)
    if response.status_code == 200:
        print(f"Issue updated with assignees: {issue_number}")
    else:
        print(f"Failed to update issue: {issue_number} - {response.status_code}: {response.text}")


def format_issue_body(route, mention):
    """Format the issue body with API route details."""
    return f"""
### API Route Information
| Method | Path | File | Link |
|--------|------|------|------|
| `{route['method']}` | `{route['path']}` | `{route['file']}` | https://github.com/Rial-Payment/backend-old/blob/main/{route['file']} |

Tagging: {mention}
"""


def main():
    """Main function to handle issue management."""
    routes = load_routes()
    existing_issues = {issue["title"]: issue["number"] for issue in get_all_issues()}

    for index, route in enumerate(routes):
        assignee = "user1" if index % 2 != 0 else "user2"
        mention = f"@{assignee}"
        title = f"API `[{route['method']}]`: `{route['path']}`"
        body = format_issue_body(route, mention)
        labels = ["api-route", "method-" + route['method'].lower()]

        if title in existing_issues:
            issue_number = existing_issues[title]
            print(f"Updating existing issue: {title} (#{issue_number})")
            update_issue(issue_number, body, [assignee])
        else:
            print(f"Creating new issue: {title}")
            create_issue(title, body, labels, [assignee])


if __name__ == "__main__":
    remove_duplicate_issues()
    main()
