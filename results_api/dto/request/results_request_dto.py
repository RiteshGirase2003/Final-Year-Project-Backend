from pydantic import BaseModel
from enum import Enum


class StatusEnum(str, Enum):
    pass_ = "pass"
    fail = "fail"


class ResultsRequestDTO(BaseModel):
    meter_id: str
    worker_id: str
    status: StatusEnum
