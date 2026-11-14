"""Retrieve repositories with timeouts and explicit API errors."""

import requests


def get_all_repos(github_token: str) -> list[str]:
    repos = []
    page = 1
    with requests.Session() as session:
        session.headers.update({"Authorization": f"Bearer {github_token}"})
        while True:
            response = session.get(
                "https://api.github.com/user/repos",
                params={"per_page": 100, "page": page},
                timeout=15,
            )
            response.raise_for_status()
            batch = response.json()
            if not batch:
                break
            repos.extend(repo["name"] for repo in batch)
            page += 1
    return repos
