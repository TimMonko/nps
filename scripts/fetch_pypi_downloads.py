"""Fetch napari's monthly PyPI downloads from ClickHouse's public PyPI dataset.

Source: the `pypi.pypi_downloads_per_day` table on sql-clickhouse.clickhouse.com
(user `demo`, no key). Counts every download PyPI logs, so totals are higher
than BigQuery-based numbers such as napari/weather-report's. Only complete
months are kept.

Outputs:
- data/pypi_downloads_monthly.csv (project, month, downloads)
- data/pypi_downloads_by_system_monthly.csv (project, month, system,
  downloads), from `pypi.pypi_downloads_per_day_by_version_by_system`.
  `system` is the OS the installer reports ("Linux", "Windows", "Darwin",
  or "" when unknown). CI and cloud installs are nearly all Linux, so the
  Windows + macOS share tracks people installing on their own machines.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

CLICKHOUSE_URL = "https://sql-clickhouse.clickhouse.com/"
PROJECTS = ("napari",)

QUERY = """
SELECT project, toStartOfMonth(date) AS month, sum(count) AS downloads
FROM pypi.pypi_downloads_per_day
WHERE project IN ({projects}) AND date < toStartOfMonth(today())
GROUP BY project, month
ORDER BY project, month
FORMAT CSVWithNames
"""

QUERY_BY_SYSTEM = """
SELECT project, toStartOfMonth(date) AS month, system, sum(count) AS downloads
FROM pypi.pypi_downloads_per_day_by_version_by_system
WHERE project IN ({projects}) AND date < toStartOfMonth(today())
GROUP BY project, month, system
ORDER BY project, month, system
FORMAT CSVWithNames
"""


def _query(sql: str, projects: tuple[str, ...]) -> pd.DataFrame:
    quoted = ", ".join(f"'{p}'" for p in projects)
    resp = requests.post(
        CLICKHOUSE_URL,
        params={"user": "demo"},
        data=sql.format(projects=quoted).encode(),
        timeout=120,
    )
    resp.raise_for_status()
    return pd.read_csv(io.StringIO(resp.text), parse_dates=["month"], keep_default_na=False)


def fetch_monthly_downloads(projects: tuple[str, ...] = PROJECTS) -> pd.DataFrame:
    return _query(QUERY, projects)


def fetch_monthly_downloads_by_system(projects: tuple[str, ...] = PROJECTS) -> pd.DataFrame:
    return _query(QUERY_BY_SYSTEM, projects)


def main() -> int:
    print("=== Fetching PyPI downloads (ClickHouse) ===", file=sys.stderr, flush=True)
    df = fetch_monthly_downloads()
    path = DATA_DIR / "pypi_downloads_monthly.csv"
    df.to_csv(path, index=False, date_format="%Y-%m-%d")
    for project, g in df.groupby("project"):
        print(
            f"  {project}: {len(g)} months, {g['month'].min():%Y-%m} to "
            f"{g['month'].max():%Y-%m}, {g['downloads'].sum():,} downloads",
            file=sys.stderr,
        )
    print(f"  Saved to {path}", file=sys.stderr)

    by_system = fetch_monthly_downloads_by_system()
    path = DATA_DIR / "pypi_downloads_by_system_monthly.csv"
    by_system.to_csv(path, index=False, date_format="%Y-%m-%d")
    print(f"  Saved to {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
