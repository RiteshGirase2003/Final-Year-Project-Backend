from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Optional
from datetime import datetime


class CreateWorkerDTO(BaseModel):
    name: StrictStr
    reg_no: StrictInt
    password: StrictStr
    photo: StrictStr
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: Optional[bool] = Field(default=True)
