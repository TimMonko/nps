"""Compute velocity: commits merged per month.

Runs LAST because it may make many API calls to collect PR merge data.
Uses `gh api` to fetch PR merge dates for each repo.

Output: data/metrics/velocity.csv — commits per month, org-wide + per-repo.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
METRICS_DIR = DATA_DIR / "metrics"
METRICS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_REPOS = [
    "napari/napari",
    "napari/npe2",
    "napari/npe2api",
    "napari/docs",
    "napari/napari-plugin-template",
    "napari/napari-plugin-manager",
    "napari/hub-lite",
]


def fetch_pr_merge_dates(repo: str) -> list[dict]:
    """Fetch merged PR merge dates via gh api.

    Uses the search API for merged PRs, sorted by merge date.
    Limited to last ~1000 PRs per repo.
    """
    print(f"  Fetching merged PRs for {repo} ...", file=sys.stderr, flush=True)
    # GitHub search: merged PRs sorted by merged date (most recent first)
    query = f"repo:{repo} is:pr is:merged"
    result = subprocess.run(
        [
            "gh", "search", "prs", query,
            "--sort", "created",
            "--order", "asc",
            "--limit", "1000",
            "--json", "number,mergedAt,createdAt,author",
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() or "Unknown error"
        raise RuntimeError(f"gh search prs failed for {repo}: {stderr}")

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    if not isinstance(prs, list):
        return []

    return [
        {
            "repo": repo,
            "number": pr.get("number"),
            "merged_at": pr.get("mergedAt"),
            "created_at": pr.get("createdAt"),
            "author": (
                pr["author"]["login"]
                if isinstance(pr.get("author"), dict)
                else None
            ),
        }
        for pr in prs
        if pr.get("mergedAt")
    ]


def compute_velocity(prs: pd.DataFrame) -> pd.DataFrame:
    """Compute PRs merged per month, org-wide and per-repo."""
    prs["merged_at"] = pd.to_datetime(prs["merged_at"], utc=True)
    prs["month"] = prs["merged_at"].dt.to_period("M")

    # Org-wide
    org_velocity = (
        prs.groupby("month")
        .size()
        .reset_index(name="prs_merged_org")
    )
    org_velocity["month"] = org_velocity["month"].dt.to_timestamp()

    # Per-repo
    per_repo = (
        prs.groupby(["month", "repo"])
        .size()
        .reset_index(name="prs_merged")
    )
    per_repo["month"] = per_repo["month"].dt.to_timestamp()
    per_repo_pivot = per_repo.pivot(
        index="month", columns="repo", values="prs_merged"
    ).fillna(0).astype(int)

    # Combine
    result = org_velocity.merge(
        per_repo_pivot, on="month", how="left"
    ).fillna(0)
    return result.sort_values("month")


def compute_velocity_from_commits() -> pd.DataFrame:
    """Fallback: compute velocity from commit data instead of PRs.

    Uses the already-fetched commit JSON files.
    """
    frames: list[pd.DataFrame] = []
    for fpath in sorted(DATA_DIR.glob("commits_*.json")):
        repo_slug = fpath.stem.replace("commits_", "").replace("_", "/", 1)
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not data:
            continue
        df = pd.DataFrame(data)
        df["repo"] = repo_slug
        frames.append(df)

    if not frames:
        raise RuntimeError("No commit data found.")

    commits = pd.concat(frames, ignore_index=True)
    commits["date"] = pd.to_datetime(commits["date"], utc=True)
    commits["month"] = commits["date"].dt.to_period("M")

    # Org-wide
    org_velocity = (
        commits.groupby("month")
        .size()
        .reset_index(name="commits_org")
    )
    org_velocity["month"] = org_velocity["month"].dt.to_timestamp()

    # Per-repo
    per_repo = (
        commits.groupby(["month", "repo"])
        .size()
        .reset_index(name="commits")
    )
    per_repo["month"] = per_repo["month"].dt.to_timestamp()
    per_repo_pivot = per_repo.pivot(
        index="month", columns="repo", values="commits"
    ).fillna(0).astype(int)
    per_repo_pivot.columns = [f"commits_{c.replace('/', '_')}" for c in per_repo_pivot.columns]

    result = org_velocity.merge(
        per_repo_pivot, on="month", how="left"
    ).fillna(0)
    return result.sort_values("month")


def main() -> int:
    print(
        "=== Velocity: Commits per month (LAST — many API calls) ===",
        file=sys.stderr,
        flush=True,
    )

    # Try PR-based velocity first, fall back to commit-based
    print("\nUsing commit-based velocity (already-fetched data) ...", file=sys.stderr)
    velocity = compute_velocity_from_commits()

    velocity.to_csv(METRICS_DIR / "velocity.csv", index=False)
    print(
        f"  {len(velocity)} months -> {METRICS_DIR / 'velocity.csv'}"
    )

    # Summary
    if not velocity.empty:
        recent = velocity[velocity["month"] >= "2026-01-01"]
        if not recent.empty:
            avg_commits = recent["commits_org"].mean()
            print(
                f"  Avg commits/month since Jan 2026: {avg_commits:.0f}",
                file=sys.stderr,
            )

    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
