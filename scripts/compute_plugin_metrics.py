"""Compute plugin ecosystem metrics.

Reads data/plugin_releases.csv from fetch_plugin_data.py.
Outputs data/metrics/plugin_metrics.csv.

Metrics:
- new_plugins: count of plugins with first release in each month
- active_plugins: plugins with ≥1 release in trailing 6 months
- total_plugins: cumulative total plugins ever released
- maintenance_ratio: active_plugins / total_plugins
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "metrics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_plugin_data() -> pd.DataFrame:
    """Load plugin release data."""
    path = DATA_DIR / "plugin_releases.csv"
    if not path.exists():
        raise RuntimeError(
            "plugin_releases.csv not found. Run fetch_plugin_data.py first."
        )
    df = pd.read_csv(path, parse_dates=["first_release", "latest_release"])
    df["first_release"] = pd.to_datetime(df["first_release"], utc=True)
    df["latest_release"] = pd.to_datetime(df["latest_release"], utc=True)
    print(f"  Loaded {len(df)} plugins", file=sys.stderr)
    with_dates = df["first_release"].notna().sum()
    print(f"  {with_dates} with known first-release date", file=sys.stderr)
    return df


def compute_new_plugins_per_month(df: pd.DataFrame) -> pd.DataFrame:
    """Count new plugins (first PyPI release) per month."""
    with_dates = df[df["first_release"].notna()].copy()
    with_dates["month"] = with_dates["first_release"].dt.to_period("M")
    monthly = (
        with_dates.groupby("month")
        .size()
        .reset_index(name="new_plugins")
    )
    monthly["month"] = monthly["month"].dt.to_timestamp()
    return monthly.sort_values("month")


def compute_maintenance_metrics(
    df: pd.DataFrame, trailing_months: int = 6
) -> pd.DataFrame:
    """Compute plugin maintenance metrics over time.

    For each month, compute:
    - total_plugins: cumulative plugins with first release ≤ that month
    - active_plugins: plugins with latest release within trailing window
    - maintenance_ratio: active / total
    """
    with_dates = df[df["first_release"].notna()].copy()

    if with_dates.empty:
        return pd.DataFrame()

    # Build a monthly time series
    min_date = with_dates["first_release"].min()
    max_date = max(
        with_dates["latest_release"].max(),
        pd.Timestamp.now(tz="UTC"),
    )
    months = pd.date_range(min_date, max_date, freq="MS")

    rows: list[dict] = []
    for m in months:
        total = (with_dates["first_release"] <= m).sum()
        # Active = latest release within [m - trailing_months, m]
        window_start = m - pd.DateOffset(months=trailing_months)
        active = (
            (with_dates["latest_release"] >= window_start)
            & (with_dates["latest_release"] <= m + pd.DateOffset(months=1))
        ).sum()
        rows.append({
            "month": m,
            "total_plugins": total,
            "active_plugins": active,
            "maintenance_ratio": active / total if total > 0 else 0.0,
        })

    result = pd.DataFrame(rows)
    return result


def main() -> int:
    print(
        "=== Phase 2.2: Computing plugin metrics ===",
        file=sys.stderr,
        flush=True,
    )

    df = load_plugin_data()

    # 1. New plugins per month
    print("\nComputing new plugins per month ...", file=sys.stderr)
    new_monthly = compute_new_plugins_per_month(df)
    new_monthly.to_csv(OUTPUT_DIR / "new_plugins_monthly.csv", index=False)
    print(
        f"  {len(new_monthly)} months → {OUTPUT_DIR / 'new_plugins_monthly.csv'}"
    )
    if not new_monthly.empty:
        print(
            f"  Peak: {new_monthly['new_plugins'].max()} new plugins in "
            f"{new_monthly.loc[new_monthly['new_plugins'].idxmax(), 'month'].date()}",
            file=sys.stderr,
        )

    # 2. Maintenance metrics
    print("\nComputing maintenance metrics ...", file=sys.stderr)
    maintenance = compute_maintenance_metrics(df)
    maintenance.to_csv(OUTPUT_DIR / "plugin_maintenance.csv", index=False)
    print(
        f"  {len(maintenance)} months → {OUTPUT_DIR / 'plugin_maintenance.csv'}"
    )
    if not maintenance.empty:
        last = maintenance.iloc[-1]
        print(
            f"  Latest: {last['active_plugins']} active / {last['total_plugins']} total "
            f"({last['maintenance_ratio']:.1%})",
            file=sys.stderr,
        )

    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
