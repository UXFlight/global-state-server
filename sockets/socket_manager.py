from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from zoneinfo import ZoneInfo

from flask import request
from custom_types.public_view import PilotPublicView, StepPublicView
from sockets.socket import socket_service
from pilot.pilot_manager import PilotManager
from database.database_manager import DatabaseManager
from custom_types.update_step_data import UpdateStepData
from core.communication_service import communication_service

class SocketManager:
    def __init__(self, pilot_manager: PilotManager, db_manager: DatabaseManager):
        self.pilot_manager: PilotManager = pilot_manager
        self.db_manager: DatabaseManager = db_manager
        self.connections: dict[str, str] = {}  # 'PB' or 'AB' -> sid
        self.socket = socket_service

    def _send(self, role: str, event: str, data: Any) -> None:
        sid = self.connections.get(role)
        if sid:
            self.socket.send(event, data, room=sid)
        else:
            print(f"[SOCKET] ⚠️ No connection for role '{role}' to send event '{event}'")

    def _send_to_pilot(self, event: str, data: Any) -> None:
        self._send("PB", event, data)

    def _send_to_atc(self, event: str, data: Any) -> None:
        self._send("AB", event, data)

    def init_events(self) -> None:
        self.socket.listen("connect", self.on_connect)
        self.socket.listen("disconnect", self.on_disconnect)

        # pilots evenets
        self.socket.listen("get_pilot_list", self.send_pilot_list)
        self.socket.listen("new_pilot", self.on_new_pilot)
        self.socket.listen("pilot_disconnected", self.on_pilot_disconnect)

        # state events
        self.socket.listen("update_step", self.on_update_step)

    # === CONNECT EVENT === #
    def on_connect(self, auth=None) -> None:
        sid: str = request.sid
        client_type = auth.get("client_type") if auth else None

        if client_type not in ("PB", "AB"):
            print(f"[SOCKET] ❌ Invalid client_type: {client_type}")
            return

        if client_type in self.connections:
            print(f"[SOCKET] ❌ {client_type} already connected. Rejecting SID {sid}")
            return

        self.connections[client_type] = sid
        now = datetime.now(ZoneInfo("America/Toronto")).strftime("%H:%M:%S")

        if client_type == "PB":
            pilot_payload = {"facility": "KLAX", "connectedSince": now} #! TEMPORARY
            self._send_to_pilot("gss_connected", pilot_payload)
            print(f"Pilot payload sent")

        print(f"[SOCKET] ✅ {client_type} connected (SID: {sid})")

    # === DISCONNECT EVENT === #
    def on_disconnect(self, data) -> None:
        sid: str = request.sid
        role = next((r for r, s in self.connections.items() if s == sid), None)

        if role:
            self.connections.pop(role)
            print(f"[SOCKET] 🔌 {role} disconnected (SID: {sid})")
        else:
            print(f"[SOCKET] ⚠️ Unknown SID disconnected: {sid}")

    # === SEND PILOT LIST TO ATC === #
    def send_pilot_list(self) -> None:
        if self.pilot_manager.has_any_pilot():
            print("[SOCKET] Sending pilot list to ATC")
            payload = [
                pilot.to_public_view() for pilot in self.pilot_manager.get_all_pilots()
            ]
            communication_service.send_pilot_list(payload)

    # === NEW PILOT === #
    def on_new_pilot(self, pilot_sid: str) -> None:
        if not pilot_sid:
            print("[SOCKET] ❌ new_pilot missing pilot_sid")
            return

        pilot = self.pilot_manager.create_pilot(pilot_sid)
        print(f"[SOCKET] ✅ Registered new pilot: {pilot_sid}")
        communication_service.send_new_pilot(pilot)

    # === PILOT DISCONNECT EVENT === #
    def on_pilot_disconnect(self, pilot_sid: str) -> None:
        if not pilot_sid:
            print("[SOCKET] ❌ pilot_disconnected missing pilot_sid")
            return

        self.pilot_manager.remove_pilot(pilot_sid)
        communication_service.send_pilot_disconnected(pilot_sid)

    # === UPDATE STEP EVENT === #
    def on_update_step(self, data: dict) -> None:
        parsed: Optional[UpdateStepData] = UpdateStepData.from_dict(data)
        sid : str = request.sid
        if not parsed:
            print("[SOCKET] ❌ Invalid step update payload")
            return

        pilot = self.pilot_manager.get_pilot(parsed.pilot_sid)
        if not pilot:
            print(f"[SOCKET] ❌ Unknown pilot SID: {parsed.pilot_sid}")
            return

        pilot.get_or_create_step(parsed.step_code, label=parsed.label)
        result : StepPublicView = pilot.update_step(
            step_code=parsed.step_code,
            status=parsed.status,
            message=parsed.message,
            validated_at=parsed.validated_at,
            request_id=parsed.request_id,
            timestamp=datetime.now(ZoneInfo("America/Toronto")).timestamp(),
            time_left=parsed.time_left
        )

        result["pilot_sid"] = pilot.sid
        communication_service.send_step_update(result)
