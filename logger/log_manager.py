from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from typing import Optional

class GSSLogManager:
    def __init__(self, base_logs_dir: Optional[Path] = None):
        self.base_logs_dir = base_logs_dir or Path.cwd() / "logs"
        self.base_logs_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_path(self, subdir: str, identifier: str) -> Path:
        log_dir = self.base_logs_dir / subdir / f"{identifier}-log"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir / "gss_events.log"

    def _timestamp(self) -> str:
        now = datetime.now(ZoneInfo('America/Toronto'))
        return now.strftime('%H:%M:%S')

    def _write(self, path: Path, event: str, data: dict):
        line = f"[{self._timestamp()}] [{event.upper():<12}] {json.dumps(data, ensure_ascii=False)}\n"
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)

    def log_pilot_event(self, pilot_sid: str, event: str, data: dict):
        path = self._get_log_path("pilot-logs", pilot_sid)
        self._write(path, event, data)

    def log_atc_event(self, event: str, data: dict):
        path = self._get_log_path("atc-logs", "atc")
        self._write(path, event, data)

log_manager = GSSLogManager()