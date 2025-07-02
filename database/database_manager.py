from typing import Optional
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        base = Path(__file__).parent
        self.downlinks = self._load_json(base / "DownLinks.json")
        self.uplinks = self._load_json(base / "UpLinks.json")
        self.codes = self._index_codes()

    def _load_json(self, path: Path) -> list:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _index_codes(self):
        result = {}
        for msg in self.downlinks + self.uplinks:
            code = msg.get("Ref_Num")
            if code:
                result[code] = msg
        return result

    def get_step_info(self, code: str) -> Optional[dict]:
        return self.codes.get(code)