# nps — napari plugin sustainability

Organization, coordination, and metrics for the **napari plugin sustainability
initiative** — a community effort (funded by a URSSI Early Career Fellowship)
to keep napari's 500+ plugin ecosystem healthy and connected to core napari.

This repo holds three kinds of content:

1. **Fellowship narrative** — the URSSI proposal, blog posts, final report,
   and conference materials (`fellowship/`).
2. **Community coordination** — plugin-sustainability working group meeting
   notes and outreach (`community/`).
3. **Ecosystem metrics** — a reproducible analysis pipeline that quantifies
   the health of the napari plugin ecosystem (`scripts/`, `data/`, `plots/`,
   `reports/`).

## Repository layout

```
fellowship/              # Fellowship narrative: proposal, blogs, conferences, final report
    blog/                #   Blog posts (published + drafts) + planning
    conferences/         #   SciPy 2026 + EuroSciPy 2026 talk materials
    final-report/        #   URSSI final report, CV, per-release contributor table
community/               # Working-group announcement, meeting notes, one-pager
scripts/                 # Active metrics pipeline (fetch → compute → plot)
notebooks/               # marimo notebooks for exploring metrics
data/                    # Cached input data (npe2api, GitHub commits) + data/metrics/
plots/                   # Generated plots (png + svg + interactive html)
reports/                 # Generated ecosystem reports (canonical: latest_ecosystem_report.md)
legacy-analysis/         # Archived, superseded exploratory analysis (kept for reference)
```

## Metrics pipeline

Everything runs through `uv run python` — uv manages the environment from
`pyproject.toml` / `uv.lock`, so there's no manual venv activation. Script
output is plain ASCII, so the pipeline works on any platform/console without
special env vars.

```sh
# Full run: fetch → compute → plot
uv run python scripts/run_all.py

# Skip network fetch, just recompute + replot from cached data
uv run python scripts/run_all.py --skip-fetch
```

### Release-contributors analysis

```sh
uv run python scripts/build_release_contributors.py      # → fellowship/final-report/new-contributors-by-release.{md,csv}
uv run python scripts/plot_release_contributors.py       # → plots/release_new_contributors.{png,svg}
uv run --extra plot python scripts/plot_release_contributors.py --interactive  # → plots/release_new_contributors_interactive.html
```

The interactive plot needs Plotly (optional `plot` extra):
`uv add --optional plot plotly`, then `uv run --extra plot python ...`.

## Links

- [The Island Dispatch announcement](https://napari.org/island-dispatch/blog/plugin-sustainability-initiative.html)
- [Working group meeting schedule](https://napari.org/stable/community/meeting_schedule.html)
- [napari hub](https://napari-hub.org)
- [npe2api](https://api.napari.org)
