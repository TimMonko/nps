"""
io.py: Functions for loading and parsing napari plugin metadata files.
"""
import json
import pandas as pd
from pathlib import Path

def load_json(path):
    """Load a JSON file and return its contents."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_json_as_dataframe(path):
    """Load a JSON file as a DataFrame."""
    data = load_json(path)
    return pd.DataFrame(data)
