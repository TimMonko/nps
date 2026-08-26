Tim Monko’s URSSI Early Career Fellowship Award supported improvements to napari’s plugin ecosystem and community development through a sustainability initiative. The work was founded to solve the problem that as napari--a multidimensional interactive scientific image viewer--and its extensible plugin ecosystem grew, so too did unsustainable practices and the communities drifted apart. I hypothesized that building a more sustainable plugin ecosystem would mutually benefit both the core napari project and its broad community of plugin developers and users. To accomplish this, I focused on:

1. Building community with shared approaches to review and sustainability, modeled after other scientific software communities and  
2. Building tools and features by finishing agreed upon goals and creating mutually beneficial architecture for the community.

I started this work by organizing community outreach with a survey and organized (continuing) regular community meetings focused on plugin sustainability. We identified a strong interest in community involvement in this work, which has remained true throughout the course of the fellowship. The community has participated via review and discussion as I did the work to modernize plugin development tooling (napari, npe2, napari-plugin-template) and has collaborated as I have worked to improve discoverability and ecosystem-wide communication (napari-hub, documentation, working group). 

During this time, I have upskilled in the napari plugin architecture and have made long-needed improvements asked for by the community. I am now the key organizer and maintainer in the community, leading a group of folks interested in the long-term sustainability of the project.

URSSI funds supported:

1. Introduction to napari Pilot workshops, March 25 and April 1, 2026\. Virtual 4hr workshops  
2. SciPy, July 13 \-- 18, 2026 in Minneapolis, MN USA  
   1. Invited talk about the Plugin Sustainability Initiative  
   2. napari Tools Plenary including plugin updates  
   3. napari workshop including how to build and use plugins  
3. EuroSciPy, July 19 \-- 23, 2026 in Krakow, PL  
   1. Sprints with community work on plugin architecture  
   2. Invited talk about the Plugin Sustainability Initiative  
   3. Co-led napari workshop including how to build plugins  
4. napari Hackathon, July 24 \-- 29, 2026 in Krakow, PL  
   1. Work with community to implement long-requested plugin functionality and architecture for community support

These conferences received strong community interest and showed engagement with the future of the sustainability initiative, including the beginning of direct collaborations with broader ecosystems including the PyOpenSci review system and the Scientific Python Development Guide Repo-Review. Overall, the plugin initiative has found multiple new, enthusiastic and frequent contributors with skillsets and experience that previously did not exist. In addition to the revitalization, excitement, and trust within and between the plugin community and napari core, I have quantitatively observed sustainable growth to the core napari project, its architecture, and mutual trust that is sustainable without my contribution.

## Presentations, workshops, and outreach

Full bibliographic details for the talks and events related to this project are provided below, in the style of a references list or CV.

### Invited talks

- Monko, T. (2026, July 17). *(Re)-connecting foundational libraries with their communities: Successes, failures, and surprises in building the napari plugin sustainability initiative* [Invited talk]. SciPy 2026, Minneapolis, MN, USA.
- Monko, T. (2026, July 20). *(Re)-connecting foundational libraries with their communities: Successes, failures, and surprises in building the napari plugin sustainability initiative* [Invited talk]. EuroSciPy 2026, Kraków, Poland.

### Plenary

- Monko, T. (2026, July 16). *napari Tools Plenary* (including plugin updates) [Plenary]. SciPy 2026, Minneapolis, MN, USA.

### Workshops and tutorials

- Monko, T. (2026, July 13). *Create custom image visualization and analysis tools with napari* [Workshop, 4 hours, ~30 participants]. SciPy 2026, Minneapolis, MN, USA.
- Monko, T. (2026, July 22). *napari: explorative visualization and workflow building for scientific data analysis* [Tutorial, 90 minutes]. EuroSciPy 2026, Kraków, Poland.
- Monko, T. (2026, March 25 and April 1). *Introduction to napari — pilot* [Virtual workshop, two 4-hour sessions, 20 seats each]. Online.

### Sprints and hackathons

- Monko, T. (2026, July 18–19). *EuroSciPy Sprints 2026* [Sprint mentor]. EuroSciPy 2026, Kraków, Poland.
- Monko, T. (2026, July 24–29). *naPLari Hackathon* [Organizer]. Kraków, Poland.

### Publications

- Monko, T. (2026, February). *Building the napari Plugin Sustainability Initiative.* The Island Dispatch (napari community blog). <https://napari.org/island-dispatch/blog/plugin-sustainability-initiative.html>

## Software artifacts and releases

The following software artifacts and releases came out of this work. Because napari is a community project, several are the collective product of the napari community, but all are direct outputs of, or closely related to, the plugin sustainability initiative. Links point to the official releases.

### Core plugin engine and viewer

- **npe2 v0.8.0** (February 6, 2026) — <https://github.com/napari/npe2/releases/tag/v0.8.0>. First release of the fellowship period: added Python 3.14 support, raised the minimum to Python 3.10, and expanded the reader documentation.
- **npe2 v0.9.0** (August 18, 2026) — <https://github.com/napari/npe2/releases/tag/v0.9.0>. Added the ready-to-consume `ConfigurationContribution` declaration to the plugin manifest, allowing plugins to define persistent, user-configurable settings (first consumed by napari 0.9.0); added writer selection by compound file extensions (e.g., `.ome.tiff`); dropped Python 3.10.
- **napari v0.7.0** (March 23, 2026) — <https://github.com/napari/napari/releases/tag/v0.7.0>. Completed the transition to the npe2 plugin engine by removing the npe1 auto-conversion setting, a change requested by the community to simplify and unify plugin infrastructure.
- **napari v0.8.0** (July 14, 2026) — <https://github.com/napari/napari/releases/tag/v0.8.0>. Dropped Python 3.10 and deprecated PyQt5, reducing the support matrix plugin developers must target; also added a built-in histogram for Image layers.
- **napari v0.9.0** (in development, release candidates) — the first napari release to consume npe2's configuration contribution.

