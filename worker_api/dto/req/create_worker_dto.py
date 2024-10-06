from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Optional
from datetime import datetime


class CreateWorkerDTO(BaseModel):
    name: StrictStr
    reg_no: StrictInt
    password: StrictStr
    photo: StrictStr
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
