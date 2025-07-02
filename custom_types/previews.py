from typing import TypedDict
from custom_types.update_step_data import StepStatus


class StepPreview(TypedDict):
    step_code: str
    status: StepStatus


class PilotPreview(TypedDict):
    sid: str
    steps: dict[str, StepPreview]

class PilotListPayload(TypedDict):
    pilots: list[PilotPreview]