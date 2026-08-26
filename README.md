# nps — napari plugin sustainability

Organization, coordination, and metrics for the **napari plugin sustainability
initiative** — a community effort (funded by a URSSI Early Career Fellowship)
to keep napari's 500+ plugin ecosystem healthy and connected to core napari.

This repo holds three kinds of content:

1. **Fellowship narrative** — the URSSI proposal, blog posts (URSSI + napari),
   the final report, and conference materials (`fellowship/`, `final-report/`,
   `conferences/`).
2. **Community coordination** — plugin-sustainability working group meeting
   notes and outreach (`community/`).
3. **Ecosystem metrics** — a reproducible analysis pipeline that quantifies
   the health of the napari plugin ecosystem (`scripts/`, `data/`, `plots/`,
   `reports/`).

## Repository layout

```
fellowship/              # URSSI proposal, blog posts (published + drafts), planning
final-report/            # URSSI final report, CV, per-release contributor table
conferences/             # SciPy 2026 + EuroSciPy 2026 talk materials
community/               # Working-group meeting notes + community one-pager
scripts/                 # Active metrics pipeline (fetch → compute → plot)
notebooks/               # marimo notebooks for exploring metrics
data/                    # Cached input data (npe2api, GitHub commits) + data/metrics/
plots/                   # Generated plots (png + svg + interactive html)
reports/                 # Generated ecosystem reports (canonical: latest_ecosystem_report.md)
legacy-analysis/         # Archived, superseded exploratory analysis (kept for reference)
```

## Metrics pipeline

```sh
# Full run: fetch → compute → plot
$env:PYTHONUTF8="1"; .venv\Scripts\python.exe scripts\run_all.py

# Skip network fetch, just recompute + replot from cached data
$env:PYTHONUTF8="1"; .venv\Scripts\python.exe scripts\run_all.py --skip-fetch
```

> **Windows note**: run with `PYTHONUTF8=1` — the compute scripts print the
> `→` arrow and crash under the cp1252 codepage otherwise.

### Release-contributors analysis

```sh
python scripts/build_release_contributors.py        # → final-report/new-contributors-by-release.{md,csv}
python scripts/plot_release_contributors.py         # → plots/release_new_contributors.{png,svg}
python scripts/plot_release_contributors.py --interactive   # → plots/release_new_contributors_interactive.html
```

Requires the `plot` extra for Plotly: `uv add --optional plot plotly`.

## Links

- [The Island Dispatch announcement](https://napari.org/island-dispatch/blog/plugin-sustainability-initiative.html)
- [Working group meeting schedule](https://napari.org/stable/community/meeting_schedule.html)
- [napari hub](https://napari-hub.org)
- [npe2api](https://api.napari.org)
