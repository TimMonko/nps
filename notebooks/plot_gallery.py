import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full", app_title="nps plot gallery")


@app.cell
def _():
    import altair as alt
    import marimo as mo

    import nps.theme
    from nps import data, plots

    return alt, data, mo, plots


@app.cell
def _(mo):
    mo.md("""
    # nps plot gallery

    Every plot in both slide themes, rendered to the same SVGs the deck uses
    (`nps.plots.render`). Edit `src/nps/plots.py` or `theme.py` and save:
    marimo reloads the module and redraws (auto-reload is on in `pyproject.toml`).
    """)
    return


@app.cell
def _(mo):
    # IBM Plex for inline SVGs; the slides load it the same way
    mo.Html(
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=IBM+Plex+Sans:wght@400;600&display=swap">'
        "<style>.gallery svg { max-width: 100%; height: auto; display: block; }</style>"
    )
    return


@app.cell
def _(data, plots):
    charts = {
        "contributors_by_year": plots.contributors_by_year(data.contributors_by_year()),
        "new_plugins_by_year": plots.new_plugins_by_year(data.new_plugins_by_year()),
        "plugin_maintenance": plots.plugin_maintenance(data.plugin_maintenance()),
        "pypi_downloads (month)": plots.pypi_downloads(data.pypi_downloads()),
        "pypi_downloads (year)": plots.pypi_downloads(data.pypi_downloads(), by="year"),
        "template_usage_by_year": plots.template_usage_by_year(data.template_usage_by_year()),
    }
    return (charts,)


@app.cell
def _(mo):
    slides = mo.ui.switch(value=True, label="slide size (1280x720 deck)")
    slides
    return (slides,)


@app.cell
def _(charts, mo, plots, slides):
    def _pair(chart):
        return mo.hstack(
            [
                mo.Html(f'<div class="gallery">{plots.render(chart, mode, slides=slides.value)}</div>')
                for mode in ("dark", "light")
            ],
            widths="equal",
            gap=1,
        )

    mo.vstack([mo.vstack([mo.md(f"## `{name}`"), _pair(chart)]) for name, chart in charts.items()])
    return


@app.cell
def _(mo):
    mo.md("""
    ## Interactive (as it would embed in a slide)
    """)
    return


@app.cell
def _(charts, mo):
    pick = mo.ui.dropdown(list(charts), value="plugin_maintenance", label="plot")
    mode = mo.ui.radio(["dark", "light"], value="dark", label="theme", inline=True)
    mo.hstack([pick, mode], justify="start")
    return mode, pick


@app.cell
def _(alt, charts, mo, mode, pick, slides):
    _name = f"napari-{mode.value}" + ("-slides" if slides.value else "")
    with alt.theme.enable(_name):
        _spec = charts[pick.value].to_dict()
    mo.ui.altair_chart(alt.Chart.from_dict(_spec) if "layer" not in _spec else alt.LayerChart.from_dict(_spec))
    return


if __name__ == "__main__":
    app.run()
