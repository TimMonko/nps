"""Fetch commit data from GitHub repos using `gh api`.

Uses the pattern from napari PR #9155's check_citation_authors.py for
fast org-wide contributor queries via the gh CLI.

Output: data/commits_{owner}_{repo}.json — list of {login, date, sha}.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TARGET_REPOS = [
    "napari/napari",
    "napari/npe2",
    "napari/docs",
    "napari/napari-plugin-template",
    "napari/napari-plugin-manager",
    "napari/hub-lite",
]

SKIP_REPOS = {
    "napari/npe2api",
    "napari/napari-ghsa-rcqj-87v5-c47r",
}

KNOWN_BOT_LOGINS = {
    "app/dependabot",
    "dependabot[bot]",
    "github-actions[bot]",
    "napari-bot",
    "pre-commit-ci[bot]",
    "renovate[bot]",
}


def _is_bot(login: str) -> bool:
    return login in KNOWN_BOT_LOGINS or login.endswith("[bot]")


def fetch_commits(repo: str) -> list[dict]:
    """Fetch all available commits for a repo via `gh api`.

    Uses --paginate --slurp to get as many pages as GitHub allows
    (typically ~4000 commits).  Returns list of {login, date, sha}.
    """
    print(f"  Fetching commits for {repo} ...", file=sys.stderr, flush=True)
    # per_page is passed as a URL query parameter, not a CLI flag
    # Use text=False (binary) to avoid Windows encoding issues with gh output
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}/commits?per_page=100",
            "--paginate",
            "--slurp",
        ],
        check=False,
        capture_output=True,
        text=False,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip() or "Unknown gh api error."
        raise RuntimeError(
            f"Failed to fetch commits for {repo}: {stderr}"
        )

    # Parse JSON: --slurp returns array of pages, each an array of commits
    raw = result.stdout.decode("utf-8", errors="replace")
    try:
        pages = json.loads(raw)
    except json.JSONDecodeError:
        pages = []

    if not isinstance(pages, list):
        pages = []

    commits: list[dict] = []
    for page in pages:
        if not isinstance(page, list):
            continue
        for item in page:
            if not isinstance(item, dict):
                continue
            author = item.get("author")
            commit = item.get("commit", {}) or {}
            login = None
            if isinstance(author, dict):
                login = author.get("login")
            if not isinstance(login, str):
                # Committer may be a user with no login via API
                committer = commit.get("committer")
                if isinstance(committer, dict):
                    login = committer.get("login")
            if not isinstance(login, str):
                continue

            sha = item.get("sha", "")
            date = None
            if isinstance(commit, dict):
                author_data = commit.get("author") or {}
                if isinstance(author_data, dict):
                    date = author_data.get("date")

            commits.append({
                "login": login,
                "date": date or "",
                "sha": sha or "",
            })

    # Filter bots
    filtered = [
        c for c in commits
        if isinstance(c, dict)
        and isinstance(c.get("login"), str)
        and not _is_bot(c["login"])
    ]
    print(
        f"    Got {len(filtered)} commits ({len(commits) - len(filtered)} bot commits filtered)",
        file=sys.stderr,
        flush=True,
    )
    return filtered


def fetch_org_repos(org: str) -> list[str]:
    """Fetch all non-archived, non-fork repos in a GitHub organization.

    Adapted from check_citation_authors.py in napari PR #9155.
    """
    print(f"  Fetching repos for org {org} ...", file=sys.stderr, flush=True)
    result = subprocess.run(
        ["gh", "api", f"/orgs/{org}/repos", "--paginate", "--slurp"],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "Unknown gh api error."
        raise RuntimeError(f"Failed to fetch org repos: {stderr}")

    payload = json.loads(result.stdout)
    if not isinstance(payload, list):
        raise TypeError("Unexpected GitHub API response for org repos.")

    repos: list[str] = []
    for page in payload:
        if not isinstance(page, list):
            continue
        for item in page:
            if not isinstance(item, dict):
                continue
            if item.get("archived") or item.get("fork"):
                continue
            full_name = item.get("full_name")
            if isinstance(full_name, str):
                repos.append(full_name)
    return sorted(repos)


def save_commits(repo: str, commits: list[dict]) -> Path:
    slug = repo.replace("/", "_")
    path = DATA_DIR / f"commits_{slug}.json"
    path.write_text(json.dumps(commits, indent=2), encoding="utf-8")
    print(f"    Saved to {path}", file=sys.stderr, flush=True)
    return path


def main() -> int:
    print("=== Phase 1.1: Fetching commit data ===", file=sys.stderr, flush=True)

    # Also fetch all napari org repos (includes the 7 targets)
    try:
        org_repos = fetch_org_repos("napari")
        print(
            f"  Found {len(org_repos)} repos in napari org",
            file=sys.stderr,
            flush=True,
        )
    except RuntimeError as e:
        print(f"  Warning: Could not fetch org repos: {e}", file=sys.stderr)
        org_repos = list(TARGET_REPOS)

    # Ensure target repos are included (deduplicate)
    all_repos = list(dict.fromkeys(TARGET_REPOS + org_repos))

    # Filter out unwanted repos
    skipped = [r for r in all_repos if r in SKIP_REPOS]
    all_repos = [r for r in all_repos if r not in SKIP_REPOS]
    if skipped:
        print(
            f"  Skipped {len(skipped)} repos: {', '.join(skipped)}",
            file=sys.stderr,
            flush=True,
        )

    print(f"  Total repos to fetch: {len(all_repos)}", file=sys.stderr, flush=True)

    failed: list[str] = []
    for i, repo in enumerate(all_repos, 1):
        print(
            f"\n[{i}/{len(all_repos)}] {repo}",
            file=sys.stderr,
            flush=True,
        )
        try:
            commits = fetch_commits(repo)
            save_commits(repo, commits)
        except RuntimeError as e:
            print(f"  FAILED: {e}", file=sys.stderr, flush=True)
            failed.append(repo)
        # Small delay to avoid hammering the API
        time.sleep(0.3)

    if failed:
        print(f"\nFailed repos ({len(failed)}):", file=sys.stderr)
        for r in failed:
            print(f"  - {r}", file=sys.stderr)
        return 1

    print("\nDone! All repos fetched successfully.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
