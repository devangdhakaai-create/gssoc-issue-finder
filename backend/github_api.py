# github_api.py — GitHub API se issues fetch karo
# Requires GITHUB_TOKEN env variable for 5000 req/hour

import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


async def fetch_issues_for_repos(repos: list[dict]) -> list[dict]:
    """Har repo ke open, unassigned issues fetch karo"""
    all_issues = []

    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as client:
        for repo in repos:
            repo_name = repo["full_name"]
            try:
                # Only open issues + no assignee
                res = await client.get(
                    f"https://api.github.com/repos/{repo_name}/issues",
                    params={"state": "open", "per_page": 50}
                )
                if res.status_code != 200:
                    continue

                for issue in res.json():
                    # PRs bhi /issues endpoint pe aate hain — skip karo
                    if "pull_request" in issue:
                        continue

                    # Sirf unassigned issues
                    if issue.get("assignees"):
                        continue

                    # Check karo /claim system toh nahi hai body mein
                    body = (issue.get("body") or "").lower()
                    if "/claim" in body or "only the issue author" in body:
                        continue

                    all_issues.append({
                        "repo": repo_name,
                        "repo_language": repo.get("language", ""),
                        "number": issue["number"],
                        "title": issue["title"],
                        "url": issue["html_url"],
                        "labels": [l["name"] for l in issue.get("labels", [])],
                        "created_at": issue["created_at"],
                        "body_preview": (issue.get("body") or "")[:200],
                    })

            except Exception as e:
                print(f"[GitHub API] Failed for {repo_name}: {e}")

    return all_issues
