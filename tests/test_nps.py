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
    (data.template_usage_by_year, plots.template_usage_by_year),
    (data.active_contributors, plots.active_contributors),
    (data.release_contributors, plots.release_contributors),
    (data.release_contributors, lambda df: plots.release_contributors(df, cadence_since="2026-09-22")),
    (data.newcomer_first_repo, plots.newcomer_first_repo),
    (data.newcomer_retention, plots.newcomer_retention),
    (data.python_support, plots.python_support),
    (data.plugin_status, plots.plugin_status),
    (data.plugin_status, lambda df: plots.plugin_status(df, share=True)),
    (data.pypi_downloads_by_system, plots.pypi_downloads_desktop),
    (data.pypi_downloads_by_system, lambda df: plots.pypi_downloads_desktop(df, by="month")),
]


def test_plugin_status_states_add_up_to_all_plugins():
    df = data.plugin_status()
    per_month = df.groupby("month")["plugins"].sum()
    versions = pd.read_csv(data.DATA_DIR / "plugin_versions.csv")
    assert per_month.iloc[-1] == versions["name"].nunique()
    assert per_month.is_monotonic_increasing
    assert df.groupby("month")["share"].sum().round(9).isin([0, 1]).all()


def test_downloads_by_system_matches_total():
    """Splitting by OS loses no downloads (the two ClickHouse tables differ by a handful)."""
    total = data.pypi_downloads().set_index("month")["downloads"]
    split = data.pypi_downloads_by_system().groupby("month")["downloads"].sum()
    assert ((split.reindex(total.index) - total).abs() <= total * 0.001 + 20).all()


def test_contributors_by_year_shape():
    df = data.contributors_by_year()
    assert list(df.columns) == ["year", "kind", "contributors", "ytd"]
    assert set(df["kind"]) == {"New", "Returning"}
    assert df["ytd"].sum() <= 2  # at most one year, two kinds


def test_release_cycles_tile_without_overlap():
    df = data.release_contributors()
    assert (df["end"] > df["start"]).all()
    assert (df["start"].iloc[1:].values >= df["end"].iloc[:-1].values).all()
    assert (df["returning"] >= 0).all()
    assert df["in_development"].sum() <= 1


def test_copied_history_dropped():
    commits = pd.DataFrame(
        {
            "repo": ["napari/napari-sphinx-theme", "napari/napari-sphinx-theme", "napari/napari"],
            "date": ["2020-01-01T00:00:00Z", "2023-01-01T00:00:00Z", "2020-01-01T00:00:00Z"],
        }
    )
    assert data.drop_copied_history(commits).index.tolist() == [1, 2]


def test_newcomers_counted_once():
    first = data.newcomer_first_repo()
    assert first["contributors"].sum() == data._commits()["login"].nunique()


def test_retention_shares_are_fractions():
    df = data.newcomer_retention()
    assert df["share"].between(0, 1).all()
    assert (df["returned"] <= df["newcomers"]).all()


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


def test_save_writes_one_file_per_theme(tmp_path):
    chart = plots.contributors_by_year(data.contributors_by_year())
    paths = plots.save(chart, tmp_path / "contributors", formats=("svg", "png"))
    assert sorted(p.name for p in paths) == [
        "contributors-dark.png",
        "contributors-dark.svg",
        "contributors-light.png",
        "contributors-light.svg",
    ]
    dark = (tmp_path / "contributors-dark.svg").read_text(encoding="utf-8")
    light = (tmp_path / "contributors-light.svg").read_text(encoding="utf-8")
    palette = nps.theme.load_brand()["color"]["palette"]
    assert palette["ground-dark"] in dark and palette["ground-light"] in light


def test_template_usage_counts_every_new_plugin():
    usage = data.template_usage_by_year().groupby("year")["plugins"].sum()
    new = data.new_plugins_by_year().set_index("year")["new_plugins"]
    assert (usage.reindex(new.index, fill_value=0) == new).all()
