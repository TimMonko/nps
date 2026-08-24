# napari new contributors by release

New contributors per napari release, computed from each release's `N authors added to this release` list in the napari docs (`napari-docs/docs/release/release_*.md`): a contributor is counted as new in release X if their GitHub handle appears in X's author list but in no earlier release's list.

**Dev window** is the first and last commit *author* dates in the git range between the previous stable release tag and the release tag. Author dates reflect when the work was actually done (committer dates are unreliable here because some releases were cut from cherry-picked branches — see Notes). **Months between releases** is the calendar gap between consecutive release dates and is unaffected by history rewriting. **New / month** is `new contributors ÷ dev window`, i.e. the average inflow of first-time contributors per month during the release's development. **Release date** is the GitHub release publish date where available, otherwise the tag commit date.

| Release | Release date | New contributors | Dev window (first → last commit) | Dev months | Months between releases | New / month |
|---|---|---|---|---|---|---|
| `0.1.0` | 2019-07-10 | 12 | 2019-06-18 → 2019-07-10 | ~0.7 mo | ~0.9 mo | ~16.6 |
| `0.1.3` | 2019-07-22 | 2 | 2019-07-20 → 2019-07-22 | ~0.1 mo | ~0.1 mo | ~30.4 |
| `0.1.5` | 2019-09-05 | 1 | 2019-08-15 → 2019-09-05 | ~0.7 mo | ~0.8 mo | ~1.4 |
| `0.2.0` | 2019-10-01 | 2 | 2019-09-11 → 2019-10-01 | ~0.7 mo | ~0.9 mo | ~3.0 |
| `0.2.1` | 2019-10-16 | 0 | 2019-10-05 → 2019-10-16 | ~0.4 mo | ~0.5 mo | ~0.0 |
| `0.2.3` | 2019-10-26 | 3 | 2019-10-17 → 2019-10-26 | ~0.3 mo | ~0.3 mo | ~10.1 |
| `0.2.4` | 2019-10-30 | 1 | 2019-10-27 → 2019-10-30 | ~0.1 mo | ~0.1 mo | ~10.1 |
| `0.2.5` | 2019-11-08 | 0 | 2019-10-31 → 2019-11-08 | ~0.3 mo | ~0.3 mo | ~0.0 |
| `0.2.6` | 2019-11-28 | 3 | 2019-11-09 → 2019-11-27 | ~0.6 mo | ~0.7 mo | ~5.1 |
| `0.2.7` | 2019-12-19 | 3 | 2019-11-27 → 2019-12-18 | ~0.7 mo | ~0.7 mo | ~4.3 |
| `0.2.8` | 2019-12-23 | 2 | 2019-12-20 → 2019-12-23 | ~0.1 mo | ~0.1 mo | ~20.3 |
| `0.2.9` | 2020-01-10 | 0 | 2019-12-25 → 2020-01-09 | ~0.5 mo | ~0.6 mo | ~0.0 |
| `0.2.10` | 2020-01-13 | 0 | 2020-01-10 → 2020-01-12 | ~0.1 mo | ~0.1 mo | ~0.0 |
| `0.2.11` | 2020-01-31 | 1 | 2020-01-13 → 2020-01-30 | ~0.6 mo | ~0.6 mo | ~1.8 |
| `0.2.12` | 2020-02-27 | 2 | 2020-01-31 → 2020-02-26 | ~0.9 mo | ~0.9 mo | ~2.3 |
| `0.3.0` | 2020-05-05 | 4 | 2020-03-02 → 2020-05-04 | ~2.1 mo | ~2.2 mo | ~1.9 |
| `0.3.1` | 2020-05-13 | 1 | 2020-05-06 → 2020-05-12 | ~0.2 mo | ~0.3 mo | ~5.1 |
| `0.3.2` | 2020-05-28 | 3 | 2020-05-14 → 2020-05-27 | ~0.4 mo | ~0.5 mo | ~7.0 |
| `0.3.3` | 2020-05-31 | 1 | 2020-05-29 → 2020-05-30 | ~0.0 mo | ~0.1 mo | ~30.4 |
| `0.3.4` | 2020-06-03 | — | 2020-05-31 → 2020-06-02 | ~0.1 mo | ~0.1 mo | — |
| `0.3.5` | 2020-06-18 | 0 | 2020-06-03 → 2020-06-18 | ~0.5 mo | ~0.5 mo | ~0.0 |
| `0.3.6` | 2020-07-19 | 2 | 2020-06-20 → 2020-07-18 | ~0.9 mo | ~1.0 mo | ~2.2 |
| `0.3.7` | 2020-09-03 | 2 | 2020-07-20 → 2020-09-03 | ~1.5 mo | ~1.5 mo | ~1.4 |
| `0.3.8` | 2020-09-24 | 1 | 2020-09-03 → 2020-09-24 | ~0.7 mo | ~0.7 mo | ~1.4 |
| `0.4.0` | 2020-10-29 | 9 | 2020-09-25 → 2020-10-28 | ~1.1 mo | ~1.1 mo | ~8.3 |
| `0.4.1` | 2020-11-25 | 8 | 2020-10-28 → 2020-11-25 | ~0.9 mo | ~0.9 mo | ~8.7 |
| `0.4.2` | 2020-11-29 | 1 | 2020-11-25 → 2020-11-28 | ~0.1 mo | ~0.1 mo | ~10.1 |
| `0.4.3` | 2021-01-14 | 0 | 2021-01-07 → 2021-01-14 | ~0.2 mo | ~0.3 mo | ~0.0 |
| `0.4.4` | 2021-01-28 | 3 | 2021-01-16 → 2021-01-26 | ~0.3 mo | ~0.5 mo | ~9.1 |
| `0.4.5` | 2021-02-12 | 3 | 2021-01-27 → 2021-02-10 | ~0.5 mo | ~0.5 mo | ~6.5 |
| `0.4.6` | 2021-03-02 | 2 | 2021-02-12 → 2021-03-01 | ~0.6 mo | ~0.6 mo | ~3.6 |
| `0.4.7` | 2021-03-25 | 1 | 2021-03-02 → 2021-03-24 | ~0.7 mo | ~0.8 mo | ~1.4 |
| `0.4.8` | 2021-05-18 | 5 | 2021-03-26 → 2021-05-18 | ~1.7 mo | ~1.8 mo | ~2.9 |
| `0.4.9` | 2021-06-11 | 1 | 2021-05-18 → 2021-06-10 | ~0.8 mo | ~0.8 mo | ~1.3 |
| `0.4.10` | 2021-06-17 | 0 | 2021-06-12 → 2021-06-16 | ~0.1 mo | ~0.2 mo | ~0.0 |
| `0.4.11` | 2021-09-03 | 5 | 2021-06-17 → 2021-09-02 | ~2.5 mo | ~2.6 mo | ~2.0 |
| `0.4.12` | 2021-10-21 | 6 | 2021-09-05 → 2021-10-21 | ~1.5 mo | ~1.6 mo | ~4.0 |
| `0.4.13` | 2022-01-17 | 7 | 2021-10-24 → 2022-01-17 | ~2.8 mo | ~2.9 mo | ~2.5 |
| `0.4.14` | 2022-02-04 | 0 | 2022-01-18 → 2022-02-04 | ~0.6 mo | ~0.6 mo | ~0.0 |
| `0.4.15` | 2022-03-10 | 1 | 2022-02-04 → 2022-03-10 | ~1.1 mo | ~1.1 mo | ~0.9 |
| `0.4.16` | 2022-05-31 | 11 | 2022-03-10 → 2022-05-31 | ~2.7 mo | ~2.7 mo | ~4.1 |
| **0.4.17** | 2022-11-09 | **19** | 2022-05-31 → 2022-11-01 | ~5.1 mo | ~5.3 mo | ~3.8 |
| **0.4.18** | 2023-07-05 | **18** | 2022-11-01 → 2023-07-05 | ~8.1 mo | ~7.8 mo | ~2.2 |
| `0.4.19` | 2024-02-01 | 4 | 2023-08-18 → 2024-02-01 | ~5.5 mo | ~6.9 mo | ~0.7 |
| `0.5.0` | 2024-07-11 | 13 | 2024-02-01 → 2024-07-10 | ~5.3 mo | ~5.3 mo | ~2.5 |
| `0.5.1` | 2024-07-25 | 1 | 2024-07-16 → 2024-07-25 | ~0.3 mo | ~0.5 mo | ~3.4 |
| `0.5.2` | 2024-08-13 | 1 | 2024-07-30 → 2024-08-12 | ~0.4 mo | ~0.6 mo | ~2.3 |
| `0.5.3` | 2024-08-30 | 1 | 2024-08-14 → 2024-08-30 | ~0.5 mo | ~0.6 mo | ~1.9 |
| `0.5.4` | 2024-09-30 | 2 | 2024-08-31 → 2024-09-30 | ~1.0 mo | ~1.0 mo | ~2.0 |
| `0.5.5` | 2024-12-12 | 2 | 2024-10-01 → 2024-12-11 | ~2.3 mo | ~2.4 mo | ~0.9 |
| `0.5.6` | 2025-01-22 | 3 | 2024-12-16 → 2025-01-22 | ~1.2 mo | ~1.3 mo | ~2.5 |
| `0.6.0` | 2025-05-01 | 4 | 2025-01-26 → 2025-04-30 | ~3.1 mo | ~3.3 mo | ~1.3 |
| `0.6.1` | 2025-05-19 | 0 | 2025-05-04 → 2025-05-18 | ~0.5 mo | ~0.6 mo | ~0.0 |
| `0.6.2` | 2025-07-01 | 3 | 2025-05-20 → 2025-06-30 | ~1.3 mo | ~1.4 mo | ~2.2 |
| `0.6.3` | 2025-07-31 | 4 | 2025-07-03 → 2025-07-31 | ~0.9 mo | ~1.0 mo | ~4.3 |
| `0.6.4` | 2025-08-15 | 0 | 2025-08-06 → 2025-08-15 | ~0.3 mo | ~0.5 mo | ~0.0 |
| `0.6.5` | 2025-10-02 | 0 | 2025-08-16 → 2025-10-01 | ~1.5 mo | ~1.6 mo | ~0.0 |
| `0.6.6` | 2025-10-16 | 0 | 2025-10-02 → 2025-10-16 | ~0.5 mo | ~0.5 mo | ~0.0 |
| `0.7.0` | 2026-03-23 | 11 | 2025-10-16 → 2026-03-21 | ~5.1 mo | ~5.2 mo | ~2.1 |
| `0.7.1` | 2026-06-15 | 10 | 2026-03-24 → 2026-06-12 | ~2.6 mo | ~2.8 mo | ~3.8 |
| `0.8.0` | 2026-07-14 | 8 | 2026-06-16 → 2026-07-12 | ~0.9 mo | ~1.0 mo | ~9.4 |
| **0.9.0** | in development (as of 2026-08-25) | **16** | 2026-07-12 → 2026-08-24 | ~1.4 mo | — | ~11.3 |

