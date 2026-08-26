"""Compute contributor metrics from commit data.

Reads data/commits_*.json files produced by fetch_contributors.py.
Outputs data/metrics_contributors.csv with monthly aggregations.

Metrics:
- new_contributors: count of first-time contributors per month (org-wide)
- new_contributors_{repo}: per-repo first-time contributors per month
- retention_Nmo: proportion of a cohort that returns after N months
- returning_rate: fraction of contributors who make >1 commit overall
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "metrics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_REPOS = [
    "napari/napari",
    "napari/npe2",
    "napari/npe2api",
    "napari/docs",
    "napari/napari-plugin-template",
    "napari/napari-plugin-manager",
    "napari/hub-lite",
]

# Repos to exclude — e.g. security advisory mirrors that duplicate commits
EXCLUDED_REPOS = {"napari/napari-ghsa-rcqj-87v5-c47r"}


def load_all_commits() -> pd.DataFrame:
    """Load all commit JSON files into a single DataFrame."""
    frames: list[pd.DataFrame] = []
    for fpath in sorted(DATA_DIR.glob("commits_*.json")):
        repo_slug = fpath.stem.replace("commits_", "").replace("_", "/", 1)
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print(f"  Warning: Could not read {fpath}", file=sys.stderr)
            continue

        if not data:
            continue

        df = pd.DataFrame(data)
        df["repo"] = repo_slug
        frames.append(df)

    if not frames:
        raise RuntimeError("No commit data found. Run fetch_contributors.py first.")

    commits = pd.concat(frames, ignore_index=True)
    commits["date"] = pd.to_datetime(commits["date"], utc=True)
    commits["login"] = commits["login"].str.lower().str.strip()

    # Exclude repos that contaminate the data (e.g. security advisory mirrors)
    n_before = len(commits)
    commits = commits[~commits["repo"].isin(EXCLUDED_REPOS)]
    n_excluded = n_before - len(commits)
    if n_excluded:
        print(f"  Excluded {n_excluded} commits from {EXCLUDED_REPOS}", file=sys.stderr)

    commits = commits.drop_duplicates(subset=["sha"])
    commits = commits.sort_values("date")

    print(
        f"  Loaded {len(commits):,} commits from {len(frames)} repos",
        file=sys.stderr,
    )
    print(
        f"  {commits['login'].nunique():,} unique contributors",
        file=sys.stderr,
    )
    print(
        f"  Date range: {commits['date'].min().date()} to {commits['date'].max().date()}",
        file=sys.stderr,
    )
    return commits


def compute_first_commit_date(
    commits: pd.DataFrame, repo: str | None = None
) -> pd.DataFrame:
    """Compute each contributor's first commit date.

    If repo is provided, scope to that repo. Otherwise, org-wide.
    """
    subset = commits if repo is None else commits[commits["repo"] == repo]
    if subset.empty:
        return pd.DataFrame(columns=["login", "first_commit"])

    first = (
        subset.groupby("login")["date"]
        .min()
        .reset_index()
        .rename(columns={"date": "first_commit"})
    )
    return first


def compute_monthly_new_contributors(
    commits: pd.DataFrame,
) -> pd.DataFrame:
    """Compute new contributors per month (org-wide)."""
    first = compute_first_commit_date(commits)
    first["month"] = first["first_commit"].dt.to_period("M")
    monthly = (
        first.groupby("month")
        .size()
        .reset_index(name="new_contributors")
    )
    monthly["month"] = monthly["month"].dt.to_timestamp()
    return monthly.sort_values("month")


def compute_monthly_new_per_repo(
    commits: pd.DataFrame,
) -> pd.DataFrame:
    """Compute new contributors per month, per target repo."""
    frames: list[pd.DataFrame] = []
    for repo in TARGET_REPOS:
        if repo not in commits["repo"].values:
            continue
        first = compute_first_commit_date(commits, repo=repo)
        first["month"] = first["first_commit"].dt.to_period("M")
        monthly = (
            first.groupby("month")
            .size()
            .reset_index(name=f"new_contributors_{repo.replace('/', '_')}")
        )
        monthly["month"] = monthly["month"].dt.to_timestamp()
        frames.append(monthly)

    if not frames:
        return pd.DataFrame()

    result = frames[0]
    for df in frames[1:]:
        result = result.merge(df, on="month", how="outer")
    return result.sort_values("month").fillna(0)


def compute_retention(
    commits: pd.DataFrame, retention_months: tuple[int, ...] = (1, 3, 6)
) -> pd.DataFrame:
    """Compute new-contributor retention rates by cohort month.

    For each monthly cohort of first-time contributors, compute the
    proportion that make ≥1 additional commit within N months.

    Returns DataFrame with columns: cohort_month, n_new, retention_{N}mo
    """
    first = compute_first_commit_date(commits)
    first = first.rename(columns={"first_commit": "first_date"})

    # Merge to get all commits with their author's first-commit date
    merged = commits[["login", "date"]].merge(first, on="login", how="inner")

    # Only consider commits after the first commit
    subsequent = merged[merged["date"] > merged["first_date"]].copy()

    # Assign each contributor to a monthly cohort
    first["cohort_month"] = first["first_date"].dt.to_period("M")

    rows: list[dict] = []
    cohorts = sorted(first["cohort_month"].unique())

    for cohort in cohorts:
        cohort_first = first[first["cohort_month"] == cohort]
        cohort_logins = set(cohort_first["login"])
        n_new = len(cohort_logins)

        row = {
            "cohort_month": cohort.to_timestamp(),
            "n_new": n_new,
        }

        cohort_subsequent = subsequent[
            subsequent["login"].isin(cohort_logins)
        ].copy()

        for n_months in retention_months:
            cutoff = pd.Timestamp(cohort.to_timestamp(), tz="UTC") + pd.DateOffset(months=n_months)
            # Contributors with ≥1 subsequent commit within N months
            within_window = cohort_subsequent[
                cohort_subsequent["date"] <= cutoff
            ]
            returning = within_window["login"].nunique()
            row[f"retention_{n_months}mo"] = (
                returning / n_new if n_new > 0 else 0.0
            )

        rows.append(row)

    return pd.DataFrame(rows).sort_values("cohort_month")


def compute_all_contributor_counts(
    commits: pd.DataFrame,
) -> pd.DataFrame:
    """Compute cumulative total contributors over time."""
    first = compute_first_commit_date(commits)
    first = first.sort_values("first_commit")
    first["total_contributors"] = range(1, len(first) + 1)
    return first[["first_commit", "login", "total_contributors"]]


def compute_active_contributors(
    commits: pd.DataFrame, trailing_months: int = 6
) -> pd.DataFrame:
    """Compute active contributors per month.

    For each month, count unique contributors with ≥1 commit in
    the trailing N-month window ending at that month.
    """
    commits = commits.copy()
    commits["month"] = commits["date"].dt.to_period("M")
    months = pd.period_range(
        commits["month"].min(), commits["month"].max(), freq="M"
    )

    rows: list[dict] = []
    for m in months:
        window_start = pd.Timestamp((m - trailing_months + 1).to_timestamp(how="start"), tz="UTC")
        window_end = pd.Timestamp(m.to_timestamp(how="end"), tz="UTC")
        in_window = commits[
            (commits["date"] >= window_start)
            & (commits["date"] <= window_end)
        ]
        n_active = in_window["login"].nunique()
        rows.append({
            "month": m.to_timestamp(),
            "active_contributors": n_active,
        })

    return pd.DataFrame(rows)


def compute_annual_contributors(commits: pd.DataFrame) -> pd.DataFrame:
    """Count unique contributors active per calendar year."""
    commits = commits.copy()
    commits["year"] = commits["date"].dt.year
    yearly = (
        commits.groupby("year")["login"]
        .nunique()
        .reset_index(name="active_contributors")
        .sort_values("year")
    )
    return yearly


def compute_new_vs_returning(commits: pd.DataFrame) -> pd.DataFrame:
    """For each year, split active contributors into new vs returning.

    New = first commit ever was in this year.
    Returning = had commits in any prior year.
    """
    commits = commits.copy()
    commits["year"] = commits["date"].dt.year
    first_year = (
        commits.groupby("login")["year"].min().reset_index(name="first_year")
    )
    yearly = (
        commits.groupby("year")["login"]
        .nunique()
        .reset_index(name="total")
        .sort_values("year")
    )
    # Merge first_year info
    yearly = yearly.merge(
        first_year.groupby("first_year").size().reset_index(name="new"),
        left_on="year", right_on="first_year", how="left",
    ).fillna(0)
    yearly["new"] = yearly["new"].astype(int)
    yearly["returning"] = yearly["total"] - yearly["new"]
    return yearly[["year", "total", "new", "returning"]]


def main() -> int:
    print(
        "=== Phase 2.1: Computing contributor metrics ===",
        file=sys.stderr,
        flush=True,
    )

    commits = load_all_commits()

    # 1. New contributors per month (org-wide)
    print("\nComputing monthly new contributors ...", file=sys.stderr)
    monthly = compute_monthly_new_contributors(commits)
    monthly.to_csv(OUTPUT_DIR / "new_contributors_monthly.csv", index=False)
    print(f"  {len(monthly)} months -> {OUTPUT_DIR / 'new_contributors_monthly.csv'}")

    # 2. Per-repo breakdown
    print("\nComputing per-repo new contributors ...", file=sys.stderr)
    per_repo = compute_monthly_new_per_repo(commits)
    if not per_repo.empty:
        per_repo.to_csv(OUTPUT_DIR / "new_contributors_per_repo.csv", index=False)
        print(f"  {len(per_repo)} months -> {OUTPUT_DIR / 'new_contributors_per_repo.csv'}")
    else:
        print("  No per-repo data computed.", file=sys.stderr)

    # 3. Retention
    print("\nComputing retention rates ...", file=sys.stderr)
    retention = compute_retention(commits)
    retention.to_csv(OUTPUT_DIR / "retention.csv", index=False)
    print(f"  {len(retention)} cohorts -> {OUTPUT_DIR / 'retention.csv'}")

    # 4. Cumulative counts
    print("\nComputing cumulative contributor counts ...", file=sys.stderr)
    cumulative = compute_all_contributor_counts(commits)
    cumulative.to_csv(OUTPUT_DIR / "cumulative_contributors.csv", index=False)
    print(f"  {len(cumulative)} contributors -> {OUTPUT_DIR / 'cumulative_contributors.csv'}")

    # 5. Active contributors (trailing 6-month window)
    print("\nComputing active contributors ...", file=sys.stderr)
    active = compute_active_contributors(commits)
    active.to_csv(OUTPUT_DIR / "active_contributors.csv", index=False)
    print(f"  {len(active)} months -> {OUTPUT_DIR / 'active_contributors.csv'}")
    if not active.empty:
        print(f"  Latest: {active['active_contributors'].iloc[-1]} active contributors", file=sys.stderr)

    # 6. Annual active contributors
    print("\nComputing annual contributor counts ...", file=sys.stderr)
    annual = compute_annual_contributors(commits)
    annual.to_csv(OUTPUT_DIR / "annual_contributors.csv", index=False)
    print(f"  {len(annual)} years -> {OUTPUT_DIR / 'annual_contributors.csv'}")

    # 7. New vs returning contributors
    print("\nComputing new vs returning contributors ...", file=sys.stderr)
    breakdown = compute_new_vs_returning(commits)
    breakdown.to_csv(OUTPUT_DIR / "new_vs_returning.csv", index=False)
    print(f"  {len(breakdown)} years -> {OUTPUT_DIR / 'new_vs_returning.csv'}")

    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
