# nps — AI Coding Agent Instructions

napari plugin sustainability (nps) — organization, coordination, and metrics
for the napari plugin sustainability initiative. This is the URSSI Early
Career Fellowship project to analyze the health and sustainability of the
napari plugin ecosystem (~500+ plugins) and improve long-term plugin
maintenance through community working groups.

## Structure

```
fellowship/                 # URSSI proposal + blog posts (published + drafts) + planning
final-report/               # URSSI final report, CV, per-release contributor table
conferences/                # Conference talk materials (SciPy 2026, EuroSciPy 2026)
community/                  # Working-group meeting notes + community one-pager
scripts/                    # Active metrics pipeline (fetch_*, compute_*, plot_*, run_all.py)
notebooks/                  # marimo notebooks for exploring metrics
data/                       # Cached input data + data/metrics/ (computed CSVs)
plots/                      # Generated plots (png + svg + interactive html)
reports/                    # Generated ecosystem reports
legacy-analysis/            # Archived, superseded exploratory analysis (do not build on)
```

## Metrics pipeline

```sh
# Full run: fetch → compute → plot
$env:PYTHONUTF8="1"; .venv\Scripts\python.exe scripts\run_all.py
# Recompute + replot from cached data (no network)
$env:PYTHONUTF8="1"; .venv\Scripts\python.exe scripts\run_all.py --skip-fetch
```

> **Windows gotcha**: run with `PYTHONUTF8=1` — the compute scripts print the
> `→` arrow and crash under the default cp1252 codepage.

### Release-contributors analysis

- `scripts/build_release_contributors.py` → `final-report/new-contributors-by-release.{md,csv}`
  (needs sibling `../napari` with tags + `../napari-docs` + `gh` CLI; `--as-of` freezes the date).
- `scripts/plot_release_contributors.py` → `plots/release_new_contributors.{png,svg}`;
  `--interactive` → `plots/release_new_contributors_interactive.html` (needs the
  `plot` extra: `uv add --optional plot plotly`).

## Data sources

- **classifiers.json** — plugin categorization data (active/withdrawn/deleted) with version histories
- **extended_summary.json** — detailed plugin metadata (PyPI/conda versions, license, authors, URLs, dependencies)
- **GitHub API** — per-repo commit dumps (`data/commits_napari_*.json`), contributor lists, release data

Both JSON files are fetched from `napari/npe2api` into `data/` (there is no
`public/` dir anymore). `data/` is committed as-is; treat it as regenerable
pipeline output.

## Key conventions

- **This is not a distributable Python package** — the `pyproject.toml` is
  just dependency metadata for the analysis scripts. Keep it that way.
- **Active analysis lives in `scripts/`** — do not resurrect
  `legacy-analysis/` code (the old `PluginAnalyzer`, `src/nps/`, or the heavy
  notebooks); it is archived for historical reference only.
- **Data analysis approach**: start exploratory, identify outliers/edge cases,
  visualize trends, and end every analysis with actionable recommendations.
  Validate assumptions against the actual plugin data (field names come from
  the npe2api JSON files).
- **Working-group notes**: append to `community/meeting-notes/` (single
  growing `YYYY-MM-DD_WG_Notes.md` compiled file; `scripts/build_wg_notes_prefix.py`
  regenerates historical prefixes).
- **Blog posts**: drafts and planning docs live in `fellowship/`; the published
  posts live on [The Island Dispatch](https://napari.org/island-dispatch/).
  The canonical fellowship proposal is `fellowship/proposal.md`.
