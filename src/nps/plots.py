"""The nps plots: DataFrame in, ``alt.Chart`` out.

Each function takes the frame from the matching loader in ``nps.data`` and
sets no colours, fonts or sizes; enable a theme from ``nps.theme`` first, or
use ``save()`` to write one file per theme. Text uses the theme's named styles
(``label`` for direct labels, ``note`` for asides), so it follows the theme too.

    import nps.theme
    from nps import data, plots

    nps.theme.enable("dark", slides=True)
    plots.contributors_by_year(data.contributors_by_year())

    # or: one SVG per theme, for slides that switch light/dark
    plots.save(plots.plugin_maintenance(data.plugin_maintenance()), "figures/maintenance")
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Literal

import altair as alt
import pandas as pd

from nps import theme as _theme

YEAR_TICKS = alt.Axis(title=None, format="%Y", tickCount="year")
LABEL_GAP = 8  # px between a mark and its direct label


def _year_axis(df: pd.DataFrame) -> alt.Axis:
    """A year axis that labels the current, partial year 'YYYY YTD'."""
    ytd_years = sorted(df.loc[df["ytd"], "year"].unique())
    if not ytd_years:
        return alt.Axis(title=None)
    y = int(ytd_years[-1])
    return alt.Axis(title=None, labelExpr=f"datum.value == {y} ? '{y} YTD' : datum.value")


def _so_far_note(df: pd.DataFrame, y_field: str) -> alt.Chart | None:
    """A muted 'so far' note above the current, partial year's bar."""
    last = df[df["ytd"]]
    if last.empty:
        return None
    totals = last.groupby("year", as_index=False)[y_field].sum()
    totals["note"] = "so far"
    return (
        alt.Chart(totals)
        .mark_text(style="note", baseline="bottom", dy=-LABEL_GAP)
        .encode(x="year:O", y=f"{y_field}:Q", text="note:N")
    )


def _layer(*charts: alt.Chart | None) -> alt.LayerChart:
    return alt.layer(*[c for c in charts if c is not None])


def contributors_by_year(df: pd.DataFrame) -> alt.LayerChart:
    """Returning (bottom) and new (top) contributors per year, labelled directly.

    ``df`` is ``nps.data.contributors_by_year()``.
    """
    stack = (
        alt.Chart(df)
        .transform_calculate(stack_order="datum.kind == 'Returning' ? 0 : 1")
        .encode(
            x=alt.X("year:O", axis=_year_axis(df)),
            y=alt.Y("contributors:Q", title="active contributors", stack="zero"),
            color=alt.Color("kind:N", sort=["New", "Returning"], legend=None),
            order=alt.Order("stack_order:Q"),
        )
    )
    bars = stack.mark_bar().encode(
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("kind:N", title="Contributors"),
            alt.Tooltip("contributors:Q", title="Count"),
        ]
    )

    # direct labels beside the middle of each segment of the last bar
    last_year = df["year"].max()
    last = df[df["year"] == last_year].set_index("kind")["contributors"]
    returning, new = int(last.get("Returning", 0)), int(last.get("New", 0))
    labels = pd.DataFrame(
        {
            "year": [last_year, last_year],
            "y": [returning / 2, returning + new / 2],
            "label": ["returning", "new"],
        }
    )
    label_marks = (
        alt.Chart(labels)
        .mark_text(style="label", align="left", baseline="middle", dx=LABEL_GAP)
        .encode(
            x=alt.X("year:O", bandPosition=1),
            y="y:Q",
            text="label:N",
        )
    )
    return _layer(bars, label_marks, _so_far_note(df, "contributors"))


def active_contributors(df: pd.DataFrame) -> alt.LayerChart:
    """Contributors active in the trailing six months: everyone, and plugin developers.

    ``df`` is ``nps.data.active_contributors()``. Each line is labelled at its end.
    """
    groups = ["all contributors", "also plugin developers"]
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("month:T", axis=YEAR_TICKS),
            y=alt.Y("contributors:Q", title="active in the last 6 months"),
            color=alt.Color("group:N", sort=groups, scale=alt.Scale(domain=groups), legend=None),
            tooltip=[
                alt.Tooltip("yearmonth(month):T", title="Month"),
                alt.Tooltip("group:N", title="Group"),
                alt.Tooltip("contributors:Q", title="Contributors"),
            ],
        )
    )
    ends = df[df["month"] == df["month"].max()].assign(label=lambda d: d["group"])
    labels = (
        alt.Chart(ends)
        .mark_text(style="label", align="left", baseline="middle", dx=LABEL_GAP)
        .encode(x="month:T", y="contributors:Q", text="label:N")
    )
    return _layer(lines, labels)


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
        y=alt.Y("new_plugins:Q", title="new plugins per year"),
        color=alt.datum("new that year"),
        tooltip=tooltip,
    )
    total = base.mark_line(point=True).encode(
        y=alt.Y("total_plugins:Q", title="total plugins"),
        color=alt.datum("total so far"),
        tooltip=tooltip,
    )
    return alt.layer(bars, total).resolve_scale(y="independent")


