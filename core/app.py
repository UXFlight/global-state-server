import signal
import sys
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from sockets.socket import socket_service
from sockets.socket_manager import SocketManager
from pilot.pilot_manager import PilotManager
from database.database_manager import DatabaseManager 


class App:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        socket_service.init(self.socketio)

        self.pilot_manager = PilotManager()
        self.db_manager = DatabaseManager()
        self.socket_manager = SocketManager(self.pilot_manager, self.db_manager)

    def start(self, host="0.0.0.0", port=5322):
        self._handle_signals()
        self.socket_manager.init_events()
        print(f"[GSS] Running Global State Server on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, use_reloader=False, allow_unsafe_werkzeug=True)

    def _handle_signals(self):
        def shutdown(sig, frame):
            print("\n[GSS] Ctrl+C detected. Shutting down.")
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown)
