import re
import pandas as pd

def extract_github_repos(extended_summary_data):
    github_pattern = r'https://github\.com/([^/]+)/([^/#@\s,]+)'
    plugin_github_mapping = {}

    for plugin in extended_summary_data:
        plugin_name = plugin.get('name')
        github_url = None

        project_urls = plugin.get('project_urls', {})

        for url_entry in project_urls:
            if isinstance(url_entry, str) and 'github.com':
                match = re.search(github_pattern, url_entry)
                if match:
                    owner, repo = match.groups()
                    clean_repo = repo.rstrip('.git').rstrip('/')
                    github_url = f'https://github.com/{owner}/{clean_repo}'
                    break

        if not github_url and plugin.get('home_page'):
            home_page = plugin['home_page']
            if 'github.com' in home_page:
                match = re.search(github_pattern, home_page)
                if match:
                    owner, repo = match.groups()
                    clean_repo = repo.rstrip('.git').rstrip('/')
                    github_url = f'https://github.com/{owner}/{clean_repo}'

        if github_url:
            plugin_github_mapping[plugin_name] = github_url

    return plugin_github_mapping

def main():
    url = 'https://raw.githubusercontent.com/npe2/npe2api/main/npe2api/extended_summary.json'
    print(f"Fetching data from {url}")
    extended_summary_data = pd.read_json(url).to_dict(orient='records')
    plugin_github_mapping = extract_github_repos(extended_summary_data)
    print(plugin_github_mapping)

    df = pd.DataFrame(list(plugin_github_mapping.items()), columns=['plugin_name', 'github_url'])
    df.to_csv('github_repos.csv', index=False)