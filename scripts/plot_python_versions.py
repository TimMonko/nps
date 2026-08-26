"""Plot Python version support across napari plugins over time."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
PLOTS_DIR = REPO_ROOT / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

CB_PALETTE = sns.color_palette("colorblind", 10)
SHADE_START = pd.Timestamp("2025-09-01")
TODAY = pd.Timestamp.now(tz="UTC")

sns.set_theme(style="whitegrid", palette=CB_PALETTE)
plt.rcParams.update({
    "figure.dpi": 225,
    "savefig.dpi": 225,
    "savefig.bbox": "tight",
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 15,
    "legend.fontsize": 12,
})

CB_MAIN = 0
CB_ROLLING = 2
CB_ACCENT = 3
CB_FILL = 4


def _save(fig: plt.Figure, name: str) -> None:
    path = PLOTS_DIR / name
    fig.savefig(path, format="svg")
    fig.savefig(path.with_suffix(".png"), format="png")
    print(f"  Saved {path}", file=sys.stderr)
    plt.close(fig)


def _ver_tuple(v: str) -> tuple[int, ...]:
    """Convert '3.10' or '3.11.0' -> (3, 10) for proper sorting. Ignores patch."""
    parts = v.split(".")
    return (int(parts[0]), int(parts[1]))


def load_data() -> pd.DataFrame:
    """Load python version data, filter to >=3.7 and drop NaN."""
    path = DATA_DIR / "python_versions.csv"
    if not path.exists():
        print("  ERROR: python_versions.csv not found.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(path, parse_dates=["first_release"])
    df = df[df["min_python"].notna()].copy()
    df["first_release"] = pd.to_datetime(df["first_release"], utc=True)
    df = df[df["first_release"].notna()]
    # Strip "v" prefix used to avoid float serialization issues (v3.10 -> 3.10)
    df["min_python"] = df["min_python"].astype(str).str.replace("v", "", regex=False).str.strip()
    # Filter out Python 3.6 and earlier
    df = df[df["min_python"].apply(lambda v: _ver_tuple(v) >= (3, 7) if v and v != "nan" else False)]
    return df


def plot_version_support_over_time() -> None:
    """Stacked area: cumulative plugins by min Python version over time."""
    df = load_data()
    df = df.sort_values("first_release")

    def _bucket(v: str) -> str:
        t = _ver_tuple(v)
        return "3.13+" if t >= (3, 13) else v

    df["py_bucket"] = df["min_python"].apply(_bucket)
    buckets = sorted(df["py_bucket"].unique(), key=lambda x: _ver_tuple(x.split("+")[0]))

    months = pd.date_range(
        df["first_release"].min().replace(day=1),
        TODAY.replace(day=1),
        freq="MS",
    )

    counts = {b: [] for b in buckets}
    for m in months:
        before = df[df["first_release"] <= m]
        for b in buckets:
            counts[b].append((before["py_bucket"] == b).sum())

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    palette = {b: CB_PALETTE[i % len(CB_PALETTE)] for i, b in enumerate(buckets)}
    ax.stackplot(
        months,
        *[counts[b] for b in buckets],
        labels=[f"Python >= {b}" for b in buckets],
        colors=[palette[b] for b in buckets],
        alpha=0.8,
    )

    ax.set_title("Python Version Requirements of napari Plugins", weight="bold")
    ax.set_ylabel("Cumulative plugin count")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left", fontsize=9)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "python_version_support.svg")


def plot_version_support_log() -> None:
    """Stacked area with log y-scale to show high-version tail."""
    df = load_data()
    df = df.sort_values("first_release")

    def _bucket(v: str) -> str:
        t = _ver_tuple(v)
        return "3.13+" if t >= (3, 13) else v

    df["py_bucket"] = df["min_python"].apply(_bucket)
    buckets = sorted(df["py_bucket"].unique(), key=lambda x: _ver_tuple(x.split("+")[0]))

    months = pd.date_range(
        df["first_release"].min().replace(day=1),
        TODAY.replace(day=1),
        freq="MS",
    )

    counts = {b: [] for b in buckets}
    for m in months:
        before = df[df["first_release"] <= m]
        for b in buckets:
            counts[b].append((before["py_bucket"] == b).sum())

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    palette = {b: CB_PALETTE[i % len(CB_PALETTE)] for i, b in enumerate(buckets)}
    ax.stackplot(
        months,
        *[counts[b] for b in buckets],
        labels=[f"Python >= {b}" for b in buckets],
        colors=[palette[b] for b in buckets],
        alpha=0.8,
    )
    ax.set_yscale("log")
    ax.set_ylim(bottom=0.5)  # avoid log(0)

    ax.set_title("Python Version Requirements (log scale)", weight="bold")
    ax.set_ylabel("Cumulative plugin count (log)")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left", fontsize=8, ncols=2)
    ax.yaxis.set_major_locator(mticker.LogLocator(base=10, numticks=8))

    _save(fig, "python_version_support_log.svg")


def plot_version_support_classifiers() -> None:
    """Line plot: plugins supporting each Python version over time (from classifiers).

    Unlike the min_python plot, a plugin can count toward MULTIPLE versions.
    This is where 3.13 and 3.14 actually show up.
    """
    df = load_data()
    df = df.sort_values("first_release")

    months = pd.date_range(
        df["first_release"].min().replace(day=1),
        TODAY.replace(day=1),
        freq="MS",
    )

    # Collect all supported versions across all plugins
    all_versions: set[str] = set()
    ver_to_plugins: dict[str, list[pd.Timestamp]] = {}
    for _, row in df.iterrows():
        versions = str(row.get("supported_versions", ""))
        if not versions:
            continue
        for v in versions.split(","):
            v = v.strip()
            if not v or v == "nan" or _ver_tuple(v) < (3, 7):
                continue
            all_versions.add(v)
            if v not in ver_to_plugins:
                ver_to_plugins[v] = []
            ver_to_plugins[v].append(row["first_release"])

    versions = sorted(all_versions, key=_ver_tuple)
    if not versions:
        print("  No classifier data to plot", file=sys.stderr)
        return

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    for i, v in enumerate(versions):
        dates = sorted(ver_to_plugins.get(v, []))
        counts = [sum(1 for d in dates if d <= m) for m in months]
        ax.plot(
            months, counts,
            color=CB_PALETTE[i % len(CB_PALETTE)],
            linewidth=2.5, label=f"Python {v}",
        )

    ax.set_title("Plugins Supporting Each Python Version", weight="bold")
    ax.set_ylabel("Number of plugins")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left", fontsize=8, ncols=2)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "python_version_support_classifiers.svg")


def plot_version_snapshot() -> None:
    """Bar chart: current Python version support across all plugins."""
    df = load_data()

    version_counts: Counter[str] = Counter()
    for _, row in df.iterrows():
        versions = str(row.get("supported_versions", ""))
        if versions:
            for v in versions.split(","):
                v = v.strip()
                if v and v != "nan" and _ver_tuple(v) >= (3, 7):
                    version_counts[v] += 1

    if not version_counts:
        print("  No version data to plot", file=sys.stderr)
        return

    versions = sorted(version_counts.keys(), key=_ver_tuple)
    counts = [version_counts[v] for v in versions]

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(versions, counts, color=CB_PALETTE[CB_MAIN], alpha=0.7)

    ax.set_title("Current Python Version Support\nAmong napari Plugins", weight="bold")
    ax.set_ylabel("Number of plugins supporting")
    ax.set_xlabel("Python version")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(counts) * 0.02,
            str(count),
            ha="center", fontsize=10, weight="bold",
        )

    _save(fig, "python_version_snapshot.svg")


def main() -> int:
    print("=== Plotting Python version data ===", file=sys.stderr, flush=True)
    plot_version_support_over_time()
    plot_version_support_log()
    plot_version_support_classifiers()
    plot_version_snapshot()
    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
