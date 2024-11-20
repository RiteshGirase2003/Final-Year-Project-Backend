from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from enum import Enum
from typing import Optional


class Routine(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    worker_id: str
    worker_name: str
    worker_reg_no: str
    date: datetime
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
