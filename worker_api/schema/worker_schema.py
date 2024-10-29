from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    admin = "admin"
    worker = "worker"

class Worker(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    reg_no: str
    password: str
    photo: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_role: UserRole = Field(default=UserRole.worker)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
