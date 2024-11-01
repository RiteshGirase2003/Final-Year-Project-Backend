from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional

class Results(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    meter_id: str
    worker_id: str
    status: str
    date: datetime
    time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }