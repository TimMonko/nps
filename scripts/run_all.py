"""Orchestrator: run the full analysis pipeline.

Usage:
    python scripts/run_all.py              # full pipeline
    python scripts/run_all.py --skip-fetch # skip data fetching, just compute + plot
    python scripts/run_all.py --plots-only # only regenerate plots
    python scripts/run_all.py --velocity   # also run velocity (slow, many API calls)
    python scripts/run_all.py --template-usage  # also re-detect napari-plugin-template
                                              # usage (slow, ~600 GitHub calls) and
                                              # rebuild reports/plugin-template-usage.md
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _run(script: str, step: str) -> bool:
    """Run a Python script. Returns True on success."""
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"  {step}", file=sys.stderr)
    print(f"{'=' * 60}\n", file=sys.stderr, flush=True)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script)],
        cwd=REPO_ROOT,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    skip_fetch = "--skip-fetch" in sys.argv
    plots_only = "--plots-only" in sys.argv
    include_velocity = "--velocity" in sys.argv
    include_template = "--template-usage" in sys.argv

    if plots_only:
        _run("plot_contributors.py", "Plotting contributor metrics")
        _run("plot_plugins.py", "Plotting plugin metrics")
        return 0

    # ── Phase 1: Fetch ──────────────────────────────────────────────────
    if not skip_fetch:
        if not _run("fetch_contributors.py", "Phase 1.1: Fetch contributor data"):
            print(
                "\nWARNING: fetch_contributors.py had failures — continuing anyway.\n",
                file=sys.stderr,
            )

        if not _run("fetch_plugin_data.py", "Phase 1.2: Fetch plugin release data"):
            print(
                "\nWARNING: fetch_plugin_data.py failed.\n",
                file=sys.stderr,
            )

        if not _run("fetch_plugin_contributors.py", "Phase 1.3: Fetch plugin contributors"):
            print(
                "\nWARNING: fetch_plugin_contributors.py failed.\n",
                file=sys.stderr,
            )

        _run("fetch_python_versions.py", "Phase 1.4: Fetch Python version data")

    # ── Template-usage detection (slow — only if requested) ─────────────
    if include_template and not skip_fetch:
        if not _run(
            "detect_plugin_template_usage.py",
            "Phase 1.5: Detect napari-plugin-template usage",
        ):
            print(
                "\nWARNING: detect_plugin_template_usage.py failed — ",
                "template chart will be skipped or stale.\n",
                file=sys.stderr,
            )

    # ── Phase 2: Compute metrics ────────────────────────────────────────
    _run("compute_contributor_metrics.py", "Phase 2.1: Compute contributor metrics")
    _run("compute_plugin_metrics.py", "Phase 2.2: Compute plugin metrics")
    _run("compute_overlap.py", "Phase 2.3: Compute plugin-dev overlap")

    # ── Velocity (slow — runs last, only if requested) ──────────────────
    if include_velocity:
        _run("compute_velocity.py", "Phase 2.x: Compute velocity (commits/month)")

    # ── Phase 3: Plot ───────────────────────────────────────────────────
    _run("plot_contributors.py", "Phase 3.1: Plot contributor metrics")
    _run("plot_plugins.py", "Phase 3.2: Plot plugin metrics")
    _run("plot_python_versions.py", "Phase 3.3: Plot Python version support")

    # ── Report (only if template detection was run) ─────────────────────
    if include_template:
        _run(
            "build_plugin_template_usage_report.py",
            "Phase 4: Build plugin-template-usage report",
        )

    print("\n✅ Pipeline complete!", file=sys.stderr)
    print(f"   Plots in: {REPO_ROOT / 'plots'}", file=sys.stderr)
    print(f"   Metrics in: {REPO_ROOT / 'data' / 'metrics'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
