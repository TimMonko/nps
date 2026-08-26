"""Fetch Python version support data for each plugin from PyPI.

Reads plugin names from plugin_releases.csv, fetches PyPI JSON for
the latest version of each, and extracts requires_python + classifiers.

Output: data/python_versions.csv
Columns: name, requires_python, min_python, max_python, supported_versions
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PYTHON_CLASSIFIER_RE = re.compile(r"Programming Language :: Python :: (3\.\d+)")


def _normalize_ver(v: str) -> str:
    """Strip to major.minor: '3.11.0' -> '3.11', '3.10.*' -> '3.10'."""
    parts = v.split(".")
    return f"{parts[0]}.{parts[1]}"


def _ver_as_tuple(v: str) -> tuple[int, ...]:
    """Convert '3.10' -> (3, 10) for proper comparison. Handles patch versions too."""
    parts = v.split(".")
    return (int(parts[0]), int(parts[1]))


def parse_requires_python(req: str | None) -> tuple[str | None, str | None]:
    """Parse a requires_python string like '>=3.8' or '>=3.9,<3.13'.

    Returns (min_version, max_version) as strings like ('3.8', None) or ('3.9', '3.12').
    Both inclusive and normalized to major.minor.
    """
    if not req:
        return None, None
    min_ver: str | None = None
    max_ver: str | None = None
    for part in req.split(","):
        part = part.strip()
        try:
            if part.startswith(">="):
                ver = _normalize_ver(part[2:].strip())
                if min_ver is None or _ver_as_tuple(ver) > _ver_as_tuple(min_ver):
                    min_ver = ver
            elif part.startswith(">"):
                # >3.9 means 3.10+, convert to >=
                ver = _normalize_ver(part[1:].strip())
                t = _ver_as_tuple(ver)
                bumped = f"{t[0]}.{t[1] + 1}"
                if min_ver is None or _ver_as_tuple(bumped) > _ver_as_tuple(min_ver):
                    min_ver = bumped
            elif part.startswith("<="):
                ver = _normalize_ver(part[2:].strip())
                if max_ver is None or _ver_as_tuple(ver) < _ver_as_tuple(max_ver):
                    max_ver = ver
            elif part.startswith("<"):
                # <3.13 means ≤3.12
                ver = _normalize_ver(part[1:].strip())
                t = _ver_as_tuple(ver)
                lowered = f"{t[0]}.{t[1] - 1}"
                if max_ver is None or _ver_as_tuple(lowered) < _ver_as_tuple(max_ver):
                    max_ver = lowered
            elif part.startswith("=="):
                ver = _normalize_ver(part[2:].strip())
                min_ver = ver
                max_ver = ver
                # <3.13 means ≤3.12
                ver = part[1:].strip()
                parts = ver.split(".")
                lowered = f"{parts[0]}.{int(parts[1]) - 1}" if len(parts) >= 2 else f"{int(parts[0]) - 1}"
                if max_ver is None or _ver_as_tuple(lowered) < _ver_as_tuple(max_ver):
                    max_ver = lowered
            elif part.startswith("=="):
                ver = part[2:].strip()
                min_ver = ver
                max_ver = ver
        except (ValueError, IndexError):
            pass
    return min_ver, max_ver


def fetch_plugin_python_info(pypi_name: str) -> dict:
    """Fetch requires_python and Python classifiers for a plugin."""
    url = f"https://pypi.org/pypi/{pypi_name}/json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {"requires_python": None, "supported_versions": "", "min_python": None, "max_python": None}
        data = resp.json()
        info = data.get("info", {})
    except Exception:
        return {"requires_python": None, "supported_versions": "", "min_python": None, "max_python": None}

    req_py = info.get("requires_python")
    classifiers = info.get("classifiers", []) or []

    # Extract Python version classifiers
    py_versions = sorted(
        {m.group(1) for m in (PYTHON_CLASSIFIER_RE.match(c) for c in classifiers) if m}
    )

    min_py, max_py = parse_requires_python(req_py)

    # Format with "v" prefix so pandas doesn't interpret as float (3.10 -> 3.1)
    min_py = f"v{min_py}" if min_py else None
    max_py = f"v{max_py}" if max_py else None

    return {
        "requires_python": req_py,
        "supported_versions": ",".join(py_versions),
        "min_python": min_py,
        "max_python": max_py,
    }


def main() -> int:
    print(
        "=== Fetching Python version data ===\n",
        file=sys.stderr,
        flush=True,
    )

    # Read plugin list
    releases_path = DATA_DIR / "plugin_releases.csv"
    if not releases_path.exists():
        print("  ERROR: plugin_releases.csv not found. Run fetch_plugin_data.py first.", file=sys.stderr)
        return 1

    plugins = pd.read_csv(releases_path)
    print(f"  {len(plugins)} plugins to check", file=sys.stderr, flush=True)

    rows: list[dict] = []
    for i, row in plugins.iterrows():
        name = row.get("name", "") or row.get("normalized_name", "")
        if not name:
            continue

        if i % 50 == 0:
            print(f"  [{i}/{len(plugins)}] ...", file=sys.stderr, flush=True)

        py_info = fetch_plugin_python_info(name)
        rows.append({
            "name": name,
            "first_release": row.get("first_release"),
            "requires_python": py_info["requires_python"],
            "supported_versions": py_info["supported_versions"],
            "min_python": py_info["min_python"],
            "max_python": py_info["max_python"],
        })
        time.sleep(0.08)

    df = pd.DataFrame(rows)
    output_path = DATA_DIR / "python_versions.csv"
    df.to_csv(output_path, index=False)
    print(f"\n  Saved {len(df)} plugins to {output_path}", file=sys.stderr)

    # Summary
    with_data = df["requires_python"].notna().sum()
    print(f"  {with_data} plugins with requires_python data", file=sys.stderr)

    if with_data > 0:
        min_counts = df["min_python"].value_counts().sort_index()
        print("\n  Minimum Python version requirements:", file=sys.stderr)
        for ver, count in min_counts.items():
            print(f"    Python >= {ver}: {count} plugins", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