### Plugin development infrastructure

- **napari-plugin-template v2.0.0** (October 28, 2025) — <https://github.com/napari/napari-plugin-template/releases/tag/v2.0.0>. Modernized the template: moved tests to the package root, added `uv`/`tox-uv` support, and modernized CI.
- **napari-plugin-template v2.1.0** (February 27, 2026) — <https://github.com/napari/napari-plugin-template/releases/tag/v2.1.0>. PEP 639 license expression, simplified to a ruff-only pre-commit, tokenless (OIDC) codecov, and removal of unneeded files.
- **napari-plugin-template v2.2.0** (July 2, 2026) — <https://github.com/napari/napari-plugin-template/releases/tag/v2.2.0>. Cleaner post-render output; no longer modifies the user's global git config.
- **napari-plugin-template v2.3.0** (July 12, 2026) — <https://github.com/napari/napari-plugin-template/releases/tag/v2.3.0>. Aligned with napari 0.8.0; dropped Python 3.10; switched from `pre-commit` to `prek`.
- **npe2 theme contribution** — plugins can now contribute themes to napari (npe2 pull requests [#464](https://github.com/napari/npe2/pull/464), [#465](https://github.com/napari/npe2/pull/465)), with corresponding documentation in the plugin-building guides ([napari/docs #1027](https://github.com/napari/docs/pull/1027)).

### Ecosystem tooling and discoverability

- **hub-lite** (<https://napari.org/hub-lite>) — a lightweight, community-managed re-implementation of the napari hub, built on data from npe2api; its development is aligned with the working group's discoverability goals.
- **npe2api** (<https://github.com/napari/npe2api>) — the plugin metadata API; automated compatibility checks against new napari releases are in active development to surface plugin breakage before users encounter it.
- **napari/docs plugin guides** — reorganization of the plugin-building documentation, including a beginner "your first plugin" pathway, guidance for plugin themes, and guidance on message routing (see pull requests [#1027](https://github.com/napari/docs/pull/1027), [#998](https://github.com/napari/docs/pull/998)).
- **napari/workshops** — the "Extending napari" workshop materials include a full plugin-building lesson ([`docs/extend/04_plugin.md`](https://github.com/napari/workshops)).
- **napari/surveys** — a new repository for analyzing napari survey data, created in October 2025 (<https://github.com/napari/surveys>).

### Community artifacts

- **Plugin Sustainability Working Group** — a weekly, globally-scheduled working group with public notes at <https://hackmd.io/@napari/plugin-wg>, recruited through a public call on Zulip and GitHub in October 2025.
- **The Island Dispatch blog post** (February 2026) — announced the initiative and its three priority efforts to the broader community: <https://napari.org/island-dispatch/blog/plugin-sustainability-initiative.html>.

## Quantitative outcomes

I tracked ecosystem health metrics continuously through the fellowship using a public metrics pipeline (the *napari plugin sustainability* repository, <https://github.com/TimMonko/nps>), which combines GitHub and npe2api data. Unless noted, figures compare the start of the fellowship (October 2025) with the most recent data (August 2026).

- **Plugin maintenance more than doubled.** The share of plugins on the napari hub that received an update in the previous year rose from **14.3% (October 2025)** to **32.8% (August 2026)**. The number of actively maintained plugins grew from **77 to 214**, while the total plugin count grew from **540 to 653**.
- **Core contributor activity grew sharply.** Monthly active contributors to the napari GitHub organization rose from **32 (October 2025)** to **64 (August 2026)** — a **doubling**. Monthly active plugin developers rose from **20 (September 2025)** to **33 (August 2026)**, a **65% increase**.
- **New contributor acquisition accelerated.** July 2026 — the month of the SciPy and EuroSciPy sprints — brought **23 new contributors** to the napari organization, the largest single-month influx in the dataset (the previous peak was 13, in April 2021). In 2026 so far, **42 of 69 contributors were new**, up from 26 new contributors across all of 2025.
- **The 0.9.0 release cycle is bringing in contributors at a record pace.** The napari 0.9.0 release notes (in development) already list **16 first-time contributors** — more than any release since 0.4.18 (July 2023).
- **Cumulative contributors reached 290** by August 6, 2026, growing steadily throughout the fellowship.
- **The ecosystem kept growing.** New plugins were added at an average of **~12 per month** during 2026, bringing the hub to **653 plugins** by August 2026.

These figures are visualized in the `plots/` directory of the `nps` repository (e.g., `plugin_maintenance.png`, `active_contributors.png`, `new_contributors_over_time.png`).

> **Note on scope.** "23 new contributors in July 2026" counts people whose *first-ever commit* to the napari GitHub organization (across all tracked organization repos) fell in that calendar month. "16 first-time contributors" counts first-time *napari* authors in the 0.9.0 release cycle (from the v0.8.0 release on July 14, 2026), per the release notes. The two reconcile exactly: 15 of the 23 also appear in the 0.9.0 notes; of the remaining 8, five joined via napari/napari in the final days of the 0.8.0 cycle (July 6–11) and three via other organization repos (two in hub-lite, one in napari-plugin-manager). Conversely, one of the 0.9.0 notes' 16 made their first commit in August 2026, outside the July window.

I will continue to shepherd the architecture, tooling, and development of the napari plugin ecosystem and community.