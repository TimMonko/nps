"""Plot plugin ecosystem metrics using seaborn with colorblind-friendly palettes.

Reads data/metrics/*.csv and produces SVG plots in plots/ directory.

Plots:
1. new_plugins_over_time.svg — new plugins released per month
2. plugin_maintenance.svg — active / total / maintenance ratio
3. plugin_dev_overlap.svg — new org contributors who are also plugin devs
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

# ── Configuration ──────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
METRICS_DIR = REPO_ROOT / "data" / "metrics"
PLOTS_DIR = REPO_ROOT / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

CB_PALETTE = sns.color_palette("colorblind", 10)
SHADE_START = pd.Timestamp("2025-09-01")
TODAY = pd.Timestamp.now(tz="UTC")

sns.set_theme(style="whitegrid", palette=CB_PALETTE)
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 15,
    "legend.fontsize": 12,
})


def _save(fig: plt.Figure, name: str) -> None:
    path = PLOTS_DIR / name
    fig.savefig(path, format="svg")
    fig.savefig(path.with_suffix(".png"), format="png")
    print(f"  Saved {path}", file=sys.stderr)
    plt.close(fig)


# Consistent color indices matching plot_contributors.py
CB_MAIN = 0       # blue — primary metric
CB_ROLLING = 2    # orange — rolling averages, ratios
CB_ACCENT = 3     # green — plugin-specific metrics
CB_FILL = 4       # red — filled areas


def _add_2026_shading(ax: plt.Axes, xmax=None) -> None:
    if xmax is None:
        xmax = TODAY
    ylims = ax.get_ylim()
    ax.axvspan(SHADE_START, xmax, alpha=0.08, color="black", zorder=0)
    ax.axvline(SHADE_START, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_ylim(ylims)


# ── Plot 1: New plugins over time ──────────────────────────────────────────

def plot_new_plugins_over_time() -> None:
    """Bar chart: new plugins released per month."""
    path = METRICS_DIR / "new_plugins_monthly.csv"
    if not path.exists():
        print("  Skipping: new_plugins_monthly.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["month"])
    df = df.sort_values("month")

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    ax.bar(
        df["month"], df["new_plugins"],
        color=CB_PALETTE[CB_MAIN], alpha=0.2, width=25,
    )

    # Rolling average overlay
    window = 3
    rolling = df.set_index("month")["new_plugins"].rolling(window=window, center=True).mean()
    ax.plot(
        rolling.index, rolling.values,
        color=CB_PALETTE[CB_ROLLING], linewidth=2.5, label=f"{window}-month rolling avg",
    )

    _add_2026_shading(ax, TODAY)

    ax.set_title("New napari Plugins Released per Month", weight="bold")
    ax.set_ylabel("New Plugins")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "new_plugins_over_time.svg")


# ── Plot 2: Plugin maintenance ─────────────────────────────────────────────

def plot_plugin_maintenance() -> None:
    """Stacked area: total plugins, actively maintained, new per month."""
    maint_path = METRICS_DIR / "plugin_maintenance.csv"
    new_path = METRICS_DIR / "new_plugins_monthly.csv"

    if not maint_path.exists():
        print("  Skipping: plugin_maintenance.csv not found", file=sys.stderr)
        return

    maint = pd.read_csv(maint_path, parse_dates=["month"]).sort_values("month")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10), sharex=True)

    for ax in (ax1, ax2):
        ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    # Top: stacked area — total (background), active (foreground)
    ax1.fill_between(
        maint["month"], 0, maint["total_plugins"],
        color=CB_PALETTE[CB_FILL], alpha=0.15, label="Total plugins",
    )
    ax1.fill_between(
        maint["month"], 0, maint["active_plugins"],
        color=CB_PALETTE[CB_MAIN], alpha=0.5, label="Actively maintained (6-month window)",
    )
    ax1.set_ylabel("Plugin Count")
    ax1.legend(frameon=True, loc="upper left")
    ax1.set_title("Plugin Ecosystem: Total vs Actively Maintained", weight="bold")

    # Bottom: maintenance ratio
    ax2.plot(
        maint["month"], maint["maintenance_ratio"],
        color=CB_PALETTE[CB_ROLLING], linewidth=2.5,
    )
    ax2.axhline(
        0.5, color="gray", linestyle=":", linewidth=0.8, alpha=0.5
    )
    ax2.set_ylabel("Maintenance Ratio")
    ax2.set_xlabel("")
    ax2.set_title("Proportion of Plugins Actively Maintained", weight="bold")
    ax2.legend(frameon=True, loc="upper left")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

    for ax in (ax1, ax2):
        _add_2026_shading(ax, TODAY)

    _save(fig, "plugin_maintenance.svg")


# ── Plot 3: Plugin-developer overlap ───────────────────────────────────────

def plot_plugin_dev_overlap() -> None:
    """Cumulative proportion: of ALL contributors, fraction also plugin devs."""
    path = METRICS_DIR / "cumulative_plugin_dev_ratio.csv"
    if not path.exists():
        print("  Skipping: cumulative_plugin_dev_ratio.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["first_commit"])

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    ax.fill_between(
        df["first_commit"], 0, df["cumulative_plugin_dev_ratio"],
        color=CB_PALETTE[CB_ACCENT], alpha=0.2,
    )
    ax.plot(
        df["first_commit"], df["cumulative_plugin_dev_ratio"],
        color=CB_PALETTE[CB_ACCENT], linewidth=2.5,
    )
    ax.set_ylabel("Cumulative proportion of all contributors\nalso in plugin repos")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.set_ylim(0, 1)

    _add_2026_shading(ax, TODAY)
    ax.set_title("Plugin Developers Among All Contributors", weight="bold")
    ax.set_xlabel("")

    # Annotate the final value
    final = df["cumulative_plugin_dev_ratio"].iloc[-1]
    ax.annotate(
        f"{final:.0%}",
        xy=(df["first_commit"].iloc[-1], final),
        xytext=(10, -10), textcoords="offset points",
        fontsize=12, weight="bold", color=CB_PALETTE[CB_ACCENT],
    )

    _save(fig, "plugin_dev_overlap.svg")


def plot_new_plugin_devs() -> None:
    """Bar + line: new plugin developers per month (first-time org contributors who are also plugin devs)."""
    path = METRICS_DIR / "overlap.csv"
    if not path.exists():
        print("  Skipping: overlap.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["month"])
    df = df.sort_values("month")
    df["rolling"] = df["n_plugin_devs"].rolling(3, center=True, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    ax.bar(
        df["month"], df["n_plugin_devs"],
        color=CB_PALETTE[CB_MAIN], alpha=0.2, width=25,
    )
    ax.plot(
        df["month"], df["rolling"],
        color=CB_PALETTE[CB_ROLLING], linewidth=2.5, label="3-month rolling avg",
    )

    _add_2026_shading(ax, TODAY)
    ax.set_title("New Plugin Developers per Month", weight="bold")
    ax.set_ylabel("New plugin developers\n(first-time org contributors also in plugin repos)")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "new_plugin_devs_over_time.svg")


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    print(
        "=== Phase 3.2: Plotting plugin metrics ===",
        file=sys.stderr,
        flush=True,
    )

    plot_new_plugins_over_time()
    plot_plugin_maintenance()
    plot_plugin_dev_overlap()
    plot_new_plugin_devs()

    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