def plugin_maintenance(df: pd.DataFrame, trailing_months: int = 6) -> alt.LayerChart:
    """All plugins released so far, and those with a release in the trailing window.

    ``df`` is ``nps.data.plugin_maintenance()``. Each line is labelled at its end.
    """
    active = f"released in the last {trailing_months} months"
    series = ["all plugins", active]
    lines = (
        alt.Chart(df)
        .transform_calculate(**{"all plugins": "datum.total_plugins", active: "datum.active_plugins"})
        .transform_fold(series, as_=["series", "plugins"])
        .mark_line()
        .encode(
            x=alt.X("month:T", axis=YEAR_TICKS),
            y=alt.Y("plugins:Q", title="plugins"),
            color=alt.Color("series:N", sort=series, legend=None),
            tooltip=[
                alt.Tooltip("yearmonth(month):T", title="Month"),
                alt.Tooltip("total_plugins:Q", title="All plugins"),
                alt.Tooltip("active_plugins:Q", title="Recently released"),
                alt.Tooltip("maintenance_ratio:Q", title="Share recent", format=".0%"),
            ],
        )
    )
    last = df.iloc[-1]
    ends = pd.DataFrame(
        {
            "month": [last["month"], last["month"]],
            "plugins": [last["total_plugins"], last["active_plugins"]],
            "label": series,
        }
    )
    labels = (
        alt.Chart(ends)
        .mark_text(style="label", align="left", baseline="middle", dx=LABEL_GAP)
        .encode(x="month:T", y="plugins:Q", text="label:N")
    )
    return _layer(lines, labels)


def template_usage_by_year(df: pd.DataFrame) -> alt.LayerChart:
    """New plugins per year, stacked by napari-plugin-template usage.

    ``df`` is ``nps.data.template_usage_by_year()``. Plugins with no public
    repo to check are stacked on top in the theme's muted context colour.
    """
    kinds = ["used the template", "no template", "no public repo"]
    bars = (
        alt.Chart(df)
        .transform_calculate(stack_order=f"indexof({kinds}, datum.kind)")
        .mark_bar()
        .encode(
            x=alt.X("year:O", axis=_year_axis(df)),
            y=alt.Y("plugins:Q", title="new plugins per year", stack="zero"),
            # ordinal: the theme colours the last kind as context
            color=alt.Color("kind:O", sort=kinds, scale=alt.Scale(domain=kinds)),
            order=alt.Order("stack_order:Q"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("kind:N", title="Template"),
                alt.Tooltip("plugins:Q", title="New plugins"),
            ],
        )
    )
    return _layer(bars, _so_far_note(df, "plugins"))


def pypi_downloads(
    df: pd.DataFrame, by: Literal["month", "year"] = "month"
) -> alt.Chart | alt.LayerChart:
    """PyPI downloads per month (bars) or per year.

    ``df`` is ``nps.data.pypi_downloads()``. With ``by="year"``, the current,
    partial year gets a "so far" note.
    """
    if by == "year":
        yearly = (
            df.assign(year=df["month"].dt.year)
            .groupby("year", as_index=False)["downloads"]
            .sum()
        )
        yearly["ytd"] = yearly["year"] == pd.Timestamp.today().year
        bars = (
            alt.Chart(yearly)
            .mark_bar()
            .encode(
                x=alt.X("year:O", axis=_year_axis(yearly)),
                y=alt.Y("downloads:Q", title="downloads per year", axis=alt.Axis(format="~s")),
                tooltip=[
                    alt.Tooltip("year:O", title="Year"),
                    alt.Tooltip("downloads:Q", title="Downloads", format=","),
                ],
            )
        )
        return _layer(bars, _so_far_note(yearly, "downloads"))
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("yearmonth(month):T", axis=YEAR_TICKS),
            y=alt.Y("downloads:Q", title="downloads per month", axis=alt.Axis(format="~s")),
            tooltip=[
                alt.Tooltip("yearmonth(month):T", title="Month"),
                alt.Tooltip("downloads:Q", title="Downloads", format=","),
            ],
        )
    )


DESKTOP = ["Windows", "macOS"]


