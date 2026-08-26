# legacy-analysis — archived exploratory analysis

This directory preserves the **original, superseded** exploratory analysis
from the early days of the project (Sep–Oct 2025). It is **archived for
reference only** — it is not maintained, and it does not run as part of the
current pipeline.

## Contents

| Path | What it is |
|------|------------|
| `analysis/plugin_analyzer.py` | The original `PluginAnalyzer` class (npe2api fetch + seaborn/matplotlib analysis) |
| `src/nps/` | An early, experimental `nps` package (`analysis.py`, `io.py`) — `notebook_import_example.py` imports a module name that never matched, so it was never wired up |
| `simple_analysis.py` | Text-only analysis driver using `analysis.plugin_analyzer` |
| `run_analysis.py` | Visualization driver using `analysis.plugin_analyzer` |
| `example_analysis.py` | Demo script for `analysis.plugin_analyzer` |
| `notebook_import_example.py` | Example of importing the experimental `src/nps` package |
| `nps_analysis.ipynb` | Heavy exploratory notebook (~4.7 MB, mostly inline outputs) |
| `napari_plugin_infrastructure_analysis.ipynb` | Earlier exploratory notebook |

## Relationship to the current pipeline

The current, maintained analysis lives in `scripts/` (fetch → compute → plot,
orchestrated by `scripts/run_all.py`) and writes to `data/`, `plots/`, and
`reports/`. The methodology here (npe2api `classifiers.json` +
`extended_summary.json`, status/license/version/distribution analysis) was the
seed for that pipeline. Keep this archive for the historical methodology; do
not build new work on it.
