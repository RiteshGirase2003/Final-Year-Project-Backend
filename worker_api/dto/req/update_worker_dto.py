from pydantic import BaseModel, Field, StrictStr
from typing import Optional
from datetime import datetime


class UpdateWorkerDTO(BaseModel):
    name: Optional[StrictStr]
    password: Optional[StrictStr]
    photo: Optional[StrictStr]
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
