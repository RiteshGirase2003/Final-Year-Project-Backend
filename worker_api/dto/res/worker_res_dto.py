from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Optional
from datetime import datetime


class WorkerResDTO(BaseModel):
    id: StrictStr
    name: StrictStr
    reg_no: StrictInt
    password: StrictStr
    photo: StrictStr
    created_at: datetime
    updated_at: datetime
