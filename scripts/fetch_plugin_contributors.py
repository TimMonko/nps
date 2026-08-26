"""Fetch plugin contributors from GitHub using `gh api`.

For each plugin repo in github_repos.csv, fetches the contributor list
via `gh api repos/{owner}/{repo}/contributors`.

Output: data/plugin_contributors.csv
Columns: plugin_name, contributor_login, contributions
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

KNOWN_BOT_LOGINS = {
    "app/dependabot",
    "dependabot[bot]",
    "github-actions[bot]",
    "napari-bot",
    "pre-commit-ci[bot]",
    "renovate[bot]",
}
MAX_WORKERS = 5  # Conservative to avoid rate limiting


def _is_bot(login: str) -> bool:
    return login in KNOWN_BOT_LOGINS or login.endswith("[bot]")


def parse_github_url(url: str) -> tuple[str, str] | None:
    """Parse github.com URL -> (owner, repo)."""
    if not isinstance(url, str) or "github.com" not in url:
        return None
    # Handle various URL formats
    parts = url.rstrip("/").split("github.com/")[-1].split("/")
    if len(parts) >= 2:
        owner = parts[0]
        repo = parts[1].rstrip(".git")
        return owner, repo
    return None


def fetch_contributors(owner: str, repo: str) -> list[dict]:
    """Fetch contributors for a single repo via gh api."""
    full_name = f"{owner}/{repo}"
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{full_name}/contributors",
            "--paginate",
            "--slurp",
        ],
        check=False,
        capture_output=True,
        text=False,
        cwd=REPO_ROOT,
    )

    if result.returncode != 0:
        # Repo might be private, deleted, or empty — skip silently
        return []

    # Parse JSON: --slurp returns array of pages
    raw = result.stdout.decode("utf-8", errors="replace")
    try:
        pages = json.loads(raw)
    except json.JSONDecodeError:
        return []

    if not isinstance(pages, list):
        return []

    contributors: list[dict] = []
    seen_logins: set[str] = set()
    for page in pages:
        if not isinstance(page, list):
            continue
        for item in page:
            if not isinstance(item, dict):
                continue
            login = item.get("login")
            if not isinstance(login, str):
                continue
            if login in seen_logins:
                continue
            seen_logins.add(login)
            if _is_bot(login):
                continue
            contributors.append({
                "login": login,
                "contributions": item.get("contributions", 0),
            })

    return contributors


def main() -> int:
    print(
        "=== Phase 1.3: Fetching plugin contributors ===",
        file=sys.stderr,
        flush=True,
    )

    # Load plugin -> github_url mapping
    csv_path = DATA_DIR / "github_repos.csv"
    if not csv_path.exists():
        print(
            "ERROR: github_repos.csv not found. Run github_repos.py first.",
            file=sys.stderr,
        )
        return 1

    df = pd.read_csv(csv_path)
    # Filter to only plugins with GitHub URLs
    df = df[df["github_url"].notna()].copy()
    print(f"  {len(df)} plugins with GitHub URLs", file=sys.stderr, flush=True)

    # Parse owner/repo from URLs
    repos_to_fetch: list[tuple[str, str, str]] = []  # (plugin_name, owner, repo)
    for _, row in df.iterrows():
        parsed = parse_github_url(row["github_url"])
        if parsed:
            repos_to_fetch.append((row["name"], parsed[0], parsed[1]))

    print(f"  {len(repos_to_fetch)} parseable repos", file=sys.stderr, flush=True)

    # Fetch contributors in parallel
    all_rows: list[dict] = []
    failed: list[str] = []
    completed = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {
            executor.submit(fetch_contributors, owner, repo): (name, owner, repo)
            for name, owner, repo in repos_to_fetch
        }

        for future in as_completed(future_map):
            name, owner, repo = future_map[future]
            try:
                contributors = future.result()
                for c in contributors:
                    all_rows.append({
                        "plugin_name": name,
                        "contributor_login": c["login"],
                        "contributions": c.get("contributions", 0),
                    })
            except Exception as e:
                failed.append(f"{owner}/{repo}: {e}")

            completed += 1
            if completed % 50 == 0:
                print(
                    f"  [{completed}/{len(repos_to_fetch)}] repos processed ...",
                    file=sys.stderr,
                    flush=True,
                )

    # Save results
    result_df = pd.DataFrame(all_rows)
    output_path = DATA_DIR / "plugin_contributors.csv"
    result_df.to_csv(output_path, index=False)

    n_plugins = result_df["plugin_name"].nunique()
    n_contributors = result_df["contributor_login"].nunique()
    print(f"\nResults:", file=sys.stderr)
    print(f"  {n_plugins} plugins with contributors", file=sys.stderr)
    print(f"  {n_contributors} unique plugin contributors", file=sys.stderr)
    print(f"  {len(all_rows)} total rows", file=sys.stderr)
    print(f"  Saved to {output_path}", file=sys.stderr)

    if failed:
        print(f"\n  {len(failed)} repos failed (private/deleted/empty):", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
