from typing import TypedDict, Optional, Dict, List
from custom_types.update_step_data import StepStatus

class StepPublicView(TypedDict):
    pilot_sid: Optional[str]
    step_code: str
    label: str
    status: str
    message: str
    timestamp: float
    validated_at: float
    request_id: str
    time_left: Optional[float]


class StepHistoryEvent(TypedDict):
    status: str
    timestamp: float
    message: Optional[str]

class PilotPublicView(TypedDict):
    sid: str
    steps: Dict[str, StepPublicView]
    history: List[StepHistoryEvent]
