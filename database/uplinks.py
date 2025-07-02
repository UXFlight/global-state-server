import json
from pathlib import Path

json_path = Path(__file__).parent / "UpLinks.json"
with open(json_path, "r", encoding="utf-8") as f:
    uplinks = json.load(f)
