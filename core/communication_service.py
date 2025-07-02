import requests
from typing import Optional, Any
from core.constants import atc_server_url, pilot_server_url


class CommunicationService:
    def __init__(self):
        self.atc_base_url = atc_server_url
        self.pilot_base_url = pilot_server_url

    def send_post(self, path: str, payload: Optional[Any] = None) -> None:
        url = f"{self.atc_base_url}{path}"
        try:
            response = requests.post(url, json=payload or {})
            response.raise_for_status()
            print(f"[COMM] ✅ POST {url} - {response.status_code}")
        except Exception as e:
            print(f"[COMM] ❌ Error POST {url} - {e}")

    def send_pilot_list(self, pilot_list: list) -> None:
        self.send_post("/pilot-list", payload=pilot_list)

    def send_new_pilot(self, pilot_data: dict) -> None:
        self.send_post("/new-pilot", payload=pilot_data)

    def send_pilot_disconnected(self, pilot_sid: str) -> None:
        self.send_post(f"/pilot-disconnected/{pilot_sid}")

    def send_step_update(self, step_data: Any) -> None:
        self.send_post("/step-updated", payload=step_data)

        
communication_service = CommunicationService()