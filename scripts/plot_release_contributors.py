"""Plot the napari per-release new-contributor data (area view).

Reads ``new-contributors-by-release.csv`` (produced by
``build_release_contributors.py``) and draws the *area* timeline bar chart:

- **X axis** — timeline; each bar spans its development window (first -> last
  commit)
- **Y axis** — new contributors per month
- **Bar area = width × height = dev window × (contributors/month) ∝ total new
  contributors** — the physical box size is proportional to how many new
  contributors the release brought in.

Every bar is labelled ``release::count`` (vertical, centred over the bar).
Zero-count releases still get a label, but dimmed, so the ``::0`` bars stay
legible without competing with the real numbers. Releases with **>= 10** new
contributors are highlighted green. ``--interactive`` also writes a zoomable /
hoverable Plotly HTML version of the same chart, which by default omits the
original 0.1.0 release (12 contributors — the initial open-sourcing, not a
release cycle).

Usage::

    python scripts/plot_release_contributors.py                       # area PNG+SVG
    python scripts/plot_release_contributors.py --interactive         # + zoomable HTML
    python scripts/plot_release_contributors.py --min-release 0.2.5   # v0.2.5 -> present
    python scripts/plot_release_contributors.py --min-dev-days 0      # include short windows

``--interactive`` requires Plotly (declared as the optional ``plot`` extra in
``pyproject.toml``: ``uv add --optional plot plotly``).

Outputs (into ``--out-dir``, default ``plots/``)::

    release_new_contributors.png/.svg
    release_new_contributors_from025.png/.svg      (when --min-release is set)
    release_new_contributors_interactive.html       (with --interactive)
"""

from __future__ import annotations

import argparse
from datetime import timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_DEFAULT = REPO_ROOT / "2026-urssi-final-report" / "new-contributors-by-release.csv"
OUT_DIR_DEFAULT = REPO_ROOT / "plots"

CB_PALETTE = sns.color_palette("colorblind", 10)
SHADE_START = pd.Timestamp("2025-09-01")            # fellowship / initiative start
TODAY = pd.Timestamp.now().tz_localize(None)
HIGHLIGHT = 10                                       # colour bars >= this many new contributors

CB_MAIN = 0     # blue
CB_ACCENT = 3   # green

LABEL_SEP = "::"                                     # bar labels read release::count

LABEL_ROTATION = -90   # default: vertical, reads downward, centered over each bar

sns.set_theme(style="whitegrid", palette=CB_PALETTE)
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})


def _ver_key(v: str) -> tuple:
    return tuple(int(x) for x in str(v).split("."))


def load(csv: Path, min_dev_days: int, min_release: str | None) -> pd.DataFrame:
    df = pd.read_csv(csv, dtype=str)
    for col in ("release_date", "dev_window_first", "dev_window_last"):
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in ("new_contributors", "new_per_month", "dev_months", "months_between_releases"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["new_contributors", "dev_window_first", "dev_window_last"])
    df["dev_days"] = (df["dev_window_last"] - df["dev_window_first"]).dt.days
    if min_dev_days > 0:
        df = df[df["dev_days"] >= min_dev_days]
    if min_release:
        key = _ver_key(min_release)
        df = df[df["release"].map(lambda v: _ver_key(v) >= key)]
    return df.sort_values("dev_window_first").reset_index(drop=True)


def _bar_color(count: float):
    return CB_PALETTE[CB_ACCENT] if count >= HIGHLIGHT else CB_PALETTE[CB_MAIN]


