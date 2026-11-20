"""Load nps's committed data as tidy DataFrames.

Everything here reads files under ``data/`` that the pipeline in ``scripts/``
writes (``pixi run pipeline``); nothing fetches. Each loader
takes an optional ``data_dir`` so tests and other repos can point elsewhere.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _path(name: str, data_dir: Path | str | None) -> Path:
    path = Path(data_dir or DATA_DIR) / name
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; run the pipeline (pixi run pipeline)"
        )
    return path


def contributors_by_year(data_dir: Path | str | None = None) -> pd.DataFrame:
    """New and returning contributors to public napari org repos, per year.

    Columns: ``year`` (int), ``kind`` ("New" or "Returning"), ``contributors``
    (int), ``ytd`` (bool, True for the current, partial year). A "new"
    contributor made their first commit to any public napari repo that year.
    """
    wide = pd.read_csv(_path("metrics/new_vs_returning.csv", data_dir))
    long = wide.melt(
        id_vars="year",
        value_vars=["new", "returning"],
        var_name="kind",
        value_name="contributors",
    )
    long["kind"] = long["kind"].map({"new": "New", "returning": "Returning"})
    long["ytd"] = long["year"] == date.today().year
    return long.sort_values(["year", "kind"]).reset_index(drop=True)


def new_plugins_by_year(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Plugins by the year of their first PyPI release.

    Columns: ``year`` (int), ``new_plugins`` (int), ``total_plugins``
    (cumulative, int), ``ytd`` (bool). Only plugins listed on npe2api today
    are counted, so plugins that were deleted from PyPI are missing.
    """
    releases = pd.read_csv(_path("plugin_releases.csv", data_dir))
    first = pd.to_datetime(releases["first_release"], utc=True).dropna()
    years = range(first.dt.year.min(), max(first.dt.year.max(), date.today().year) + 1)
    per_year = first.dt.year.value_counts().reindex(years, fill_value=0).sort_index()
    out = pd.DataFrame({"year": per_year.index, "new_plugins": per_year.to_numpy()})
    out["total_plugins"] = out["new_plugins"].cumsum()
    out["ytd"] = out["year"] == date.today().year
    return out


def plugin_maintenance(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Plugins released so far and plugins with a recent release, per month.

    Columns: ``month`` (Timestamp, first of the month), ``total_plugins``,
    ``active_plugins`` (at least one release of any version in the six months
    ending that month), ``maintenance_ratio`` (active / total).
    """
    df = pd.read_csv(_path("metrics/plugin_maintenance.csv", data_dir))
    df["month"] = pd.to_datetime(df["month"].str[:10])
    return df


def pypi_downloads(
    project: str = "napari", data_dir: Path | str | None = None
) -> pd.DataFrame:
    """Monthly PyPI downloads of ``project`` (complete months only).

    Columns: ``month`` (Timestamp), ``downloads`` (int). Source: ClickHouse's
    public PyPI dataset, which counts every download PyPI logs (mirrors and CI
    included), so it reads higher than BigQuery-based counts.
    """
    df = pd.read_csv(_path("pypi_downloads_monthly.csv", data_dir), parse_dates=["month"])
    df = df[df["project"] == project]
    if df.empty:
        raise ValueError(f"no downloads for {project!r}; add it to fetch_pypi_downloads.py")
    return df[["month", "downloads"]].reset_index(drop=True)


TEMPLATE_KINDS = {
    "new_template": "used the template",
    "new_not_template": "no template",
    "new_unknown": "not checked",
}


def template_usage_by_year(data_dir: Path | str | None = None) -> pd.DataFrame:
    """New plugins per year, split by napari-plugin-template usage.

    Columns: ``year`` (int), ``kind`` ("used the template", "no template",
    "not checked"), ``plugins`` (int), ``ytd`` (bool). "used the template"
    covers both the cookiecutter and copier eras; "not checked" is plugins
    without a GitHub repo or released after the last template scan
    (``scripts/detect_plugin_template_usage.py``).
    """
    monthly = pd.read_csv(_path("metrics/new_plugins_template_monthly.csv", data_dir))
    monthly["year"] = pd.to_datetime(monthly["month"]).dt.year
    yearly = monthly.groupby("year", as_index=False)[list(TEMPLATE_KINDS)].sum()
    long = yearly.melt(id_vars="year", var_name="kind", value_name="plugins")
    long["kind"] = long["kind"].map(TEMPLATE_KINDS)
    long["plugins"] = long["plugins"].astype(int)
    long["ytd"] = long["year"] == date.today().year
    return long.sort_values(["year", "kind"]).reset_index(drop=True)
