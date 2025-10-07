import json
import pandas as pd
import re
import pathlib

data_dir = pathlib.Path(__file__).parent.parent / "public"
data_path = data_dir / "extended_summary.json"

output_dir = pathlib.Path(__file__).parent.parent / "data"
output_dir.mkdir(exist_ok=True)

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)  # data is a list of dicts

df = pd.DataFrame(data)

def get_github_url(row):
    gh_pattern = r'https://github\.com/([^/]+)/([^/#@\s,]+)'
    candidates = row.get('project_url') or []
    # Add home_page as a candidate
    home = row.get('home_page')
    if home:
        candidates = list(candidates) + [home]
    for entry in candidates:
        if isinstance(entry, str) and 'github.com' in entry:
            match = re.search(gh_pattern, entry)
            if match:
                owner, repo = match.groups()
                clean_repo = repo.rstrip('.git').rstrip('/')
                return f'https://github.com/{owner}/{clean_repo}'
    return None

df['github_url'] = df.apply(get_github_url, axis=1)

# save to github_repos.csv
output_path = output_dir / "github_repos.csv"
# get just the name and github_url columns
df = df[['name', 'github_url']]

df.to_csv(output_path, index=False)

# find the number of plugins without a github_url
no_github = df['github_url'].isnull()
print(f"Number of plugins without a GitHub URL: {no_github.sum()} out of {len(df)}")

# # print plugins without a github_url
# print(df[no_github]['name'])