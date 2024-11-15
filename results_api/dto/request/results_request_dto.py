from pydantic import BaseModel, StrictStr
from enum import Enum


class StatusEnum(str, Enum):
    pass_ = "pass"
    fail = "fail"


class ResultsRequestDTO(BaseModel):
    serial_no: StrictStr
    meter_id: StrictStr
    worker_id: StrictStr
    status: StatusEnum
    client: StrictStr
