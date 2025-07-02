from typing import Dict, Optional
from custom_types.public_view import PilotPublicView
from logger.log_manager import log_manager
from pilot.pilot import Pilot

class PilotManager:
    def __init__(self):
        self.pilots: Dict[str, Pilot] = {}  # sid -> Pilot

    def create_pilot(self, sid: str) -> PilotPublicView:
        if sid in self.pilots:
            raise ValueError(f"Pilot with SID '{sid}' already exists.")
        pilot = Pilot(sid)
        self.pilots[sid] = pilot

        log_manager.log_pilot_event(
            sid,
            "new_pilot",
            {"message": f"Pilot {sid} registered by backend."}
        )
        return pilot.to_public_view()

    def get_pilot(self, sid: str) -> Optional[Pilot]:
        return self.pilots.get(sid)


    def remove_pilot(self, sid: str) -> None:
        if sid in self.pilots:
            del self.pilots[sid]
            log_manager.log_pilot_event(
                sid,
                "pilot_disconnected",
                {"message": f"Pilot {sid} disconnected."}
            )

    def get_all_pilots(self) -> list[Pilot]:
        return list(self.pilots.values())

    def has_any_pilot(self) -> bool:
        return len(self.pilots) > 0