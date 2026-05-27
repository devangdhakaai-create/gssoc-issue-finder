# main.py — FastAPI app entry point
# Run: uvicorn main:app --reload

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from github_api import fetch_issues_for_repos
from scraper import get_gssoc_repos
from filters import filter_issues

app = FastAPI(title="GSSoC Issue Finder")

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache (replace with PostgreSQL for persistence)
_cache: dict = {"repos": [], "issues": []}


@app.get("/")
def root():
    return {"status": "GSSoC Issue Finder running ✅"}


@app.get("/refresh")
async def refresh():
    """Scrape GSSoC projects + fetch GitHub issues → store in cache"""
    repos = await get_gssoc_repos()          # Step 1: GSSoC page se repos fetch
    issues = await fetch_issues_for_repos(repos)  # Step 2: GitHub API se issues
    _cache["repos"] = repos
    _cache["issues"] = issues
    return {"repos_found": len(repos), "issues_found": len(issues)}


@app.get("/issues")
def get_issues(
    skills: Optional[str] = Query(None, description="Comma separated: python,react,fastapi"),
    difficulty: Optional[str] = Query(None, description="beginner/intermediate/advanced"),
    label: Optional[str] = Query(None, description="Filter by label e.g. bug,feature"),
):
    """
    Return filtered issues.
    ?skills=python,react  ?difficulty=beginner  ?label=bug
    """
    issues = _cache["issues"]
    if not issues:
        return {"message": "No data yet. Call /refresh first.", "issues": []}

    skill_list = [s.strip().lower() for s in skills.split(",")] if skills else []
    filtered = filter_issues(issues, skill_list, difficulty, label)
    return {"total": len(filtered), "issues": filtered}
