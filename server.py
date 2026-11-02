from datetime import date, timedelta
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("github-trends")
API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json"}


def _search(q: str, limit: int) -> list[dict]:
    r = httpx.get(
        f"{API}/search/repositories",
        params={"q": q, "sort": "stars", "order": "desc",
                "per_page": min(limit, 30)},
        headers=HEADERS, timeout=15,
    )
    r.raise_for_status()
    return [
        {"name": i["full_name"], "stars": i["stargazers_count"],
         "language": i["language"], "description": i["description"],
         "url": i["html_url"]}
        for i in r.json()["items"]
    ]


@mcp.tool()
def trending(language: str = "", days: int = 7, limit: int = 10) -> list[dict]:
    """New repos from the last N days, ranked by stars."""
    since = (date.today() - timedelta(days=days)).isoformat()
    q = f"created:>{since}"
    if language:
        q += f" language:{language}"
    return _search(q, limit)


@mcp.tool()
def search(query: str, limit: int = 10) -> list[dict]:
    """Search repos by keyword, ranked by stars."""
    return _search(query, limit)


@mcp.tool()
def repo_info(owner: str, name: str) -> dict:
    """Key details about one repository."""
    r = httpx.get(f"{API}/repos/{owner}/{name}", headers=HEADERS, timeout=15)
    r.raise_for_status()
    d = r.json()
    return {"name": d["full_name"], "stars": d["stargazers_count"],
            "forks": d["forks_count"], "open_issues": d["open_issues_count"],
            "language": d["language"], "license": (d["license"] or {}).get("name"),
            "updated": d["pushed_at"], "url": d["html_url"]}


if __name__ == "__main__":
    mcp.run()
