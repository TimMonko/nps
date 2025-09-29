"""
analysis.py: Functions for analyzing napari plugin metadata.
"""
import pandas as pd

def summarize_plugin_status(classifiers_df):
    """Return counts of plugins by status (active/withdrawn/deleted)."""
    return classifiers_df['status'].value_counts()

def summarize_license_types(summary_df):
    """Return counts of plugins by license type."""
    return summary_df['license'].value_counts(dropna=False)

def find_stale_plugins(summary_df, days_stale=365):
    """Return plugins not updated in the last `days_stale` days."""
    import datetime
    now = pd.Timestamp.now()
    summary_df['last_release'] = pd.to_datetime(summary_df['last_release'], errors='coerce')
    stale = summary_df[summary_df['last_release'] < (now - pd.Timedelta(days=days_stale))]
    return stale
