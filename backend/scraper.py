# scraper.py — GSSoC projects list fetch karo
# GSSoC page JS-rendered hai, isliye known repo list use kar rahe hain
# Production mein: Playwright se dynamic scrape karo

import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# GSSoC 2026 accepted repos (sample — add more from gssoc.girlscript.org/projects)
GSSOC_REPOS = [
    "Team-NoxVeil/InterXAI",
    "Checkora/Checkora",
    "prajwalsuryawanshi/agentapi",
    "EnvForge/EnvForge",
    "iloveAgents/iloveAgents",
    "AegisAI/AegisAI",
]


async def get_gssoc_repos() -> list[dict]:
    """
    Repo list return karo with basic metadata.
    Production mein Playwright se gssoc.girlscript.org/projects scrape karo.
    """
    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as client:
        repos = []
        for repo_path in GSSOC_REPOS:
            try:
                res = await client.get(f"https://api.github.com/repos/{repo_path}")
                if res.status_code == 200:
                    data = res.json()
                    repos.append({
                        "full_name": data["full_name"],
                        "description": data.get("description", ""),
                        "language": data.get("language", ""),
                        "topics": data.get("topics", []),
                        "open_issues": data.get("open_issues_count", 0),
                    })
            except Exception as e:
                print(f"[Scraper] Failed for {repo_path}: {e}")
        return repos
