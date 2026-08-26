"""Build reports/plugin-template-usage.md — napari-plugin-template usage.

Inputs:
  - data/plugin_template_usage.csv  (from detect_plugin_template_usage.py)
  - data/plugin_releases.csv        (from fetch_plugin_data.py)

Output:
  - reports/plugin-template-usage.md
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
REPORTS_DIR = REPO_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
OUT = REPORTS_DIR / "plugin-template-usage.md"

TPL_ERAS = ("copier", "cookiecutter", "template")
CUT = pd.Timestamp("2025-09-01", tz="UTC")
GENERATED = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d")


def load() -> pd.DataFrame:
    usage = pd.read_csv(DATA_DIR / "plugin_template_usage.csv")
    rel = pd.read_csv(DATA_DIR / "plugin_releases.csv")
    rel["first_release"] = pd.to_datetime(rel["first_release"], utc=True)
    rel["latest_release"] = pd.to_datetime(rel["latest_release"], utc=True)
    return usage.merge(
        rel[["name", "first_release", "latest_release"]], on="name", how="left"
    )


def md_table(df: pd.DataFrame, cols: list[str]) -> str:
    """Render a compact markdown table."""
    if df.empty:
        return "_none_"
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if c == "first_release" and pd.notna(v):
                cells.append(str(v)[:10])
            elif c == "template_era":
                cells.append(str(v))
            elif c == "evidence":
                cells.append(str(v)[:80])
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> int:
    df = load()
    n_total = len(df)
    flagged = df["template_era"].isin(TPL_ERAS)
    n_flagged = int(flagged.sum())

    new = df[df["first_release"] >= CUT].copy()
    new_tpl = new[new["template_era"].isin(TPL_ERAS)].sort_values("first_release")
    new_other = new[~new["template_era"].isin(TPL_ERAS)].sort_values("first_release")

    counts = df["template_era"].value_counts()

    lines: list[str] = []
    lines.append("# napari-plugin-template usage")
    lines.append("")
    lines.append(
        f"Generated {GENERATED} from npe2api `extended_summary.json` "
        f"({n_total} plugins), GitHub repo inspection, and PyPI descriptions. "
        "The napari-plugin-template used **cookiecutter** until 2024-06-13, then "
        "switched to **copier**."
    )
    lines.append("")

    # ── Summary ───────────────────────────────────────────────────────────
    lines.append("## Summary")
    lines.append("")
    lines.append(
        f"**{n_flagged} of {n_total} plugins ({n_flagged / n_total:.0%})** show "
        "evidence of having used the napari-plugin-template."
    )
    lines.append("")
    rows = []
    for era in ("cookiecutter", "copier", "template", "no", "no_github", "unavailable"):
        rows.append((era, int(counts.get(era, 0))))
    lines.append(md_table(pd.DataFrame(rows, columns=["era", "count"]), ["era", "count"]))
    lines.append("")
    lines.append(
        f"New plugins since 2025-09-01: **{len(new)}**, of which "
        f"**{len(new_tpl)} ({len(new_tpl) / len(new):.0%})** use the template."
    )
    lines.append("")

    # ── Methodology ───────────────────────────────────────────────────────
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "Each plugin's GitHub repo (from `github_repos.csv`) is checked for "
        "template fingerprints; plugins with no reachable repo are checked "
        "via their PyPI long description. Evidence is ranked:"
    )
    lines.append("")
    lines.append("- **`.copier-answers.yml`** — copier-generated (napari template keys / "
                 "`_src_path` -> napari-plugin-template).")
    lines.append("- **`.cookiecutter.json`** — cookiecutter-generated (napari template keys).")
    lines.append("- **README** — generation statement "
                 "(\"generated with [copier|cookiecutter] using the "
                 "[napari-plugin-template|cookiecutter-napari-plugin]\"), the template "
                 "badge block (napari-hub shields + codecov), or the template README footer.")
    lines.append("- **`.napari-hub/` + `.github/workflows/test_and_deploy.yml`** — weak signal.")
    lines.append("- **PyPI description** — same markers, used as fallback for no_github / "
                 "deleted / private repos.")
    lines.append("")
    lines.append(
        "Eras: **cookiecutter** (pre-2024-06), **copier** (2024-06+), "
        "**template** (evidence but era ambiguous), **no** (no evidence found), "
        "**no_github** (no GitHub URL in metadata), **unavailable** (repo gone)."
    )
    lines.append("")

    # ── New since 2025-09-01 ──────────────────────────────────────────────
    lines.append("## New plugins since 2025-09-01 using the template")
    lines.append("")
    lines.append(f"**{len(new_tpl)}** of {len(new)} new plugins.")
    lines.append("")
    lines.append(
        md_table(
            new_tpl[["name", "first_release", "template_era", "evidence"]],
            ["name", "first_release", "template_era", "evidence"],
        )
    )
    lines.append("")
    lines.append("### New plugins NOT flagged")
    lines.append("")
    lines.append(
        md_table(
            new_other[["name", "first_release", "template_era"]],
            ["name", "first_release", "template_era"],
        )
    )
    lines.append("")

    # ── Full table ────────────────────────────────────────────────────────
    lines.append("## All plugins")
    lines.append("")
    all_sorted = df.sort_values(["template_era", "name"])
    lines.append(
        md_table(
            all_sorted[["name", "first_release", "template_era", "evidence"]],
            ["name", "first_release", "template_era", "evidence"],
        )
    )
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
