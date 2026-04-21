"""Plot contributor metrics using seaborn with colorblind-friendly palettes.

Reads data/metrics/*.csv and produces SVG plots in plots/ directory.

Plots:
1. new_contributors_over_time.svg — org-wide new contributors/month (30-day rolling)
2. new_contributors_per_repo.svg — per-repo breakdown
3. retention_heatmap.svg — cohort retention heatmap
4. cumulative_contributors.svg — cumulative growth
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

# Colorblind-friendly palette (Paul Tol "bright" + seaborn "colorblind")
CB_PALETTE = sns.color_palette("colorblind", 10)
SHADE_START = pd.Timestamp("2025-09-01")
TODAY = pd.Timestamp.now(tz="UTC")

TARGET_REPOS = [
    "new_contributors_napari_napari",
    "new_contributors_napari_npe2",
    "new_contributors_napari_docs",
    "new_contributors_napari_napari-plugin-template",
]
REPO_LABELS = {
    "new_contributors_napari_napari": "napari",
    "new_contributors_napari_npe2": "npe2",
    "new_contributors_napari_docs": "docs",
    "new_contributors_napari_napari-plugin-template": "plugin-template",
}

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


# Consistent color indices across all plots
CB_MAIN = 0       # blue — primary metric (new contributors, total plugins)
CB_ROLLING = 2    # orange — rolling averages, ratios
CB_ACCENT = 3     # green — plugin-specific metrics
CB_FILL = 4       # red — filled areas


def _add_2026_shading(ax: plt.Axes, xmax=None) -> None:
    """Add a light shaded region from Sep 2025 to the right edge."""
    if xmax is None:
        xmax = TODAY
    ylims = ax.get_ylim()
    ax.axvspan(SHADE_START, xmax, alpha=0.08, color="black", zorder=0)
    ax.axvline(SHADE_START, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_ylim(ylims)


# ── Plot 1: New contributors over time (org-wide) ──────────────────────────

def plot_new_contributors_over_time() -> None:
    """Line plot of new contributors per month with 30-day rolling window."""
    path = METRICS_DIR / "new_contributors_monthly.csv"
    if not path.exists():
        print("  Skipping: new_contributors_monthly.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["month"])
    df = df.sort_values("month").set_index("month")

    # 2-month rolling — reduces jitter while keeping more resolution
    window = 2
    df["rolling"] = df["new_contributors"].rolling(window=window, center=True, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(6, 5))

    # Raw bars (very transparent so the line is clearly visible)
    ax.bar(
        df.index, df["new_contributors"],
        color=CB_PALETTE[CB_MAIN], alpha=0.25, width=25, label="Monthly", zorder=1,
    )

    # Rolling line
    ax.plot(
        df.index, df["rolling"],
        color=CB_PALETTE[CB_ROLLING], linewidth=2.5, label=f"{window}-month rolling avg", zorder=2,
    )

    _add_2026_shading(ax, TODAY)
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    ax.set_title("New Contributors to the napari Organization", weight="bold")
    ax.set_ylabel("New Contributors")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "new_contributors_over_time.svg")


# ── Plot 2: New contributors per repo ──────────────────────────────────────

def plot_new_contributors_per_repo() -> None:
    """Two-line plot: org-wide total + napari/napari only."""
    org_path = METRICS_DIR / "new_contributors_monthly.csv"
    repo_path = METRICS_DIR / "new_contributors_per_repo.csv"
    if not org_path.exists() or not repo_path.exists():
        print("  Skipping: metrics not found", file=sys.stderr)
        return

    org = pd.read_csv(org_path, parse_dates=["month"]).set_index("month")
    repo = pd.read_csv(repo_path, parse_dates=["month"]).set_index("month")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    # Org-wide total (all repos)
    total_series = org["new_contributors"].rolling(3, center=True, min_periods=1).mean()
    ax.plot(
        org.index, total_series,
        color=CB_PALETTE[CB_MAIN], linewidth=2.5, label="All napari org repos",
    )

    # napari/napari only
    napari_series = repo["new_contributors_napari_napari"].rolling(3, center=True, min_periods=1).mean()
    ax.plot(
        repo.index, napari_series,
        color=CB_PALETTE[CB_ROLLING], linewidth=2.5, label="napari/napari only",
    )

    _add_2026_shading(ax, TODAY)
    ax.set_title("New Contributors: Org-wide vs napari Main Repo", weight="bold")
    ax.set_ylabel("New Contributors (3-month rolling)")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "new_contributors_per_repo.svg")


# ── Plot 3: Retention by year ──────────────────────────────────────────────

def plot_retention_heatmap() -> None:
    """Grouped bar chart: yearly retention rates for 1mo, 3mo, 6mo windows.

    Monthly cohorts are too sparse (often 1–5 people) to show meaningful
    patterns, so we aggregate by year.
    """
    path = METRICS_DIR / "retention.csv"
    if not path.exists():
        print("  Skipping: retention.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["cohort_month"])
    if df.empty:
        return

    retention_cols = [c for c in df.columns if c.startswith("retention_")]
    if not retention_cols:
        return

    # Aggregate by year: weighted average of retention rates
    df["year"] = df["cohort_month"].dt.year
    yearly = df.groupby("year").apply(
        lambda g: pd.Series({
            "n_new": g["n_new"].sum(),
            **{
                col: (g[col] * g["n_new"]).sum() / g["n_new"].sum()
                for col in retention_cols
            },
        }),
        include_groups=False,
    ).reset_index()

    # Melt for grouped bars
    melted = yearly.melt(
        id_vars=["year", "n_new"],
        value_vars=retention_cols,
        var_name="window",
        value_name="retention",
    )
    window_labels = {
        "retention_1mo": "1 month",
        "retention_3mo": "3 months",
        "retention_6mo": "6 months",
    }
    melted["window"] = melted["window"].map(window_labels)

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(
        data=melted,
        x="year", y="retention", hue="window",
        palette=[CB_PALETTE[CB_MAIN], CB_PALETTE[CB_ROLLING], CB_PALETTE[CB_ACCENT]],
        ax=ax,
    )
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.set_ylim(0, 1)
    ax.set_title("New Contributor Retention by Year", weight="bold")
    ax.set_ylabel("Retention Rate")
    ax.set_xlabel("")
    ax.legend(frameon=True, title="Return within")

    # Annotate bar groups with cohort size
    for _, row in yearly.iterrows():
        ax.text(
            row["year"], 0.05,
            f"n={row['n_new']}",
            ha="center", fontsize=8, color="gray",
        )

    _save(fig, "retention_heatmap.svg")


# ── Plot 4: Cumulative contributors + annual growth ────────────────────────

def plot_cumulative_contributors() -> None:
    """Dual-panel: cumulative total (top) + annual new contributors (bottom).

    The bottom panel uses color to highlight three phases:
    initial growth, slowdown, and re-acceleration.
    """
    cum_path = METRICS_DIR / "cumulative_contributors.csv"
    month_path = METRICS_DIR / "new_contributors_monthly.csv"
    if not cum_path.exists():
        print("  Skipping: cumulative_contributors.csv not found", file=sys.stderr)
        return

    cum = pd.read_csv(cum_path, parse_dates=["first_commit"]).sort_values("first_commit")

    # Aggregate new contributors by year for the bottom panel
    monthly = pd.read_csv(month_path, parse_dates=["month"])
    monthly["year"] = monthly["month"].dt.year
    annual = monthly.groupby("year")["new_contributors"].sum().reset_index()

    # Color-code years by phase
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), sharex=True)

    # ── Top panel: cumulative ──
    ax1.set_xlim(pd.Timestamp("2019-01-01"), TODAY)
    ax1.fill_between(
        cum["first_commit"], cum["total_contributors"],
        color=CB_PALETTE[CB_FILL], alpha=0.3,
    )
    ax1.plot(
        cum["first_commit"], cum["total_contributors"],
        color=CB_PALETTE[CB_MAIN], linewidth=2.5,
    )
    _add_2026_shading(ax1, TODAY)
    ax1.set_title("Cumulative + Annual New Contributors", weight="bold")
    ax1.set_ylabel("Total Contributors")
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # ── Bottom panel: annual new contributors ──
    ax2.set_xlim(pd.Timestamp("2019-01-01"), TODAY)
    ax2.bar(
        pd.to_datetime(annual["year"], format="%Y"),
        annual["new_contributors"],
        color=CB_PALETTE[CB_MAIN], alpha=0.7, width=250,
    )
    ax2.set_ylabel("New Contributors per Year")
    ax2.set_xlabel("")

    # Annotate the 2023 dip
    min_row = annual.loc[annual["new_contributors"].idxmin()]
    ax2.annotate(
        f"Low: {int(min_row['new_contributors'])} new",
        xy=(pd.Timestamp(f"{int(min_row['year'])}-07-01"), min_row["new_contributors"]),
        xytext=(0, -20), textcoords="offset points",
        fontsize=9, color=CB_PALETTE[CB_FILL],
        ha="center", va="top",
        arrowprops=dict(arrowstyle="->", color=CB_PALETTE[CB_FILL], lw=1),
    )

    _save(fig, "cumulative_contributors.svg")


# ── Plot 5: Active contributors ────────────────────────────────────────────

def plot_active_contributors() -> None:
    """Line plot: active contributors with 6-month trailing window.

    Also overlays active plugin developers from the same metric."""
    path = METRICS_DIR / "active_contributors.csv"
    plugin_path = METRICS_DIR / "active_plugin_devs.csv"
    if not path.exists():
        print("  Skipping: active_contributors.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["month"])

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    ax.fill_between(
        df["month"], 0, df["active_contributors"],
        color=CB_PALETTE[CB_MAIN], alpha=0.15,
    )
    ax.plot(
        df["month"], df["active_contributors"],
        color=CB_PALETTE[CB_MAIN], linewidth=2.5, label="All active contributors",
    )

    # Overlay active plugin devs
    if plugin_path.exists():
        plugin_df = pd.read_csv(plugin_path, parse_dates=["month"])
        ax.plot(
            plugin_df["month"], plugin_df["active_plugin_devs"],
            color=CB_PALETTE[CB_ACCENT], linewidth=2.5, label="Active plugin developers",
        )

    _add_2026_shading(ax, TODAY)
    ax.set_title("Active napari Contributors (6-month trailing)", weight="bold")
    ax.set_ylabel("Active Contributors")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="lower right")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "active_contributors.svg")


# ── Plot 5b: Active napari contributors (no plugin overlay) ────────────────

def plot_active_napari_only() -> None:
    """Line plot: active napari org contributors (fill + line style)."""
    path = METRICS_DIR / "active_contributors.csv"
    if not path.exists():
        print("  Skipping: active_contributors.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path, parse_dates=["month"])

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(pd.Timestamp("2019-01-01"), TODAY)

    ax.fill_between(
        df["month"], 0, df["active_contributors"],
        color=CB_PALETTE[CB_MAIN], alpha=0.15,
    )
    ax.plot(
        df["month"], df["active_contributors"],
        color=CB_PALETTE[CB_MAIN], linewidth=2.5,
    )

    _add_2026_shading(ax, TODAY)
    ax.set_title("Active napari Contributors (6-month trailing)", weight="bold")
    ax.set_ylabel("Active Contributors")
    ax.set_xlabel("")

    _save(fig, "active_napari_only.svg")


# ── Plot 6: Annual active contributors ─────────────────────────────────────

def plot_annual_contributors() -> None:
    """Bar chart: unique contributors active per calendar year."""
    path = METRICS_DIR / "annual_contributors.csv"
    if not path.exists():
        print("  Skipping: annual_contributors.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path).sort_values("year")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(
        df["year"], df["active_contributors"],
        color=CB_PALETTE[CB_MAIN], alpha=0.7, width=0.6,
    )
    ax.set_title("Active Contributors per Year", weight="bold")
    ax.set_ylabel("Contributors with ≥1 commit")
    ax.set_xlabel("")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "annual_contributors.svg")


# ── Plot 7: New vs returning contributors ──────────────────────────────────

def plot_new_vs_returning() -> None:
    """Stacked bar: each year split into new vs returning contributors."""
    path = METRICS_DIR / "new_vs_returning.csv"
    if not path.exists():
        print("  Skipping: new_vs_returning.csv not found", file=sys.stderr)
        return

    df = pd.read_csv(path).sort_values("year")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(
        df["year"], df["returning"],
        color=CB_PALETTE[CB_MAIN], alpha=0.7, width=0.6, label="Returning",
    )
    ax.bar(
        df["year"], df["new"],
        bottom=df["returning"],
        color=CB_PALETTE[CB_ACCENT], alpha=0.8, width=0.6, label="New",
    )
    ax.set_title("Contributors per Year: New vs Returning", weight="bold")
    ax.set_ylabel("Active Contributors")
    ax.set_xlabel("")
    ax.legend(frameon=True, loc="upper left")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, "new_vs_returning.svg")


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    print(
        "=== Phase 3.1: Plotting contributor metrics ===",
        file=sys.stderr,
        flush=True,
    )

    plot_new_contributors_over_time()
    plot_new_contributors_per_repo()
    plot_retention_heatmap()
    plot_cumulative_contributors()
    plot_active_contributors()
    plot_active_napari_only()
    plot_annual_contributors()
    plot_new_vs_returning()

    print("\nDone!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
