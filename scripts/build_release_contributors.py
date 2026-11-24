"""Build the napari per-release new-contributors table.

Writes ``data/release_contributors.csv`` (used by the site) from three
inputs; ``--out <file>.md`` also writes the Markdown table and a CSV beside it
(how the frozen 2026-08-25 copy in ``fellowship/final-report/`` was made):

1. **Release notes author lists** — ``napari-docs/docs/release/release_*.md``.
   A contributor counts as *new* in release X if their GitHub handle appears in
   X's "N authors added to this release" list but in no earlier release's list.
2. **napari git history** — a local clone of napari (for tags and commit dates).
   The development window is the first->last commit *author* date in the range
   between the previous stable release tag and the release tag.
3. **GitHub release publish dates** — via the ``gh`` CLI (optional; falls back
   to tag dates if unavailable).

Usage::

    python scripts/build_release_contributors.py   # uses/updates .cache/napari, .cache/docs
    python scripts/build_release_contributors.py --napari ../napari \\
        --docs ../napari-docs --out fellowship/final-report/new-contributors-by-release.md
    python scripts/build_release_contributors.py --as-of 2026-08-24   # freeze dates

Requires:
- Clones of ``napari/napari`` (with tags) and ``napari/docs``. By default the
  script keeps blobless clones in ``.cache/`` (gitignored) and fetches them on
  every run, so it works on any machine and in CI. ``--napari``/``--docs``
  use existing clones as they are, without fetching.
- ``gh`` CLI authenticated (optional; without it, release dates use tag dates).

Methodology notes / gotchas baked into the logic:

- **Author dates, not committer dates.** 0.4.18 and 0.4.19 were released from
  cherry-picked branches (``v0.4.18x`` and Czaki's cherry-picks), which rewrote
  committer dates to Jun–Jul 2023. The dev window therefore uses author dates
  (when the work was actually done); the cherry-pick story is documented in the
  Notes section of the output.
- **Previous tag is selected by commit date, not version order.** ``v0.1.9`` is
  an out-of-order tag (its commit is dated 2021 after an early history
  rewrite); picking the previous tag by version order would corrupt the window.
- **Monotonic validation.** If the computed first->last commit range is not
  monotonic (history-rewrite artifact), the window falls back to the two tag
  dates.
- **In-development release.** A docs release with no stable tag yet (e.g. 0.9.0)
  is treated as in development: its window runs from the last stable tag to the
  latest ``origin/main`` commit, and its release date reads "in development".
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# ── helpers ───────────────────────────────────────────────────────────────

def git(naperi: Path, args: list[str]) -> str:
    return subprocess.run(
        ["git", "--no-pager", *args],
        cwd=naperi, capture_output=True, text=True,
    ).stdout


def git_one(naperi: Path, fmt: str, rev: str) -> str:
    return git(naperi, ["log", "-1", f"--format={fmt}", rev]).strip()


def tag_date(naperi: Path, tag: str) -> str | None:
    out = git_one(naperi, "%ai", tag)
    return out[:10] if out else None


def head_date(naperi: Path) -> str:
    for ref in ("origin/main", "main", "HEAD"):
        out = git_one(naperi, "%ai", ref)
        if out:
            return out[:10]
    return date.today().isoformat()


def git_range_author_dates(naperi: Path, prev: str, tag: str) -> list[str]:
    """Author dates (ISO) of commits in prev..tag, oldest first."""
    out = git(naperi, ["log", "--reverse", "--format=%ai", f"{prev}..{tag}"])
    return [ln.strip()[:10] for ln in out.splitlines() if ln.strip()]


CACHE = REPO_ROOT / ".cache"
CLONES = {
    "napari": "https://github.com/napari/napari.git",
    "docs": "https://github.com/napari/docs.git",
}


def cached_clone(name: str) -> Path:
    """A blobless clone of napari/<name> in .cache/, fetched to the latest main and tags."""
    path = CACHE / name
    if not (path / ".git").exists():
        CACHE.mkdir(exist_ok=True)
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--quiet", CLONES[name], str(path)], check=True
        )
    subprocess.run(["git", "-C", str(path), "fetch", "--quiet", "--tags", "--force", "origin"], check=True)
    subprocess.run(["git", "-C", str(path), "checkout", "--quiet", "--detach", "origin/HEAD"], check=True)
    return path


def fetch_gh_release_dates() -> dict[str, str]:
    """tag -> published date (YYYY-MM-DD) for stable napari releases."""
    try:
        out = subprocess.run(
            ["gh", "api", "repos/napari/napari/releases?per_page=100", "--paginate", "--slurp"],
            capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
        data = [r for page in json.loads(out.stdout) for r in page]
    except Exception:
        print("  Warning: could not fetch GitHub release dates via gh; "
              "using tag dates instead.", flush=True)
        return {}
    return {
        r["tag_name"]: r["published_at"][:10]
        for r in data
        if not r.get("prerelease") and not r.get("draft")
    }


def months_between(a: str, b: str) -> float:
    return round((date.fromisoformat(b) - date.fromisoformat(a)).days / 30.44, 1)


def sort_key(path: Path):
    m = re.match(r"release_0_(\d+)_(\d+)", path.name)
    return (int(m.group(1)), int(m.group(2))) if m else (999, 999)


def authors_handles(text: str) -> set[str] | None:
    m = re.search(
        r"##\s*\d+\s+authors added to this release.*?(?=\n## |\Z)", text, re.S | re.I
    )
    if not m:
        return None
    return set(re.findall(r"@([A-Za-z0-9][A-Za-z0-9_-]*)", m.group(0)))


# ── main ──────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--napari", type=Path, default=None, help="existing napari clone (default: .cache/napari)")
    ap.add_argument("--docs", type=Path, default=None, help="existing napari/docs clone (default: .cache/docs)")
    ap.add_argument("--csv", type=Path, default=REPO_ROOT / "data" / "release_contributors.csv")
    ap.add_argument("--out", type=Path, default=None, help="also write this Markdown table (+ .csv beside it)")
    ap.add_argument("--as-of", type=str, default=date.today().isoformat(),
                    help="Freeze the 'as of' / refresh date (YYYY-MM-DD). Default: today.")
    args = ap.parse_args()

    napari_dir = args.napari.resolve() if args.napari else cached_clone("napari")
    docs_dir = args.docs.resolve() if args.docs else cached_clone("docs")
    as_of = args.as_of

    # 1. stable tags (vX.Y.Z only), sorted by version
    tags = git(napari_dir, ["tag"]).splitlines()
    stable_tags = sorted(
        (t for t in tags if re.fullmatch(r"v\d+\.\d+\.\d+", t)),
        key=lambda t: tuple(int(x) for x in t[1:].split(".")),
    )
    td = {t: tag_date(napari_dir, t) for t in stable_tags}

    def prev_tag_by_date(tag: str) -> str | None:
        tdate = td.get(tag)
        if not tdate:
            return None
        cand = [(d, t) for t, d in td.items() if d and d < tdate]
        return max(cand)[1] if cand else None

    def dev_window(tag: str, prev: str | None, prev_date: str | None, this_date: str | None):
        if prev is None or not prev_date or not this_date:
            return this_date, this_date
        dates = git_range_author_dates(napari_dir, prev, tag)
        first = dates[0] if dates else None
        last = dates[-1] if dates else None
        ok = first and last and prev_date <= first <= last <= this_date
        if not ok:
            first, last = prev_date, this_date
        return first, last

    published = fetch_gh_release_dates()

    # 2. walk release notes, newest-first accumulation for first-appearance
    seen: set[str] = set()
    rows = []
    for p in sorted((docs_dir / "docs" / "release").glob("release_*.md"), key=sort_key):
        m = re.match(r"release_0_(\d+)_(\d+)", p.name)
        ver = f"0.{m.group(1)}.{m.group(2)}"
        tag = f"v{ver}"
        text = p.read_text(encoding="utf-8", errors="replace")

        handles = authors_handles(text)
        if handles is None:
            n_new = n_all = None
        else:
            n_all = len(handles)
            n_new = len(handles - seen)
            seen |= handles

        tdate = td.get(tag)
        in_dev = tag not in stable_tags
        if in_dev:
            # e.g. 0.9.0: last stable tag -> latest commit on the default branch
            prev = stable_tags[-1]
            first = td.get(prev)
            last = head_date(napari_dir)
            dev_days = (date.fromisoformat(last) - date.fromisoformat(first)).days if first and last else 0
            dev_months = months_between(first, last) if first and last else None
        elif tag in stable_tags:
            prev = prev_tag_by_date(tag)
            first, last = dev_window(tag, prev, td.get(prev), tdate)
            dev_days = (date.fromisoformat(last) - date.fromisoformat(first)).days if first and last else 0
            dev_months = months_between(first, last) if first and last else None
        else:
            first = last = tdate
            dev_days = 0
            dev_months = None

        # new contributors per month during the author-date dev window
        if n_new is None or not first or not last or dev_days <= 0:
            rate = None
        else:
            rate = round(n_new / (dev_days / 30.44), 1)

        release_date = published.get(tag) or tdate or ""
        if in_dev:
            release_date = f"in development (as of {as_of})"

        gap = None
        if not in_dev:
            prev_tag = prev_tag_by_date(tag)
            prev_pub = published.get(prev_tag) or td.get(prev_tag) if prev_tag else None
            if prev_pub and re.fullmatch(r"\d{4}-\d{2}-\d{2}", release_date):
                gap = months_between(prev_pub, release_date)

        rows.append({
            "ver": ver, "release_date": release_date, "n_new": n_new, "n_all": n_all,
            "first": first, "last": last, "dev_months": dev_months,
            "gap": gap, "rate": rate,
        })

    # 3. render markdown
    L = []
    L.append("# napari new contributors by release\n")
    L.append(
        "New contributors per napari release, computed from each release's "
        "`N authors added to this release` list in the napari docs "
        "(`napari-docs/docs/release/release_*.md`): a contributor is counted as "
        "new in release X if their GitHub handle appears in X's author list but in "
        "no earlier release's list.\n"
    )
    L.append(
        "**Dev window** is the first and last commit *author* dates in the git "
        "range between the previous stable release tag and the release tag. Author "
        "dates reflect when the work was actually done (committer dates are "
        "unreliable here because some releases were cut from cherry-picked "
        "branches — see Notes). **Months between releases** is the calendar gap "
        "between consecutive release dates and is unaffected by history "
        "rewriting. **New / month** is `new contributors ÷ dev window`, i.e. the "
        "average inflow of first-time contributors per month during the release's "
        "development. **Release date** is the GitHub release publish date where "
        "available, otherwise the tag commit date.\n"
    )
    L.append(
        "| Release | Release date | New contributors | Dev window (first -> last commit) | Dev months | Months between releases | New / month |"
    )
    L.append("|---|---|---|---|---|---|---|")
    for r in rows:
        nc = "—" if r["n_new"] is None else (f"**{r['n_new']}**" if r["n_new"] >= 16 else str(r["n_new"]))
        rel = f"**{r['ver']}**" if (r["n_new"] or 0) >= 16 else f"`{r['ver']}`"
        dev = f"{r['first']} -> {r['last']}" if r["first"] and r["last"] else "—"
        devm = f"~{r['dev_months']} mo" if r["dev_months"] is not None else "—"
        gap = f"~{r['gap']} mo" if r["gap"] is not None else "—"
        rate = "—" if r["rate"] is None else f"~{r['rate']}"
        L.append(f"| {rel} | {r['release_date']} | {nc} | {dev} | {devm} | {gap} | {rate} |")

    L.append("\n---\n## Notes\n")
    L.append(
        "- Releases with **16+ new contributors** are bolded; those are the "
        "all-time high-water marks (0.4.17, 0.4.18, and 0.9.0).\n"
    )
    L.append(
        "- **New / month** is `new contributors ÷ dev window`. Very short "
        "patch-release windows (e.g. 0.3.3, ~1–2 days) produce large per-month "
        "rates, so treat those as outliers; the longer release cycles are the "
        "meaningful comparisons.\n"
    )
    L.append(
        "- **0.4.18 and 0.4.19 were released from cherry-picked branches**, not the "
        "normal main-line flow. 0.4.18 was cut by Juan Nunez-Iglesias on July 5, "
        "2023 from the `v0.4.18x` branch (forked and cherry-picked in June 2023), "
        "gathering ~8 months of accumulated main-line work (authored Oct 2022 – "
        "May 2023) — which is why v0.4.17's range to v0.4.18 spans ~8 months by "
        "author date despite all commits being committed in Jun–Jul 2023. 0.4.19 "
        "was released by Grzegorz Bokota (Czaki) on Feb 1, 2024, also via "
        "cherry-picking; v0.4.18 is *not* an ancestor of v0.4.19. The **Dev "
        "window** column therefore uses author dates.\n"
    )
    L.append(
        "- 0.1.0 predates the `authors added` convention being fully populated, "
        "so its count reflects all authors listed (all new at first release).\n"
    )
    L.append(
        "- 0.3.4's release notes do not contain an author list, so its count is "
        "not available.\n"
    )
    L.append(
        "- For 0.4.18 and 0.4.19 the release notes themselves state \"19 new "
        "contributors\" and \"5 new contributors\" respectively; the "
        "handle-matching method used here gives 18 and 4. The one-person "
        "difference is a handle-matching artifact (a contributor listed under a "
        "slightly different handle in an earlier release).\n"
    )
    L.append(
        "- Data source: `napari-docs` release notes; development windows computed "
        f"from the local napari git history (author dates); refresh date {as_of}.\n"
    )

    # reproduction section (kept in the output so it always matches the script)
    L.append("\n---\n## Reproducing this table\n")
    L.append(
        "Regenerate this file with:\n\n"
        "```sh\n"
        "python scripts/build_release_contributors.py\n"
        "```\n\n"
        "Inputs: a local `napari/napari` clone with tags fetched (default "
        "`../napari`), a local `napari/napari-docs` clone (default `../napari-docs`), "
        "and the `gh` CLI for official release dates (optional). Use `--napari`, "
        "`--docs`, `--out`, and `--as-of` to override paths or freeze the date. "
        "See the script's module docstring for the full methodology.\n"
    )

    csv_paths = [args.csv]
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("\n".join(L), encoding="utf-8")
        print(f"Wrote {args.out} ({len(rows)} releases)")
        csv_paths.append(args.out.with_suffix(".csv"))
    for csv_path in csv_paths:
        _write_csv(csv_path, rows)
    return 0


def _write_csv(csv_path: Path, rows: list[dict]) -> None:
    """Write the machine-readable table."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "release", "release_date", "new_contributors", "contributors",
            "dev_window_first", "dev_window_last", "dev_months",
            "months_between_releases", "new_per_month",
        ])
        for r in rows:
            def clean(v):
                return "" if v is None else v
            writer.writerow([
                r["ver"], clean(r["release_date"]), clean(r["n_new"]), clean(r["n_all"]),
                clean(r["first"]), clean(r["last"]), clean(r["dev_months"]),
                clean(r["gap"]), clean(r["rate"]),
            ])
    print(f"Wrote {csv_path} ({len(rows)} releases)")


if __name__ == "__main__":
    raise SystemExit(main())
