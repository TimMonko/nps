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


def active_contributors(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Contributors with a commit in the trailing six months, per month.

    Columns: ``month`` (Timestamp), ``group`` ("all contributors" or "also
    plugin developers": those who have also contributed to a napari plugin's
    repo), ``contributors`` (int). Commits to public napari org repos.
    """
    everyone = pd.read_csv(_path("metrics/active_contributors.csv", data_dir))
    plugin_devs = pd.read_csv(_path("metrics/active_plugin_devs.csv", data_dir))
    wide = everyone.merge(plugin_devs, on="month", how="left").fillna(0)
    wide["month"] = pd.to_datetime(wide["month"].str[:10])
    long = wide.melt(
        id_vars="month",
        value_vars=["active_contributors", "active_plugin_devs"],
        var_name="group",
        value_name="contributors",
    )
    long["group"] = long["group"].map(
        {"active_contributors": "all contributors", "active_plugin_devs": "also plugin developers"}
    )
    return long.astype({"contributors": int})


# napari's release policy with a monthly cadence (napari/docs#1126) merged on this date
MONTHLY_CADENCE = "2026-09-22"
QUICK_PATCH_DAYS = 14  # releases this soon after the previous one are quick patches


def release_contributors(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Contributors to each napari release, from the release notes' author lists.

    One row per release, oldest first. Columns: ``release`` (str), ``start``
    and ``end`` (Timestamp: the previous release's date and this release's;
    for the release in development, ``end`` is the "as of" date), ``months``
    (float, ``end - start``), ``contributors`` (int, everyone in the author
    list), ``new`` (int, in no earlier release's list), ``returning`` (int),
    ``in_development`` (bool), ``per_month`` (float, contributors / months),
    ``quick_patch`` (bool, released under ``QUICK_PATCH_DAYS`` days after the
    previous one). Releases with no author list are dropped.
    """
    df = pd.read_csv(_path("release_contributors.csv", data_dir), dtype={"release": str})
    as_of = df["release_date"].str.extract(r"as of (\d{4}-\d{2}-\d{2})")[0]
    df["in_development"] = as_of.notna()
    df["end"] = pd.to_datetime(as_of.fillna(df["release_date"]))
    df = df.sort_values("end").reset_index(drop=True)
    df["start"] = df["end"].shift().fillna(pd.to_datetime(df["dev_window_first"]))
    df = df.dropna(subset=["contributors", "new_contributors"])
    out = pd.DataFrame(
        {
            "release": df["release"],
            "start": df["start"],
            "end": df["end"],
            "months": ((df["end"] - df["start"]).dt.days / 30.44).round(1),
            "contributors": df["contributors"].astype(int),
            "new": df["new_contributors"].astype(int),
            "in_development": df["in_development"],
        }
    )
    out["returning"] = out["contributors"] - out["new"]
    out["per_month"] = (out["contributors"] / out["months"]).round(1)
    out["quick_patch"] = (out["end"] - out["start"]).dt.days < QUICK_PATCH_DAYS
    return out.reset_index(drop=True)


# Repos whose git history starts with another project's: commits before the
# date are that project's (napari-sphinx-theme began as a copy of
# pydata-sphinx-theme on 2022-01-20), so they are not napari contributions.
COPIED_HISTORY = {"napari/napari-sphinx-theme": "2022-01-20"}


def drop_copied_history(commits: pd.DataFrame) -> pd.DataFrame:
    """Drop commits a repo inherited from the project it was copied from."""
    dates = pd.to_datetime(commits["date"], utc=True)
    keep = pd.Series(True, index=commits.index)
    for repo, since in COPIED_HISTORY.items():
        keep &= ~((commits["repo"] == repo) & (dates < pd.Timestamp(since, tz="UTC")))
    return commits[keep]


def _commits(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Every commit to a public napari org repo: ``login``, ``date``, ``repo``."""
    import json

    frames = []
    for path in sorted(Path(data_dir or DATA_DIR).glob("commits_*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if rows:
            frame = pd.DataFrame(rows)
            frame["repo"] = path.stem.removeprefix("commits_").replace("_", "/", 1)
            frames.append(frame)
    if not frames:
        raise FileNotFoundError("no data/commits_*.json; run the pipeline (pixi run pipeline)")
    commits = pd.concat(frames, ignore_index=True).dropna(subset=["login"])
    commits = drop_copied_history(commits.drop_duplicates(subset="sha"))
    commits["login"] = commits["login"].str.lower().str.strip()
    commits["date"] = pd.to_datetime(commits["date"], utc=True).dt.tz_localize(None)
    return commits[["login", "date", "repo"]].sort_values("date").reset_index(drop=True)


FIRST_REPOS = {
    "napari/napari": "napari",
    "napari/docs": "docs",
}


def newcomer_first_repo(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Where newcomers make their first commit, per year.

    Columns: ``year`` (int), ``repo`` ("napari", "docs" or "other repos"),
    ``contributors`` (int), ``ytd`` (bool). Each person counts once, in the
    year and repo of their first commit to any public napari org repo.
    """
    commits = _commits(data_dir)
    first = commits.groupby("login").first()
    first["year"] = first["date"].dt.year
    first["repo"] = first["repo"].map(FIRST_REPOS).fillna("other repos")
    out = first.groupby(["year", "repo"]).size().rename("contributors").reset_index()
    out["ytd"] = out["year"] == commits["date"].max().year
    return out


RETURN_GAP_DAYS = 14  # a later commit at least this long after the first counts as coming back
RETURN_WINDOWS = {"within 3 months": 91, "within a year": 365}


def newcomer_retention(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Share of each year's newcomers who came back, per window.

    A newcomer *came back* if they committed again to any public napari org
    repo between ``RETURN_GAP_DAYS`` days and the window after their first
    commit (the gap keeps one pull request's commits from counting). Only
    people whose whole window has passed are counted, so the latest year
    holds only its earlier newcomers.

    Columns: ``year`` (int), ``window`` (key of ``RETURN_WINDOWS``),
    ``newcomers`` (int, counted for this window), ``returned`` (int),
    ``share`` (float), ``partial`` (bool: the year's later newcomers are
    still inside the window).
    """
    commits = _commits(data_dir)
    as_of = commits["date"].max()
    first = commits.groupby("login")["date"].min().rename("first")
    later = commits.join(first, on="login")
    later["days"] = (later["date"] - later["first"]).dt.days
    rows = []
    for window, days in RETURN_WINDOWS.items():
        came_back = set(later.loc[later["days"].between(RETURN_GAP_DAYS, days), "login"])
        people = first[first <= as_of - pd.Timedelta(days=days)].to_frame()
        people["year"] = people["first"].dt.year
        people["returned"] = people.index.isin(came_back)
        for year, group in people.groupby("year"):
            all_that_year = (first.dt.year == year).sum()
            rows.append(
                {
                    "year": int(year),
                    "window": window,
                    "newcomers": len(group),
                    "returned": int(group["returned"].sum()),
                    "share": group["returned"].mean(),
                    "partial": len(group) < all_that_year,
                }
            )
    return pd.DataFrame(rows)


PYTHONS = [f"3.{minor}" for minor in range(8, 15)]


def python_support(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Which Python versions plugins say they support, per plugin group.

    Reads the ``Programming Language :: Python :: 3.x`` classifiers of each
    plugin's latest release; plugins without them are left out. Groups:
    "released in the last 2 years" and "older", by the latest release.
    Columns: ``python`` (str), ``group`` (str), ``plugins`` (int, listing
    that version), ``share`` (float, of the group's plugins with classifiers).
    """
    versions = pd.read_csv(_path("python_versions.csv", data_dir)).dropna(subset=["supported_versions"])
    releases = pd.read_csv(_path("plugin_releases.csv", data_dir), usecols=["name", "latest_release"])
    df = versions.merge(releases, on="name", how="left")
    latest = pd.to_datetime(df["latest_release"], utc=True).dt.tz_localize(None)
    cutoff = latest.max() - pd.DateOffset(years=2)
    df["group"] = (latest >= cutoff).map({True: "released in the last 2 years", False: "older"})
    listed = df["supported_versions"].str.split(",")
    rows = []
    for group in ["released in the last 2 years", "older"]:
        in_group = listed[df["group"] == group]
        for python in PYTHONS:
            n = int(in_group.map(lambda vs: python in vs).sum())
            rows.append({"python": python, "group": group, "plugins": n, "share": n / len(in_group)})
    return pd.DataFrame(rows)


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


SYSTEMS = {"Windows": "Windows", "Darwin": "macOS", "Linux": "Linux", "": "unknown"}


def pypi_downloads_by_system(
    project: str = "napari", data_dir: Path | str | None = None
) -> pd.DataFrame:
    """Monthly PyPI downloads of ``project`` by the installer's operating system.

    Columns: ``month`` (Timestamp), ``system`` ("Windows", "macOS", "Linux",
    "unknown"), ``downloads`` (int). CI and cloud machines are nearly all
    Linux (napari's 2022 and late-2024 spikes are Linux only), so Windows +
    macOS is the cleaner signal of people installing napari themselves.
    """
    df = pd.read_csv(
        _path("pypi_downloads_by_system_monthly.csv", data_dir),
        parse_dates=["month"],
        keep_default_na=False,
    )
    df = df[df["project"] == project]
    if df.empty:
        raise ValueError(f"no downloads for {project!r}; add it to fetch_pypi_downloads.py")
    df = df.assign(system=df["system"].map(SYSTEMS).fillna("unknown"))
    out = df.groupby(["month", "system"], as_index=False)["downloads"].sum()
    return out.astype({"downloads": int})


PLUGIN_STATES = {
    "recent": "released in the last 6 months",
    "quiet": "last release 6 to 24 months ago",
    "dormant": "no release in 2 years",
}


def plugin_status(
    data_dir: Path | str | None = None, *, start: str = "2020-01-01"
) -> pd.DataFrame:
    """Every plugin released so far, by how recently it last released, per month.

    Built from every version's upload time (``plugin_versions.csv``). At the
    end of each month each plugin released so far counts once: "recent" (a
    release in the last 6 months), "quiet" (last release 6 to 24 months ago)
    or "dormant" (nothing in 2 years), so the three add up to all plugins.

    Columns: ``month`` (Timestamp), ``state`` (a ``PLUGIN_STATES`` value),
    ``plugins`` (int), ``share`` (of all plugins that month), and
    ``recent_share_of_living`` (recent / (recent + quiet), the same on every
    row of a month).
    """
    versions = pd.read_csv(_path("plugin_versions.csv", data_dir))
    uploads = pd.DataFrame(
        {
            "name": versions["name"],
            "t": pd.to_datetime(versions["upload_time"], utc=True).dt.tz_localize(None),
        }
    ).dropna()
    rows = []
    for month in pd.date_range(start, pd.Timestamp.today(), freq="MS"):
        end = month + pd.offsets.MonthBegin(1)
        last = uploads[uploads["t"] < end].groupby("name")["t"].max()
        recent = int((last >= end - pd.DateOffset(months=6)).sum())
        living = int((last >= end - pd.DateOffset(months=24)).sum())
        counts = {"recent": recent, "quiet": living - recent, "dormant": len(last) - living}
        for key, n in counts.items():
            rows.append(
                {
                    "month": month,
                    "state": PLUGIN_STATES[key],
                    "plugins": n,
                    "share": n / len(last) if len(last) else 0.0,
                    "recent_share_of_living": recent / living if living else 0.0,
                }
            )
    return pd.DataFrame(rows)


TEMPLATE_KINDS = {
    "new_template": "used the template",
    "new_not_template": "no template",
    "new_unknown": "no public repo",
}


def template_usage_by_year(data_dir: Path | str | None = None) -> pd.DataFrame:
    """New plugins per year, split by napari-plugin-template usage.

    Columns: ``year`` (int), ``kind`` ("used the template", "no template",
    "no public repo"), ``plugins`` (int), ``ytd`` (bool). "used the template"
    covers both the cookiecutter and copier eras; "no public repo" is plugins
    whose metadata links no GitHub repo, or whose repo is gone or private
    (``scripts/detect_plugin_template_usage.py``; plugins released after the
    last scan also land here until ``pixi run refresh``).
    """
    monthly = pd.read_csv(_path("metrics/new_plugins_template_monthly.csv", data_dir))
    monthly["year"] = pd.to_datetime(monthly["month"]).dt.year
    yearly = monthly.groupby("year", as_index=False)[list(TEMPLATE_KINDS)].sum()
    long = yearly.melt(id_vars="year", var_name="kind", value_name="plugins")
    long["kind"] = long["kind"].map(TEMPLATE_KINDS)
    long["plugins"] = long["plugins"].astype(int)
    long["ytd"] = long["year"] == date.today().year
    return long.sort_values(["year", "kind"]).reset_index(drop=True)
