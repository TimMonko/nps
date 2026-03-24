"""Check what github_repos.csv contains vs extended_summary.json."""
import json
from pathlib import Path

import pandas as pd

# extended_summary count
summary_path = Path("public/extended_summary.json")
with open(summary_path, encoding="utf-8") as f:
    summary = json.load(f)
print(f"extended_summary.json: {len(summary)} plugins")

# github_repos.csv count
csv_path = Path("data/github_repos.csv")
df = pd.read_csv(csv_path)
print(f"github_repos.csv: {len(df)} rows")
print(f"  with github_url: {df['github_url'].notna().sum()}")
print(f"  without github_url: {df['github_url'].isna().sum()}")

# What's in extended_summary but not in github_repos?
summary_names = {p.get("normalized_name", "") for p in summary if p.get("normalized_name")}
csv_names = set(df["name"].str.lower())
missing = summary_names - csv_names
print(f"\nIn extended_summary but not in github_repos.csv: {len(missing)}")
if missing:
    print("  Sample:", sorted(missing)[:15])

# What about the reverse?
extra_in_csv = csv_names - summary_names
print(f"\nIn github_repos.csv but not in extended_summary: {len(extra_in_csv)}")

# Show some plugins without github_urls
no_url = df[df["github_url"].isna()]
print(f"\nSample plugins WITHOUT github_url ({len(no_url)} total):")
print(no_url["name"].head(10).to_string(index=False))

# Show a sample of pypi_versions lengths
n_versions = [len(p.get("pypi_versions", [])) for p in summary]
print(f"\nPyPI versions stats: min={min(n_versions)}, max={max(n_versions)}, median={sorted(n_versions)[len(n_versions)//2]}")
