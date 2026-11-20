"""Smoke tests for nps.data, nps.theme and nps.plots against the committed data."""

from __future__ import annotations

import altair as alt
import pandas as pd
import pytest
import vl_convert as vlc

import nps.theme
from nps import data, plots

LOADERS_AND_PLOTS = [
    (data.contributors_by_year, plots.contributors_by_year),
    (data.new_plugins_by_year, plots.new_plugins_by_year),
    (data.plugin_maintenance, plots.plugin_maintenance),
    (data.pypi_downloads, plots.pypi_downloads),
]


def test_contributors_by_year_shape():
    df = data.contributors_by_year()
    assert list(df.columns) == ["year", "kind", "contributors", "ytd"]
    assert set(df["kind"]) == {"New", "Returning"}
    assert df["ytd"].sum() <= 2  # at most one year, two kinds


def test_new_plugins_total_is_cumulative():
    df = data.new_plugins_by_year()
    assert (df["total_plugins"] == df["new_plugins"].cumsum()).all()
    assert df["year"].is_monotonic_increasing


def test_maintenance_active_never_exceeds_total():
    df = data.plugin_maintenance()
    assert (df["active_plugins"] <= df["total_plugins"]).all()
    assert pd.api.types.is_datetime64_any_dtype(df["month"])


def test_pypi_downloads_unknown_project():
    with pytest.raises(ValueError):
        data.pypi_downloads("not-a-project")


def test_themes_registered_from_brand():
    for name in nps.theme.THEMES:
        assert name in alt.theme.names()
    brand = nps.theme.load_brand()
    dark = nps.theme.theme_config("dark")["config"]
    assert dark["background"] == brand["color"]["palette"]["ground-dark"]
    assert dark["range"]["category"][0] == brand["color"]["palette"]["series-1-dark"]
    assert len(dark["range"]["category"]) == 4


@pytest.mark.parametrize("theme", ["napari-light", "napari-dark-slides"])
@pytest.mark.parametrize(("load", "plot"), LOADERS_AND_PLOTS)
def test_plots_render(load, plot, theme):
    with alt.theme.enable(theme):
        chart = plot(load())
        spec = chart.to_dict()  # validates against the Vega-Lite schema
    svg = vlc.vegalite_to_svg(spec)
    assert svg.startswith("<svg")


def test_plots_set_no_colours():
    """Colours come from the theme, not the plot functions."""
    for load, plot in LOADERS_AND_PLOTS:
        spec = plot(load()).to_json()
        assert "#" not in spec.replace("#/", "")  # no hex colours (ignore JSON refs)


def test_downloads_by_year_marks_ytd():
    chart = plots.pypi_downloads(data.pypi_downloads(), by="year")
    assert "YTD" in chart.to_json()
