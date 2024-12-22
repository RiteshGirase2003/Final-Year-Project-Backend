from pydantic import BaseModel, Field, StrictStr
from typing import List
from datetime import datetime


class MultimeterResDTO(BaseModel):
    id: StrictStr
    model: StrictStr
    description: StrictStr
    photo: StrictStr
    created_at: datetime
    updated_at: datetime
    created_by: StrictStr
