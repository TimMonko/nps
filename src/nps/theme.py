"""Altair themes built from the repo's ``_brand.yml``.

Importing this module registers four Altair themes:

- ``napari-light`` and ``napari-dark``: for web pages
- ``napari-light-slides`` and ``napari-dark-slides``: larger text for 1280x720 slides

Enable one before drawing, e.g. ``alt.theme.enable("napari-dark")``, or use
``nps.theme.enable("dark", slides=True)``. The plots in ``nps.plots`` set no
colours or fonts of their own.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Literal

import altair as alt
import yaml

Mode = Literal["light", "dark"]

BRAND_FILE = Path(__file__).resolve().parents[2] / "_brand.yml"


@cache
def load_brand(path: Path | str = BRAND_FILE) -> dict:
    """Read ``_brand.yml``."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Palette:
    ground: str
    ink: str
    muted: str
    rule: str
    context: str
    series: tuple[str, ...]


def palette(mode: Mode, brand: dict | None = None) -> Palette:
    """The plot colours for ``mode``, taken from the brand's colour palette."""
    brand = brand or load_brand()
    named = brand["color"]["palette"]

    def get(token: str) -> str:
        return named[f"{token}-{mode}"]

    series = []
    while f"series-{len(series) + 1}-{mode}" in named:
        series.append(named[f"series-{len(series) + 1}-{mode}"])
    return Palette(
        ground=get("ground"),
        ink=get("ink"),
        muted=get("muted"),
        rule=get("rule"),
        context=get("context"),
        series=tuple(series),
    )


def font_family(brand: dict | None = None) -> str:
    brand = brand or load_brand()
    base = brand["typography"]["base"]
    family = base["family"] if isinstance(base, dict) else base
    return f"{family}, system-ui, sans-serif"


def theme_config(mode: Mode, *, slides: bool = False, brand: dict | None = None) -> dict:
    """The Vega-Lite config for one theme."""
    p = palette(mode, brand)
    font = font_family(brand)
    label, title = (18, 18) if slides else (13, 13)
    return {
        "config": {
            "background": p.ground,
            "font": font,
            "padding": 8,
            "view": {
                "stroke": None,
                "continuousWidth": 960 if slides else 640,
                "continuousHeight": 420 if slides else 320,
                "discreteWidth": 960 if slides else 640,
                "discreteHeight": 420 if slides else 320,
            },
            "axis": {
                "labelColor": p.muted,
                "titleColor": p.muted,
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": label,
                "titleFontSize": title,
                "titleFontWeight": "normal",
                "titlePadding": 10,
                "labelPadding": 6,
                "gridColor": p.rule,
                "domainColor": p.context,
                "tickColor": p.context,
                "ticks": False,
            },
            "axisX": {"grid": False, "labelAngle": 0, "labelOverlap": True},
            "axisY": {"domain": False, "labelFlush": False},
            "legend": {
                "labelColor": p.ink,
                "titleColor": p.muted,
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": label,
                "titleFontSize": title,
                "titleFontWeight": "normal",
                "orient": "top",
                "direction": "horizontal",
                "title": None,
                "symbolType": "square",
                "symbolStrokeWidth": 0,
                "labelLimit": 0,
            },
            "title": {
                "color": p.ink,
                "subtitleColor": p.muted,
                "font": font,
                "subtitleFont": font,
                "fontSize": label + 4,
                "subtitleFontSize": label,
                "fontWeight": 600,
                "anchor": "start",
                "offset": 12,
            },
            "header": {"labelColor": p.ink, "titleColor": p.muted, "labelFont": font},
            "range": {"category": list(p.series)},
            "mark": {"color": p.series[0]},
            "bar": {"color": p.series[0], "cornerRadiusEnd": 1},
            "area": {"color": p.series[0]},
            "line": {"color": p.series[0], "strokeWidth": 2.5 if slides else 2},
            "point": {"color": p.series[0], "filled": True, "size": 60 if slides else 40},
            "rule": {"color": p.context},
            "text": {"color": p.ink, "font": font, "fontSize": label},
        }
    }


THEMES: dict[str, tuple[Mode, bool]] = {
    "napari-light": ("light", False),
    "napari-dark": ("dark", False),
    "napari-light-slides": ("light", True),
    "napari-dark-slides": ("dark", True),
}


def register() -> None:
    """Register the four napari themes with Altair (does not enable one)."""
    for name, (mode, slides) in THEMES.items():

        def _theme(mode: Mode = mode, slides: bool = slides) -> alt.theme.ThemeConfig:
            return theme_config(mode, slides=slides)  # type: ignore[return-value]

        alt.theme.register(name, enable=False)(_theme)


def enable(mode: Mode = "light", *, slides: bool = False) -> str:
    """Enable a napari theme and return its name."""
    name = f"napari-{mode}" + ("-slides" if slides else "")
    alt.theme.enable(name)
    return name


register()
