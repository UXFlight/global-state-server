import json
from pathlib import Path

json_path = Path(__file__).parent / "DownLinks.json"
with open(json_path, "r", encoding="utf-8") as f:
    downlinks = json.load(f)
