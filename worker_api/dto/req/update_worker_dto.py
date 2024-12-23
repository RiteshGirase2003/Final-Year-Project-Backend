from pydantic import BaseModel, Field, StrictStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    worker = "worker"


class UpdateWorkerDTO(BaseModel):
    name: Optional[StrictStr]
    password: Optional[StrictStr]
    photo: Optional[StrictStr]
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    user_role: UserRole = Field(default=UserRole.worker)
    email: Optional[StrictStr] = Field(default="")
