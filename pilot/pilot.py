from typing import Dict, List, Optional
from custom_types.public_view import PilotPublicView, StepPublicView
from logger.log_manager import log_manager
from state.step import Step, StepEvent
from custom_types.update_step_data import StepStatus


class Pilot:
    def __init__(self, sid: str):
        self.sid = sid
        self.steps: Dict[str, Step] = {}
        self.history: List[StepEvent] = []

    def get_or_create_step(self, code: str, label: str) -> Step:
        if code not in self.steps:
            self.steps[code] = Step(step_code=code, label=label)
        return self.steps[code]

    def get_step(self, code: str) -> Step: #! WITHER RAISE ERROR OR RETURN NONE
        try:
            return self.steps[code]
        except KeyError:
            raise ValueError(f"Step '{code}' does not exist.")

    ##! GETS PUBLIC VIEW OF PILOT
    def to_public_view(self) -> PilotPublicView:
        return {
            "sid": self.sid,
            "steps": {
                step_code: step.to_public_view()
                for step_code, step in self.steps.items()
            },
            "history": [
                {
                    "status": event.status.value,
                    "timestamp": event.timestamp,
                    "message": event.message,
                }
                for event in self.history
            ],
        }
    
    ##! UPDATE STEP + RETURNS PUBLIC VIEW OF STEP
    def update_step(
        self,
        step_code: str,
        status: StepStatus,
        message: str,
        validated_at: float,
        request_id: str,
        timestamp: float,
        time_left: Optional[float] = None
    ) -> StepPublicView:
        step = self.get_step(step_code)

        step.update(
            status=status,
            message=message,
            timestamp=timestamp,
            validated_at=validated_at,
            request_id=request_id,
            time_left=time_left,
        )

        self.history.append(StepEvent(status=status, timestamp=timestamp, message=message))

        log_manager.log_pilot_event(
            self.sid,
            "update_step",
            {
                "step_code": step_code,
                "status": status.value,
                "message": message,
                "request_id": request_id,
                "validated_at": validated_at,
                "time_left": time_left
            }
        )

        return step.to_public_view()

    def reset(self) -> None:
        for step in self.steps.values():
            step.reset()