---
## Notes

- Releases with **16+ new contributors** are bolded; those are the all-time high-water marks (0.4.17, 0.4.18, and 0.9.0).

- **New / month** is `new contributors ÷ dev window`. Very short patch-release windows (e.g. 0.3.3, ~1–2 days) produce large per-month rates, so treat those as outliers; the longer release cycles are the meaningful comparisons.

- **0.4.18 and 0.4.19 were released from cherry-picked branches**, not the normal main-line flow. 0.4.18 was cut by Juan Nunez-Iglesias on July 5, 2023 from the `v0.4.18x` branch (forked and cherry-picked in June 2023), gathering ~8 months of accumulated main-line work (authored Oct 2022 – May 2023) — which is why v0.4.17's range to v0.4.18 spans ~8 months by author date despite all commits being committed in Jun–Jul 2023. 0.4.19 was released by Grzegorz Bokota (Czaki) on Feb 1, 2024, also via cherry-picking; v0.4.18 is *not* an ancestor of v0.4.19. The **Dev window** column therefore uses author dates.

- 0.1.0 predates the `authors added` convention being fully populated, so its count reflects all authors listed (all new at first release).

- 0.3.4's release notes do not contain an author list, so its count is not available.

- For 0.4.18 and 0.4.19 the release notes themselves state "19 new contributors" and "5 new contributors" respectively; the handle-matching method used here gives 18 and 4. The one-person difference is a handle-matching artifact (a contributor listed under a slightly different handle in an earlier release).

- Data source: `napari-docs` release notes; development windows computed from the local napari git history (author dates); refresh date 2026-08-25.


---
## Reproducing this table

Regenerate this file with:

```sh
python scripts/build_release_contributors.py
```

Inputs: a local `napari/napari` clone with tags fetched (default `../napari`), a local `napari/napari-docs` clone (default `../napari-docs`), and the `gh` CLI for official release dates (optional). Use `--napari`, `--docs`, `--out`, and `--as-of` to override paths or freeze the date. See the script's module docstring for the full methodology.
