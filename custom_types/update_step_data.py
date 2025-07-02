from enum import Enum
from typing import Optional
from dataclasses import dataclass

class StepStatus(Enum):
    IDLE = "idle"
    REQUESTED = "requested"
    NEW = "new"
    LOADED = "loaded"
    EXECUTED = "executed"
    CANCELLED = "cancelled"
    CLOSED = "closed"
    STANDBY = "standby"
    UNABLE = "unable"
    
@dataclass
class UpdateStepData:
    def __init__(
        self,
        pilot_sid: str,
        step_code: str,
        status: StepStatus,
        message: str,
        validated_at: float,
        request_id: str,
        time_left: Optional[float] = None,
        label: Optional[str] = None,
    ):
        self.pilot_sid = pilot_sid
        self.step_code = step_code
        self.status = status
        self.message = message
        self.validated_at = validated_at
        self.request_id = request_id
        self.time_left = time_left
        self.label = label or step_code

    @staticmethod
    def from_dict(data: dict) -> Optional["UpdateStepData"]:
        try:
            return UpdateStepData(
                pilot_sid=data["pilot_sid"],
                step_code=data["step_code"],
                label=data.get("label"),
                status=StepStatus(data["status"]),
                message=data["message"],
                validated_at=data["validated_at"],
                request_id=data["request_id"],
                time_left=data.get("time_left"),
            )
        except KeyError as e:
            print(f"[PARSE] Missing key in update_step: {e}")
            return None
