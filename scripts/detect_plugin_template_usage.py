"""Detect which napari plugins were generated from the napari-plugin-template.

The napari-plugin-template historically used cookiecutter
(napari/cookiecutter-napari-plugin) and switched to copier on 2024-06-13
(commit 47fe643 "Use copier instead of cookiecutter").

Fingerprints detected per plugin repo (root level unless noted):

  * `.cookiecutter.json`               — cookiecutter template artifact
  * `.copier-answers.yml`              — copier template artifact
  * README text                        — "napari-plugin-template" / copier badge /
                                          "cookiecutter-napari-plugin" /
                                          napari-hub shields badge + codecov badge
  * `.napari-hub/DESCRIPTION.md`       — cookiecutter-era leftover
  * `.github/workflows/test_and_deploy.yml`  — template CI (supporting evidence)

Output: data/plugin_template_usage.csv
Columns: name, owner, repo, template_era, evidence, details

template_era:
  * copier        — generated from napari-plugin-template via copier (2024-06+)
  * cookiecutter  — generated via cookiecutter (pre-2024-06)
  * template      — evidence of napari-plugin-template but era ambiguous
  * no            — no evidence found
  * unavailable   — repo not reachable (deleted/private/no default branch)

Requires the `gh` CLI to be authenticated (uses `gh api` for repo trees and
raw.githubusercontent.com for file contents).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
GH_CSV = DATA_DIR / "github_repos.csv"
OUT_CSV = DATA_DIR / "plugin_template_usage.csv"

MAX_WORKERS = 8
REQUEST_SLEEP = 0.05  # small delay between gh api calls

# ── marker strings ────────────────────────────────────────────────────────
# README: the generation statement is required (avoid false positives from
# READMEs that merely LINK to the template, e.g. "Try the napari plugin template")
COOKIECUTTER_GEN_RE = re.compile(r"generated\s+with\s+\[?[Cc]ookiecutter\]?")
COPIER_GEN_RE = re.compile(r"generated\s+with\s+\[?[Cc]opier\]?")
# The napari template is referenced by these names in generated READMEs
NAPARI_TEMPLATE_NAMES = ("napari-plugin-template", "cookiecutter-napari-plugin")
# Badge block common to both eras: napari-hub shields endpoint + codecov badge
TEMPLATE_BADGE_MARKERS = (
    "api.napari-hub.org/shields/",
    "codecov.io/gh/",
)
# napari-template specific keys inside .cookiecutter.json
COOKIECUTTER_JSON_KEYS = (
    "plugin_name",
    "module_name",
    "include_reader_plugin",
    "github_username_or_organization",
)
# napari-template specific markers inside .copier-answers.yml
COPIER_ANSWERS_MARKERS = (
    "napari-plugin-template",
    "include_reader_plugin",
    "# Changes here will be overwritten by Copier; NEVER EDIT MANUALLY",
)
README_CANDIDATES = ("README.md", "README.rst", "readme.md", "Readme.md", "README.txt")
ANSWERS_CANDIDATES = (".copier-answers.yml", ".copier-answers.yaml")
COOKIECUTTER_FILE = ".cookiecutter.json"

# Eras that warrant a PyPI-description fallback check (no repo to inspect)
PYPI_CHECK_ERAS = {"no", "no_github", "unavailable", "error"}


def run_gh_api(args: list[str]) -> tuple[bool, str]:
    """Run `gh api <args...>` and return (ok, raw_stdout)."""
    result = subprocess.run(
        ["gh", "api", *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, result.stdout


def fetch_raw(url: str) -> tuple[bool, str]:
    """Fetch a raw.githubusercontent.com URL (not rate-limited)."""
    result = subprocess.run(
        ["curl", "-sS", "-L", "--max-time", "20", url],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        return False, result.stderr.strip()
    # curl returns empty body on 404 (content may be a "404: Not Found" page)
    if not result.stdout or "404: Not Found" in result.stdout[:200]:
        return False, "not found"
    return True, result.stdout


def fetch_blob_content(owner: str, repo: str, blob_sha: str) -> str | None:
    """Fetch blob raw content via git blobs API (fallback when raw fails)."""
    ok, out = run_gh_api([
        f"repos/{owner}/{repo}/git/blobs/{blob_sha}",
        "-H",
        "Accept: application/vnd.github.raw",
    ])
    return out if ok else None


def parse_github_url(url: str) -> tuple[str, str] | None:
    if not isinstance(url, str) or "github.com" not in url:
        return None
    parts = url.rstrip("/").split("github.com/")[-1].split("/")
    if len(parts) >= 2:
        owner = parts[0]
        repo = parts[1]
        # NOTE: do NOT use rstrip('.git') — it strips any trailing characters
        # in the set {., g, i, t}, corrupting repo names that end in those
        # letters (e.g. 'napari-chat-assistant' -> 'assistan').
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo
    return None


def classify_repo(owner: str, repo: str) -> dict:
    """Detect template usage for a single repo."""
    full = f"{owner}/{repo}"
    result = {
        "owner": owner,
        "repo": repo,
        "template_era": "unavailable",
        "evidence": "",
        "details": "",
    }

    ok, tree_out = run_gh_api([f"repos/{full}/git/trees/HEAD?recursive=1"])
    if not ok:
        result["details"] = f"tree api failed: {tree_out[:120]}"
        return result
    try:
        tree = json.loads(tree_out)
    except json.JSONDecodeError:
        result["details"] = "unparseable tree"
        return result

    paths: list[str] = [t.get("path", "") for t in tree.get("tree", [])]
    path_set = set(paths)
    # map path -> blob sha for content fallback
    blob_sha = {t.get("path"): t.get("sha") for t in tree.get("tree", []) if t.get("type") == "blob"}

    readme_path = next((p for p in README_CANDIDATES if p in path_set), None)
    answers_path = next((p for p in ANSWERS_CANDIDATES if p in path_set), None)
    has_cookiecutter = COOKIECUTTER_FILE in path_set
    has_napari_hub = ".napari-hub/DESCRIPTION.md" in path_set
    has_tpl_ci = ".github/workflows/test_and_deploy.yml" in path_set

    # Determine a branch for raw fetches (try main, then master)
    def raw_url(branch: str, path: str) -> str:
        return f"https://raw.githubusercontent.com/{full}/{branch}/{path}"

    def fetch_text(path: str) -> str | None:
        for branch in ("main", "master"):
            ok, body = fetch_raw(raw_url(branch, path))
            if ok:
                return body
        # fallback to blob API using tree sha
        sha = blob_sha.get(path)
        if sha:
            return fetch_blob_content(owner, repo, sha)
        return None

    evidence: list[str] = []
    era: str | None = None

    # 1) .cookiecutter.json content (cookiecutter era)
    if has_cookiecutter:
        content = fetch_text(COOKIECUTTER_FILE)
        if content:
            try:
                cfg = json.loads(content)
            except json.JSONDecodeError:
                cfg = {}
            napari_keys = [k for k in COOKIECUTTER_JSON_KEYS if k in cfg]
            if napari_keys:
                evidence.append(".cookiecutter.json (napari keys)")
                era = "cookiecutter"
            else:
                evidence.append(".cookiecutter.json (non-napari)")
        else:
            evidence.append(".cookiecutter.json (unreadable)")

    # 2) .copier-answers.yml content (copier era)
    if answers_path:
        content = fetch_text(answers_path)
        if content:
            hits = [m for m in COPIER_ANSWERS_MARKERS if m.lower() in content.lower()]
            if hits:
                evidence.append(".copier-answers.yml")
                if "napari-plugin-template" in content.lower():
                    era = "copier"
                elif era is None:
                    era = "copier"  # copier answers w/ napari keys is napari template
            else:
                evidence.append(".copier-answers.yml (non-napari)")
        else:
            evidence.append(".copier-answers.yml (unreadable)")

    # 3) README content
    if readme_path:
        readme = fetch_text(readme_path)
        if readme:
            lower = readme.lower()
            cc_gen = bool(COOKIECUTTER_GEN_RE.search(lower))
            cop_gen = bool(COPIER_GEN_RE.search(lower))
            has_name = any(n.lower() in lower for n in NAPARI_TEMPLATE_NAMES)
            badge_hits = [m for m in TEMPLATE_BADGE_MARKERS if m in lower]
            if cop_gen and has_name:
                evidence.append("README: generated with copier via napari-plugin-template")
                if era is None:
                    era = "copier"
            elif cc_gen and has_name:
                evidence.append("README: generated with cookiecutter via cookiecutter-napari-plugin")
                if era is None:
                    era = "cookiecutter"
            elif len(badge_hits) >= 2:
                # napari-hub shields + codecov badges only appear in this template
                evidence.append("README template badge block")
                if era is None:
                    era = "template"
        else:
            evidence.append("README (unreadable)")

    # 4) Weak supporting signals if nothing definitive yet
    if era is None and has_napari_hub and has_tpl_ci:
        evidence.append(".napari-hub/ + test_and_deploy.yml")
        era = "template"

    if era is None:
        era = "no"
        # note napari-hub/CI presence for manual review but don't call it template
        if has_napari_hub or has_tpl_ci:
            result["details"] = "supporting files present but no definitive marker"

    result["template_era"] = era
    result["evidence"] = "; ".join(evidence) if evidence else ("none" if era == "no" else "")
    if not result["details"]:
        result["details"] = "; ".join(evidence)
    return result


def check_pypi_description(name: str) -> tuple[str, str] | None:
    """Check a plugin's PyPI long description for template markers.

    Falls back on this when the repo can't be inspected (no GitHub URL,
    deleted/private repo, or no marker found in the repo).  Returns
    (template_era, evidence) or None.
    """
    import requests  # noqa: PLC0415

    url = f"https://pypi.org/pypi/{name}/json"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            return None
        desc = resp.json().get("info", {}).get("description") or ""
    except Exception:
        return None

    lower = desc.lower()
    has_name = any(n.lower() in lower for n in NAPARI_TEMPLATE_NAMES)
    if COPIER_GEN_RE.search(lower) and has_name:
        return "copier", "pypi description: generated with copier via napari-plugin-template"
    if COOKIECUTTER_GEN_RE.search(lower) and has_name:
        return "cookiecutter", "pypi description: generated with cookiecutter via cookiecutter-napari-plugin"
    badge_hits = [m for m in TEMPLATE_BADGE_MARKERS if m in lower]
    if len(badge_hits) >= 2:
        return "template", "pypi description: template badge block"
    # classic template README *reference-style* link footer, e.g.
    #   [napari-plugin-template]: https://github.com/napari/napari-plugin-template
    # (a plain inline mention/link, e.g. "Try the napari plugin template",
    # does NOT match — avoids false positives)
    footer_re = re.compile(
        r"\[\s*(?:napari-plugin-template|cookiecutter-napari-plugin)\s*\]:\s*\[?\s*https?://",
        re.I,
    )
    if footer_re.search(lower):
        return "template", "pypi description: template README footer"
    return None


def main() -> int:
    df = pd.read_csv(GH_CSV)
    rows = []
    for _, row in df.iterrows():
        name = row["name"]
        url = row.get("github_url")
        parsed = parse_github_url(url) if url else None
        if parsed is None:
            rows.append(
                {
                    "name": name,
                    "owner": "",
                    "repo": "",
                    "template_era": "no_github",
                    "evidence": "",
                    "details": "no github url",
                }
            )
            continue
        owner, repo = parsed
        rows.append({"name": name, "owner": owner, "repo": repo})

    results: list[dict] = []
    total = len([r for r in rows if r.get("repo")])
    done = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {}
        for r in rows:
            if not r.get("repo"):
                results.append(r)
                continue
            f = ex.submit(classify_repo, r["owner"], r["repo"])
            futures[f] = r["name"]
        for f in as_completed(futures):
            done += 1
            name = futures[f]
            try:
                info = f.result()
            except Exception as exc:  # noqa: BLE001
                info = {
                    "owner": "",
                    "repo": "",
                    "template_era": "error",
                    "evidence": "",
                    "details": str(exc)[:200],
                }
            info = {"name": name, **info}
            results.append(info)
            if done % 50 == 0 or done == total:
                print(f"  [{done}/{total}] processed", file=sys.stderr, flush=True)
            time.sleep(REQUEST_SLEEP)

    out = pd.DataFrame(results)
    out = out.sort_values("name").reset_index(drop=True)
    out["pypi_evidence"] = ""

    # PyPI-description fallback for plugins we could not confirm from a repo
    for idx in out.index[out["template_era"].isin(PYPI_CHECK_ERAS)]:
        name = out.at[idx, "name"]
        hit = check_pypi_description(name)
        if hit:
            era, evidence = hit
            out.at[idx, "template_era"] = era
            out.at[idx, "pypi_evidence"] = evidence
            out.at[idx, "evidence"] = (
                f"{out.at[idx, 'evidence']}; {evidence}".lstrip("; ").strip()
            )
        time.sleep(0.03)

    out.to_csv(OUT_CSV, index=False)
    print(f"\nSaved {len(out)} rows to {OUT_CSV}", file=sys.stderr)

    counts = out["template_era"].value_counts()
    print("\n=== Template era counts (repo + PyPI description) ===", file=sys.stderr)
    for k, v in counts.items():
        print(f"  {k:14s} {v}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
