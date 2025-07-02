from dataclasses import dataclass, field
from typing import Optional, List
import threading
import time
from custom_types.public_view import StepPublicView
from custom_types.update_step_data import StepStatus


@dataclass
class StepEvent:
    status: StepStatus
    timestamp: float
    message: str = ''

@dataclass
class Step:
    step_code: str
    label: str
    request_id: str = ""
    message: str = ''
    status: StepStatus = StepStatus.IDLE
    timestamp: float = field(default_factory=time.time)
    validated_at: float = field(default_factory=time.time)
    time_left: Optional[float] = None
    event_log: List[StepEvent] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def update(
        self,
        status: StepStatus,
        message: str,
        timestamp: float,
        validated_at: float,
        request_id: str,
        time_left: Optional[float] = None
    ) -> None:
        with self.lock:
            self.status = status
            self.message = message
            self.timestamp = timestamp
            self.validated_at = validated_at
            self.request_id = request_id
            self.time_left = time_left
            self.event_log.append(StepEvent(status=status, timestamp=timestamp, message=message))

    def reset(self) -> None:
        with self.lock:
            now = time.time()
            self.status = StepStatus.IDLE
            self.message = ''
            self.timestamp = now
            self.validated_at = now
            self.request_id = ""
            self.time_left = None
            self.event_log.clear()

    def to_public_view(self) -> StepPublicView:
        return {
            "pilot_sid": None,
            "step_code": self.step_code,
            "label": self.label,
            "status": self.status.value,
            "message": self.message,
            "timestamp": self.timestamp,
            "validated_at": self.validated_at,
            "request_id": self.request_id,
            "time_left": self.time_left,
        }