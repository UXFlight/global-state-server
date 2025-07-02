from typing import Any, Optional
from flask_socketio import SocketIO

class SocketService:
    def __init__(self):
        self.socketio: SocketIO | None = None

    def init(self, socketio: SocketIO) -> None:
        self.socketio = socketio

    def send(self, event: str, payload: Any, room: Optional[str] = None) -> None:
        if self.socketio:
            self.socketio.emit(event, payload, room=room)

    def listen(self, event: str, callback):
        if not self.socketio:
            raise RuntimeError("SocketIO not initialized. Call init() before listen().")
        return self.socketio.on(event)(callback)

socket_service = SocketService()