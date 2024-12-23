from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    worker = "worker"

class WorkerResDTO(BaseModel):
    id: StrictStr
    name: StrictStr
    reg_no: StrictStr
    photo: StrictStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user_role: UserRole
    email: StrictStr
