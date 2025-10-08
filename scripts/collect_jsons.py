# Collect JSON files from Github https://github.com/napari/npe2api/

import requests
import json
import pathlib

# Direct download from GitHub repository
URL = "https://raw.githubusercontent.com/napari/npe2api/main/public/"
FILES = ["extended_summary.json"]

output_dir = pathlib.Path(__file__).parent.parent / "public"
output_dir.mkdir(parents=True, exist_ok=True)

for file in FILES:
    response = requests.get(URL + file)
    data = response.json()

    # Save to local file
    output_path = output_dir / file

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {file} to {output_path}")
    print("Sample data:", json.dumps(data[:1], indent=2))