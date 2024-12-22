from pydantic import BaseModel, constr
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    pass_ = "pass"
    fail = "fail"


class ResultsRequestDTO(BaseModel):
    serial_no: constr(strict=True, min_length=1)
    meter_id: constr(strict=True, min_length=1)
    worker_id: constr(strict=True, min_length=1)
    status: StatusEnum
    client: constr(strict=True, min_length=1)