def pypi_downloads_desktop(
    df: pd.DataFrame, by: Literal["month", "year"] = "year"
) -> alt.LayerChart:
    """Windows and macOS downloads, stacked, per year or month; Linux left out.

    ``df`` is ``nps.data.pypi_downloads_by_system()``. CI runs almost entirely
    on Linux, so leaving Linux out removes the CI spikes and keeps the people.
    """
    desktop = df[df["system"].isin(DESKTOP)]
    if by == "year":
        desktop = (
            desktop.assign(year=desktop["month"].dt.year)
            .groupby(["year", "system"], as_index=False)["downloads"]
            .sum()
        )
        desktop["ytd"] = desktop["year"] == pd.Timestamp.today().year
        x = alt.X("year:O", axis=_year_axis(desktop))
        x_tip = alt.Tooltip("year:O", title="Year")
        unit = "year"
    else:
        x = alt.X("yearmonth(month):T", axis=YEAR_TICKS)
        x_tip = alt.Tooltip("yearmonth(month):T", title="Month")
        unit = "month"
    bars = (
        alt.Chart(desktop)
        .transform_calculate(stack_order=f"indexof({DESKTOP}, datum.system)")
        .mark_bar()
        .encode(
            x=x,
            y=alt.Y(
                "downloads:Q",
                title=f"Windows + macOS downloads per {unit}",
                stack="zero",
                axis=alt.Axis(format="~s"),
            ),
            color=alt.Color("system:N", sort=DESKTOP, scale=alt.Scale(domain=DESKTOP), legend=None),
            order=alt.Order("stack_order:Q"),
            tooltip=[
                x_tip,
                alt.Tooltip("system:N", title="System"),
                alt.Tooltip("downloads:Q", title="Downloads", format=","),
            ],
        )
    )
    if by != "year":
        return _layer(bars)
    # direct labels beside the middle of each segment of the last bar
    last_year = desktop["year"].max()
    last = desktop[desktop["year"] == last_year].set_index("system")["downloads"]
    win, mac = int(last.get("Windows", 0)), int(last.get("macOS", 0))
    labels = pd.DataFrame(
        {"year": [last_year] * 2, "y": [win / 2, win + mac / 2], "label": DESKTOP}
    )
    label_marks = (
        alt.Chart(labels)
        .mark_text(style="label", align="left", baseline="middle", dx=LABEL_GAP)
        .encode(x=alt.X("year:O", bandPosition=1), y="y:Q", text="label:N")
    )
    return _layer(bars, label_marks, _so_far_note(desktop, "downloads"))


def plugin_status(df: pd.DataFrame, *, share: bool = False) -> alt.LayerChart:
    """All plugins released so far, stacked by how recently each last released.

    ``df`` is ``nps.data.plugin_status()``. The stack's top is the total, so
    growth and upkeep read off one chart; ``share=True`` draws each state as a
    share of all plugins instead. Bands are labelled at their right end.
    """
    from nps.data import PLUGIN_STATES

    states = list(PLUGIN_STATES.values())
    y_field, y_title, fmt = (
        ("share", "share of all plugins", "%") if share else ("plugins", "plugins", "~s")
    )
    areas = (
        alt.Chart(df)
        .transform_calculate(stack_order=f"indexof({states}, datum.state)")
        .mark_area()
        .encode(
            x=alt.X("month:T", axis=YEAR_TICKS),
            y=alt.Y(f"{y_field}:Q", title=y_title, stack="zero", axis=alt.Axis(format=fmt)),
            # ordinal: the theme colours the last state (dormant) as context
            color=alt.Color("state:O", sort=states, scale=alt.Scale(domain=states), legend=None),
            order=alt.Order("stack_order:Q"),
            tooltip=[
                alt.Tooltip("yearmonth(month):T", title="Month"),
                alt.Tooltip("state:N", title="State"),
                alt.Tooltip("plugins:Q", title="Plugins"),
                alt.Tooltip("share:Q", title="Share of all", format=".0%"),
                alt.Tooltip("recent_share_of_living:Q", title="Recent / (recent + quiet)", format=".0%"),
            ],
        )
    )
    last = df[df["month"] == df["month"].max()].set_index("state").reindex(states)
    tops = last[y_field].cumsum()
    labels = pd.DataFrame(
        {
            "month": last.index.map(lambda _: df["month"].max()),
            "y": (tops - last[y_field] / 2).to_numpy(),
            "label": [f"{s} ({int(n)})" for s, n in zip(states, last["plugins"])],
        }
    )
    label_marks = (
        alt.Chart(labels)
        .mark_text(style="label", align="left", baseline="middle", dx=LABEL_GAP)
        .encode(x="month:T", y="y:Q", text="label:N")
    )
    return _layer(areas, label_marks)


def render(
    chart: alt.TopLevelMixin,
    mode: _theme.Mode,
    *,
    slides: bool = True,
    fmt: Literal["svg", "png"] = "svg",
    scale: float = 2.0,
) -> str | bytes:
    """Render ``chart`` under one napari theme to SVG text or PNG bytes."""
    import vl_convert as vlc

    _theme.register_fonts()
    name = f"napari-{mode}" + ("-slides" if slides else "")
    with alt.theme.enable(name):
        spec = chart.to_dict()
    if fmt == "png":
        return vlc.vegalite_to_png(spec, scale=scale)
    return vlc.vegalite_to_svg(spec)


def save(
    chart: alt.TopLevelMixin,
    stem: str | Path,
    *,
    slides: bool = True,
    modes: Sequence[_theme.Mode] = ("dark", "light"),
    formats: Iterable[Literal["svg", "png"]] = ("svg",),
) -> list[Path]:
    """Write ``chart`` once per theme as ``<stem>-<mode>.<fmt>``; return the paths.

    The same mechanism napari-talks uses for light/dark slides: emit both files
    and let CSS show the one matching the deck's theme.
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = []
    for mode in modes:
        for fmt in formats:
            out = stem.with_name(f"{stem.name}-{mode}.{fmt}")
            content = render(chart, mode, slides=slides, fmt=fmt)
            if isinstance(content, bytes):
                out.write_bytes(content)
            else:
                out.write_text(content, encoding="utf-8")
            paths.append(out)
    return paths
