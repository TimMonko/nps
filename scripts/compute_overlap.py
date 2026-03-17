"""Compute overlap: new org contributors who are also plugin developers.

Reads contributor metrics and plugin contributor data.
Outputs data/metrics/overlap.csv — per cohort month, what proportion
of new org contributors also appear in ≥1 plugin repo.

A "plugin developer" is defined as someone who has ≥1 commit in any
napari plugin's GitHub repo (from plugin_contributors.csv).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
METRICS_DIR = DATA_DIR / "metrics"
METRICS_DIR.mkdir(parents=True, exist_ok=True)


def load_plugin_contributor_set() -> set[str]:
    """Load the set of all plugin contributor logins."""
    path = DATA_DIR / "plugin_contributors.csv"
    if not path.exists():
        print(
            "  Warning: plugin_contributors.csv not found. "
            "Run fetch_plugin_contributors.py first.",
            file=sys.stderr,
        )
        return set()
    df = pd.read_csv(path)
    logins = set(df["contributor_login"].str.lower().str.strip())
    print(f"  Loaded {len(logins):,} unique plugin contributors", file=sys.stderr)
    return logins


def compute_overlap(
    plugin_contributors: set[str],
) -> pd.DataFrame:
    """Compute per-cohort overlap between org and plugin contributors.

    Uses cumulative_contributors.csv to know who joined when, then
    checks each contributor against the plugin contributor set.
    """
    cumulative_path = METRICS_DIR / "cumulative_contributors.csv"
    if not cumulative_path.exists():
        raise RuntimeError(
            "cumulative_contributors.csv not found. "
            "Run compute_contributor_metrics.py first."
        )

    contribs = pd.read_csv(cumulative_path, parse_dates=["first_commit"])
    contribs["login"] = contribs["login"].str.lower().str.strip()

    if contribs.empty:
        return pd.DataFrame()

    # Mark each contributor as plugin developer or not
    contribs["is_plugin_dev"] = contribs["login"].isin(plugin_contributors)

    # Group by month
    contribs["month"] = contribs["first_commit"].dt.to_period("M")

    monthly = (
        contribs.groupby("month")
        .agg(
            n_new=("login", "count"),
            n_plugin_devs=("is_plugin_dev", "sum"),
        )
        .reset_index()
    )
    monthly["month"] = monthly["month"].dt.to_timestamp()
    monthly["plugin_dev_ratio"] = (
        monthly["n_plugin_devs"] / monthly["n_new"]
    )
    monthly = monthly.sort_values("month")

    return monthly


def compute_total_overlap(
    plugin_contributors: set[str],
) -> dict:
    """Compute total (not just new) overlap stats.

    Returns:
        n_org: total unique org contributors
        n_plugin_devs_in_org: how many of those are also plugin devs
        total_plugin_dev_ratio: n_plugin_devs_in_org / n_org
    """
    cumulative_path = METRICS_DIR / "cumulative_contributors.csv"
    if not cumulative_path.exists():
        raise RuntimeError(
            "cumulative_contributors.csv not found. "
            "Run compute_contributor_metrics.py first."
        )

    contribs = pd.read_csv(cumulative_path, parse_dates=["first_commit"])
    contribs["login"] = contribs["login"].str.lower().str.strip()

    n_org = len(contribs)
    n_plugin_devs_in_org = contribs["login"].isin(plugin_contributors).sum()
    total_plugin_dev_ratio = n_plugin_devs_in_org / n_org if n_org > 0 else 0.0

    # Also compute cumulative proportion over time
    contribs = contribs.sort_values("first_commit")
    contribs["is_plugin_dev"] = contribs["login"].isin(plugin_contributors)
    contribs["cumulative_plugin_devs"] = contribs["is_plugin_dev"].cumsum()
    contribs["cumulative_total"] = range(1, len(contribs) + 1)
    contribs["cumulative_plugin_dev_ratio"] = (
        contribs["cumulative_plugin_devs"] / contribs["cumulative_total"]
    )

    return {
        "n_org": n_org,
        "n_plugin_devs_in_org": n_plugin_devs_in_org,
        "total_plugin_dev_ratio": total_plugin_dev_ratio,
        "cumulative": contribs[["first_commit", "cumulative_plugin_dev_ratio"]],
    }


def compute_active_plugin_devs(
    plugin_contributors: set[str],
) -> pd.DataFrame:
    """Compute active plugin devs per month.

    Reads active_contributors.csv and filters each month's active set
    to only those also in the plugin contributor list.
    """
    active_path = METRICS_DIR / "active_contributors.csv"
    if not active_path.exists():
        print("  Warning: active_contributors.csv not found", file=sys.stderr)
        return pd.DataFrame()

    # Load all commits to determine who was active each month
    frames: list[pd.DataFrame] = []
    for fpath in sorted((Path(__file__).resolve().parent.parent / "data").glob("commits_*.json")):
        import json
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not data:
            continue
        repo_slug = fpath.stem.replace("commits_", "").replace("_", "/", 1)
        df = pd.DataFrame(data)
        df["repo"] = repo_slug
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    commits = pd.concat(frames, ignore_index=True)
    commits["date"] = pd.to_datetime(commits["date"], utc=True)
    commits["login"] = commits["login"].str.lower().str.strip()
    commits = commits[~commits["repo"].isin({"napari/napari-ghsa-rcqj-87v5-c47r"})]
    commits = commits.drop_duplicates(subset=["sha"])

    months = pd.period_range(
        commits["date"].dt.to_period("M").min(),
        commits["date"].dt.to_period("M").max(),
        freq="M",
    )

    rows: list[dict] = []
    for m in months:
        window_start = pd.Timestamp((m - 5).to_timestamp(how="start"), tz="UTC")  # 6-month trailing
        window_end = pd.Timestamp(m.to_timestamp(how="end"), tz="UTC")
        in_window = commits[
            (commits["date"] >= window_start) & (commits["date"] <= window_end)
        ]
        active_logins = set(in_window["login"].unique())
        n_active_plugin_devs = len(active_logins & plugin_contributors)
        rows.append({
            "month": m.to_timestamp(),
            "active_plugin_devs": n_active_plugin_devs,
        })

    return pd.DataFrame(rows)


def main() -> int:
    print(
        "=== Phase 2.3: Computing plugin-developer overlap ===",
        file=sys.stderr,
        flush=True,
    )

    plugin_devs = load_plugin_contributor_set()

    if not plugin_devs:
        print("  No plugin contributor data — skipping overlap.", file=sys.stderr)
        return 0

    # 1. Per-cohort overlap (new contributors)
    overlap = compute_overlap(plugin_devs)
    overlap.to_csv(METRICS_DIR / "overlap.csv", index=False)
    print(
        f"\n  {len(overlap)} months → {METRICS_DIR / 'overlap.csv'}"
    )
    if not overlap.empty:
        recent = overlap[overlap["month"] >= "2026-01-01"]
        if not recent.empty:
            avg_ratio = recent["plugin_dev_ratio"].mean()
            print(
                f"  Since Jan 2026: {avg_ratio:.1%} of new contributors "
                f"are also plugin developers",
                file=sys.stderr,
            )

    # 2. Total overlap (all contributors, not just new)
    total = compute_total_overlap(plugin_devs)
    total["cumulative"].to_csv(METRICS_DIR / "cumulative_plugin_dev_ratio.csv", index=False)
    print(
        f"\n  Total org contributors: {total['n_org']}",
        file=sys.stderr,
    )
    print(
        f"  Plugin devs among them: {total['n_plugin_devs_in_org']} "
        f"({total['total_plugin_dev_ratio']:.1%})",
        file=sys.stderr,
    )

    # 3. Active plugin devs
    print("\nComputing active plugin developers ...", file=sys.stderr)
    active = compute_active_plugin_devs(plugin_devs)
    if not active.empty:
        active.to_csv(METRICS_DIR / "active_plugin_devs.csv", index=False)
        print(f"  {len(active)} months → {METRICS_DIR / 'active_plugin_devs.csv'}")
        print(f"  Latest: {active['active_plugin_devs'].iloc[-1]} active plugin devs", file=sys.stderr)

    # 4. New plugin developers (first-time org contributors who are plugin devs)
    # Already in overlap.csv as n_plugin_devs
    print("\n  New plugin devs data already in overlap.csv", file=sys.stderr)

    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
