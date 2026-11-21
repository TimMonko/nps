"""Fetch plugin release dates from npe2api and PyPI.

Downloads npe2api extended_summary, then queries PyPI JSON API per
plugin for the upload time of every release.

Outputs:
  data/plugin_releases.csv  one row per plugin
      (name, first_release, latest_release, n_versions, github_url, ...)
  data/plugin_versions.csv  one row per release (name, version, upload_time)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

NPE2API_EXTENDED_SUMMARY = (
    "https://raw.githubusercontent.com/napari/npe2api/main/"
    "public/extended_summary.json"
)


def download_extended_summary() -> list[dict]:
    """Download extended_summary.json from npe2api.

    Falls back to local cached copy if download fails.
    """
    local_path = DATA_DIR / "extended_summary.json"
    print("Downloading extended_summary.json ...", file=sys.stderr, flush=True)
    try:
        resp = requests.get(NPE2API_EXTENDED_SUMMARY, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        local_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"  Saved to {local_path}", file=sys.stderr, flush=True)
        return data
    except Exception as e:
        print(f"  Download failed: {e}", file=sys.stderr)
        if local_path.exists():
            print(f"  Using cached {local_path}", file=sys.stderr)
            return json.loads(local_path.read_text(encoding="utf-8"))
        raise RuntimeError(
            "Could not download extended_summary.json and no cache found."
        ) from e


def fetch_pypi_versions(pypi_name: str) -> list[tuple[str, str]]:
    """Fetch (version, upload_time) for every release from the PyPI JSON API.

    The upload time is that of the release's first file, as an ISO 8601
    string like "2020-03-15T10:30:00" (UTC). Sorted oldest first.
    """
    url = f"https://pypi.org/pypi/{pypi_name}/json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"    Warning: {pypi_name}: {e}", file=sys.stderr)
        return []

    releases = data.get("releases", {})
    if not releases:
        return []

    # Filter out empty releases and get upload times
    dated_versions: list[tuple[str, str]] = []
    for version, files in releases.items():
        if not files:
            continue
        for f in files:
            upload_time = f.get("upload_time")
            if upload_time:
                dated_versions.append((version, upload_time))
                break  # just need first upload for each version

    dated_versions.sort(key=lambda x: x[1])
    return dated_versions


def load_github_repos_csv() -> dict[str, str]:
    """Load github_repos.csv -> {plugin_name: github_url}."""
    csv_path = DATA_DIR / "github_repos.csv"
    if not csv_path.exists():
        print(
            "  github_repos.csv not found — run github_repos.py first.",
            file=sys.stderr,
        )
        return {}
    df = pd.read_csv(csv_path)
    return dict(
        zip(df["name"].str.lower(), df["github_url"].where(df["github_url"].notna(), None))
    )


def main() -> int:
    print("=== Phase 1.2: Fetching plugin release data ===", file=sys.stderr, flush=True)

    # 1. Get plugin list
    plugins = download_extended_summary()
    print(f"  {len(plugins)} plugins in extended_summary", file=sys.stderr, flush=True)

    # 2. Rebuild github_repos.csv from the summary just downloaded (otherwise
    #    plugins new since the last run have no repo and skip template checks)
    import runpy

    runpy.run_path(str(Path(__file__).with_name("github_repos.py")))
    github_map = load_github_repos_csv()
    print(f"  {len(github_map)} plugins in github_repos.csv", file=sys.stderr, flush=True)

    # 3. Fetch PyPI release dates for each plugin
    rows: list[dict] = []
    version_rows: list[dict] = []
    total = len(plugins)
    for i, plugin in enumerate(plugins, 1):
        name = plugin.get("name", "")
        if not name:
            continue

        if i % 50 == 0:
            print(
                f"  [{i}/{total}] Fetching release dates ...",
                file=sys.stderr,
                flush=True,
            )

        versions = fetch_pypi_versions(name)
        version_rows.extend(
            {"name": name, "version": v, "upload_time": t} for v, t in versions
        )
        first = versions[0][1] if versions else None
        latest = versions[-1][1] if versions else None
        n_vers = len(versions)

        rows.append({
            "name": name,
            "normalized_name": plugin.get("normalized_name", ""),
            "first_release": first,
            "latest_release": latest,
            "n_versions": n_vers,
            "pypi_versions": len(plugin.get("pypi_versions", [])),
            "conda_versions": len(plugin.get("conda_versions", [])),
            "github_url": github_map.get(name.lower()),
            "summary": plugin.get("summary", ""),
            "author": plugin.get("author", ""),
            "license": plugin.get("license", ""),
        })

        # Be kind to PyPI
        time.sleep(0.1)

    # 4. Save
    df = pd.DataFrame(rows)
    # Convert date strings to datetime
    df["first_release"] = pd.to_datetime(df["first_release"], utc=True)
    df["latest_release"] = pd.to_datetime(df["latest_release"], utc=True)

    output_path = DATA_DIR / "plugin_releases.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} plugins to {output_path}", file=sys.stderr)

    versions_df = pd.DataFrame(version_rows, columns=["name", "version", "upload_time"])
    versions_df["upload_time"] = pd.to_datetime(versions_df["upload_time"], utc=True)
    versions_path = DATA_DIR / "plugin_versions.csv"
    versions_df.sort_values(["name", "upload_time"]).to_csv(versions_path, index=False)
    print(f"Saved {len(versions_df)} releases to {versions_path}", file=sys.stderr)

    # Summary stats
    with_dates = df["first_release"].notna().sum()
    print(f"  {with_dates} plugins with known first-release date", file=sys.stderr)
    if with_dates > 0:
        print(
            f"  Date range: {df['first_release'].min().date()} to {df['first_release'].max().date()}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
