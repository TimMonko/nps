"""The nps plots: DataFrame in, ``alt.Chart`` out.

Each function takes the frame from the matching loader in ``nps.data`` and
sets no colours, fonts or sizes; enable a theme from ``nps.theme`` first.
Callers can add ``.properties(width=..., height=..., title=...)``.

    import nps.theme
    from nps import data, plots

    nps.theme.enable("dark", slides=True)
    plots.contributors_by_year(data.contributors_by_year())
"""

from __future__ import annotations

from typing import Literal

import altair as alt
import pandas as pd

YTD_OPACITY = 0.55
YEAR_TICKS = alt.Axis(title=None, format="%Y", tickCount="year")


def _year_axis(df: pd.DataFrame) -> alt.Axis:
    """A year axis that labels the current, partial year 'YYYY YTD'."""
    ytd_years = sorted(df.loc[df["ytd"], "year"].unique())
    if not ytd_years:
        return alt.Axis(title=None)
    y = int(ytd_years[-1])
    return alt.Axis(title=None, labelExpr=f"datum.value == {y} ? '{y} YTD' : datum.value")


def _ytd_opacity() -> alt.OpacityValue:
    return alt.condition("datum.ytd", alt.value(YTD_OPACITY), alt.value(1.0))


def contributors_by_year(df: pd.DataFrame) -> alt.Chart:
    """Stacked bars of new and returning contributors per year.

    ``df`` is ``nps.data.contributors_by_year()``.
    """
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("year:O", axis=_year_axis(df)),
            y=alt.Y("contributors:Q", title="Contributors", stack="zero"),
            color=alt.Color("kind:N", sort=["New", "Returning"]),
            order=alt.Order("kind:N", sort="ascending"),
            opacity=_ytd_opacity(),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("kind:N", title="Contributors"),
                alt.Tooltip("contributors:Q", title="Count"),
            ],
        )
    )


def new_plugins_by_year(df: pd.DataFrame) -> alt.LayerChart:
    """New plugins per year (bars, left axis) and the running total (line, right axis).

    ``df`` is ``nps.data.new_plugins_by_year()``.
    """
    base = alt.Chart(df).encode(x=alt.X("year:O", axis=_year_axis(df)))
    tooltip = [
        alt.Tooltip("year:O", title="Year"),
        alt.Tooltip("new_plugins:Q", title="New plugins"),
        alt.Tooltip("total_plugins:Q", title="Total plugins"),
    ]
    bars = base.mark_bar().encode(
        y=alt.Y("new_plugins:Q", title="New plugins per year"),
        color=alt.datum("New that year"),
        opacity=_ytd_opacity(),
        tooltip=tooltip,
    )
    total = base.mark_line(point=True).encode(
        y=alt.Y("total_plugins:Q", title="Total plugins"),
        color=alt.datum("Total so far"),
        tooltip=tooltip,
    )
    return (
        alt.layer(bars, total)
        .resolve_scale(y="independent")
        .configure_legend(title=None)
    )


def plugin_maintenance(df: pd.DataFrame, trailing_months: int = 6) -> alt.Chart:
    """All plugins released so far, and those with a release in the trailing window.

    ``df`` is ``nps.data.plugin_maintenance()``.
    """
    active = f"Released in the last {trailing_months} months"
    return (
        alt.Chart(df)
        .transform_calculate(**{"All plugins": "datum.total_plugins", active: "datum.active_plugins"})
        .transform_fold(["All plugins", active], as_=["series", "plugins"])
        .mark_line()
        .encode(
            x=alt.X("month:T", axis=YEAR_TICKS),
            y=alt.Y("plugins:Q", title="Plugins"),
            color=alt.Color("series:N", sort=["All plugins", active]),
            tooltip=[
                alt.Tooltip("yearmonth(month):T", title="Month"),
                alt.Tooltip("total_plugins:Q", title="All plugins"),
                alt.Tooltip("active_plugins:Q", title=active),
                alt.Tooltip("maintenance_ratio:Q", title="Share active", format=".0%"),
            ],
        )
    )


def pypi_downloads(
    df: pd.DataFrame, by: Literal["month", "year"] = "month"
) -> alt.Chart:
    """PyPI downloads per month (bars) or per year.

    ``df`` is ``nps.data.pypi_downloads()``. With ``by="year"``, the current
    year is a partial total and drawn faded.
    """
    if by == "year":
        yearly = (
            df.assign(year=df["month"].dt.year)
            .groupby("year", as_index=False)["downloads"]
            .sum()
        )
        yearly["ytd"] = yearly["year"] == pd.Timestamp.today().year
        return (
            alt.Chart(yearly)
            .mark_bar()
            .encode(
                x=alt.X("year:O", axis=_year_axis(yearly)),
                y=alt.Y("downloads:Q", title="Downloads per year", axis=alt.Axis(format="~s")),
                opacity=_ytd_opacity(),
                tooltip=[
                    alt.Tooltip("year:O", title="Year"),
                    alt.Tooltip("downloads:Q", title="Downloads", format=","),
                ],
            )
        )
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("yearmonth(month):T", axis=YEAR_TICKS),
            y=alt.Y("downloads:Q", title="Downloads per month", axis=alt.Axis(format="~s")),
            tooltip=[
                alt.Tooltip("yearmonth(month):T", title="Month"),
                alt.Tooltip("downloads:Q", title="Downloads", format=","),
            ],
        )
    )
