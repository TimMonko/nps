# Example usage of the new library in a notebook cell
import sys
sys.path.append('../src')  # Adjust path as needed for your setup

from napari_plugin_analysis.io import load_classifiers, load_extended_summary
from napari_plugin_analysis.analysis import summarize_plugin_status, summarize_license_types, find_stale_plugins

# Example: Load data
classifiers_df = load_classifiers('../npe2api/public/classifiers.json')
extended_summary_df = load_extended_summary('../npe2api/public/extended_summary.json')

# Example: Analyze
status_counts = summarize_plugin_status(classifiers_df)
license_counts = summarize_license_types(extended_summary_df)
stale_plugins = find_stale_plugins(extended_summary_df)

print(status_counts)
print(license_counts)
print(stale_plugins[['name', 'last_release']])