def _shade(ax, xmax=None):
    ylim = ax.get_ylim()
    ax.axvspan(SHADE_START, xmax or TODAY, alpha=0.08, color="black", zorder=0)
    ax.axvline(SHADE_START, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_ylim(ylim)


def view_area(df: pd.DataFrame, label_rotation: int = LABEL_ROTATION, label_min: int = 1):
    fig, ax = plt.subplots(figsize=(16, 6.5))
    for _, r in df.iterrows():
        left = r["dev_window_first"].to_pydatetime()
        width = r["dev_window_last"] - r["dev_window_first"]
        ax.bar(left, r["new_per_month"], width=width, align="edge",
               color=_bar_color(r["new_contributors"]),
               alpha=0.85, edgecolor="white", linewidth=0.4)
    _shade(ax)
    # centred labels above each bar; zero-count releases get a small dim label
    for _, r in df.iterrows():
        c = int(r["new_contributors"])
        if c != 0 and c < label_min:
            continue
        x = r["dev_window_first"] + (r["dev_window_last"] - r["dev_window_first"]) / 2
        ax.annotate(f"{r['release']}{LABEL_SEP}{c}",
                    (x, r["new_per_month"]),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", rotation=label_rotation,
                    fontsize=6 if c == 0 else 7,
                    color="#b8b8b8" if c == 0 else "#262626")
    ax.set_xlim(df["dev_window_first"].min() - timedelta(days=30), TODAY)
    ax.grid(axis="y", alpha=0.4)
    ax.set_ylabel("New contributors / month")
    ax.set_xlabel("Timeline (release dates)")
    ax.set_title(
        "napari new contributors per release — bar area = new contributors\n"
        "(green: ≥ 10 new contributors; labels: release::count)",
        weight="bold",
    )
    return fig


def view_interactive(df: pd.DataFrame, out_dir: Path, label_min: int = 1,
                     include_0_1_0: bool = False) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError as e:
        raise SystemExit(
            "--interactive requires plotly: `uv add --optional plot plotly`"
        ) from e

    d = df.copy()
    skipped_010 = False
    if not include_0_1_0 and (d["release"] == "0.1.0").any():
        d = d[d["release"] != "0.1.0"].reset_index(drop=True)
        skipped_010 = True
    d["x_mid"] = d["dev_window_first"] + (d["dev_window_last"] - d["dev_window_first"]) / 2
    d["dev_ms"] = (d["dev_window_last"] - d["dev_window_first"]).dt.total_seconds() * 1000
    label_meta = []
    for _, r in d.iterrows():
        c = int(r["new_contributors"])
        if c == 0:
            label_meta.append((f"{r['release']}{LABEL_SEP}{c}", True))      # dim
        elif c >= label_min:
            label_meta.append((f"{r['release']}{LABEL_SEP}{c}", False))     # normal
        else:
            label_meta.append(("", False))
    d["label"] = [t for t, _ in label_meta]
    d["dim"] = [is_dim for _, is_dim in label_meta]
    colors = ["#2e8b57" if c >= HIGHLIGHT else "#4477aa" for c in d["new_contributors"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=d["x_mid"], y=d["new_per_month"], width=d["dev_ms"],
        marker_color=colors,
        customdata=d[["release", "new_contributors",
                      "dev_window_first", "dev_window_last"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "new contributors: %{customdata[1]}<br>"
            "rate: %{y:.1f} / month<br>"
            "dev window: %{customdata[2]} -> %{customdata[3]}<extra></extra>"
        ),
    ))
    # labels as annotations so they render at a uniform size:
    # Plotly auto-scales Bar text to fit each bar's width
    for xi, yi, lab, is_dim in zip(d["x_mid"], d["new_per_month"], d["label"], d["dim"]):
        if lab:
            fig.add_annotation(
                x=xi, y=yi, text=lab,
                textangle=-90, showarrow=False,
                font=dict(size=8, color="#b8b8b8" if is_dim else "#262626"),
                xanchor="center", yanchor="bottom", yshift=2,
            )
    sub = "bar area = new contributors · green = ≥ 10 · labels: release::count"
    if skipped_010:
        sub += " · 0.1.0 omitted (original release: 12 contributors)"
    sub += " · zoom to explore"
    fig.update_layout(
        title="napari new contributors per release<br>" f"<sub>{sub}</sub>",
        xaxis_title="Timeline (release dates)",
        yaxis_title="New contributors / month",
        hovermode="closest",
        height=560,
        margin=dict(t=90, b=40),
    )
    out = out_dir / "release_new_contributors_interactive.html"
    fig.write_html(out, include_plotlyjs="cdn")
    print(f"  Saved {out}")


def _save(fig, out_dir: Path, stem: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for fmt in ("svg", "png"):
        fig.savefig(out_dir / f"{stem}.{fmt}", format=fmt)
        print(f"  Saved {out_dir / f'{stem}.{fmt}'}")
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, default=CSV_DEFAULT)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR_DEFAULT)
    ap.add_argument("--min-dev-days", type=int, default=14,
                    help="Drop releases whose dev window is shorter than this "
                         "many days (short patch windows inflate per-month rates). "
                         "Set 0 to show everything.")
    ap.add_argument("--min-release", type=str, default=None,
                    help="Only show releases at or after this version, e.g. 0.2.5.")
    ap.add_argument("--interactive", action="store_true",
                    help="Also write the zoomable Plotly HTML file.")
    ap.add_argument("--label-rotation", type=int, default=LABEL_ROTATION,
                    help="Rotation (degrees) of the static bar labels (default 90).")
    ap.add_argument("--label-min", type=int, default=1,
                    help="Full-size labels for releases with at least this many "
                         "new contributors (default 1); zero-count releases "
                         "always get a dimmed label.")
    ap.add_argument("--include-0-1-0", action="store_true",
                    help="Keep the original 0.1.0 release (12 contributors) in "
                         "the interactive view (omitted by default).")
    args = ap.parse_args()

    df = load(args.csv, args.min_dev_days, args.min_release)
    n0 = len(pd.read_csv(args.csv, dtype=str))
    print(f"  plotting {len(df)} of {n0} releases"
          + (f"  [min-dev-days={args.min_dev_days}]" if args.min_dev_days else "")
          + (f"  [from v{args.min_release}]" if args.min_release else ""))

    stem = "release_new_contributors"
    if args.min_release:
        stem += f"_from{''.join(args.min_release.split('.'))}"
    _save(view_area(df, label_rotation=args.label_rotation, label_min=args.label_min),
          args.out_dir, stem)

    if args.interactive:
        view_interactive(df, args.out_dir, label_min=args.label_min,
                         include_0_1_0=args.include_0_1_0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
