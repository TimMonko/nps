# nps — AI Coding Agent Instructions

napari plugin sustainability (nps) — organization, coordination, and metrics
for the napari plugin sustainability initiative. This is the URSSI Early
Career Fellowship project to analyze the health and sustainability of the
napari plugin ecosystem (~500+ plugins) and improve long-term plugin
maintenance through community working groups.

## Structure

```
_quarto.yml, _brand.yml     # Quarto website config; brand = colours/fonts/logos
site/                       # Website pages (.qmd), rendered to _site/ (Pages)
.github/workflows/pages.yml # Renders the site from committed data, deploys on main
fellowship/                 # Fellowship narrative: proposal, blogs, conferences, final report
    blog/                   #   Blog posts (published + drafts) + planning
    conferences/            #   Conference talk materials (SciPy 2026, EuroSciPy 2026)
    final-report/           #   URSSI final report, CV, per-release contributor table
community/                  # Working-group announcement, meeting notes, one-pager
scripts/                    # Active metrics pipeline (fetch_*, compute_*, plot_*, run_all.py)
notebooks/                  # marimo notebooks for exploring metrics
data/                       # Cached input data + data/metrics/ (computed CSVs)
plots/                      # Generated plots (png + svg + interactive html)
reports/                    # Generated ecosystem reports
```

## Metrics pipeline

Environments are managed by pixi from `pyproject.toml` (`pixi.lock`
committed; no uv). Dependency groups and extras are pixi features; the
environments are `default`, `dev` (tests), `site` (Quarto from conda-forge),
`plot` (Plotly) and `notebook` (marimo). Script output is plain ASCII (no
non-ASCII printed to stdout/stderr), so the pipeline works on any
platform/console without `PYTHONUTF8` or similar.

```sh
pixi run pipeline     # full run: fetch → compute → plot
pixi run recompute    # recompute + replot from cached data (no network)
pixi run test         # pytest, dev environment
pixi run render       # site -> _site/, site environment
pixi run preview      # quarto preview, site environment
```

### Release-contributors analysis

- `pixi run python scripts/build_release_contributors.py` → `data/release_contributors.csv` (part of
  `pixi run refresh`; keeps blobless napari + napari/docs clones in `.cache/`; `gh` for release dates;
  `--out x.md` also writes the Markdown table; `--as-of` freezes the date). The copy in
  `fellowship/final-report/` is the report's frozen 2026-08-25 version.
- `pixi run python scripts/plot_release_contributors.py` → `plots/release_new_contributors.{png,svg}`;
  `pixi run -e plot python scripts/plot_release_contributors.py --interactive` →
  `plots/release_new_contributors_interactive.html`.

## Data sources

- **classifiers.json** — plugin categorization data (active/withdrawn/deleted) with version histories
- **extended_summary.json** — detailed plugin metadata (PyPI/conda versions, license, authors, URLs, dependencies)
- **GitHub API** — per-repo commit dumps (`data/commits_napari_*.json`, public repos only), contributor lists, release data
- **PyPI JSON API** — upload time of every plugin release (`data/plugin_versions.csv`)
- **ClickHouse public PyPI dataset** — napari monthly downloads (`data/pypi_downloads_monthly.csv`), no key

Both JSON files are fetched from `napari/npe2api` into `data/` (there is no
`public/` dir anymore). `data/` is committed as-is; treat it as regenerable
pipeline output.

## Key conventions

- **`src/nps/` is the plotting package** (installed editable in every pixi environment):
  `nps.data` loads the committed data as tidy DataFrames (never fetches),
  `nps.plots` turns them into Altair charts with no colours or fonts of their
  own, and `nps.theme` registers `napari-light`/`napari-dark` (plus `-slides`)
  Altair themes built from `_brand.yml`. Enable a theme before plotting.
  Other repos (napari-talks) depend on it by path. Tests: `pixi run test`.
- **`_brand.yml` is the one source** for colours, fonts and logos (Quarto
  site and Altair themes). Light/dark colour values need Quarto >= 1.8.
- **The pipeline lives in `scripts/`** (fetch → compute → CSVs in `data/`).
  The old `legacy-analysis/` code was deleted (git history has it); don't
  bring it back.
- **The site (`site/*.qmd`) is thin**: each page includes `site/_setup.qmd`
  and shows charts with `show(plots.x(data.x()))` in a cell with
  `#| renderings: [light, dark]`, so the chart follows the site's theme
  toggle. Pages include `fellowship/` and `community/` Markdown rather than
  copying it; keep page text short. CI renders, never fetches. Pages live in
  `site/`, so URLs are `/nps/site/<page>.html`; `/nps/` redirects there.
- **Tools come from the project env**: Quarto is the conda-forge `quarto`
  package in the `site` pixi feature (`pixi run -e site quarto ...`), never a
  global install.
- **Data analysis approach**: start exploratory, identify outliers/edge cases,
  visualize trends, and end every analysis with actionable recommendations.
  Validate assumptions against the actual plugin data (field names come from
  the npe2api JSON files).
- **Working-group notes**: append to the single growing
  `community/working-group-meeting-notes.md`; `scripts/build_wg_notes_prefix.py`
  regenerates historical prefixes.
- **Blog posts**: drafts and planning docs live in `fellowship/blog/`; the
  published posts live on [The Island Dispatch](https://napari.org/island-dispatch/).
  The canonical fellowship proposal is `fellowship/proposal.md`.
