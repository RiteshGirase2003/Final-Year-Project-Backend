from pydantic import BaseModel, Field, StrictStr
from typing import List
from datetime import datetime


class MultimeterResDTO(BaseModel):
    id: StrictStr
    serial_no: StrictStr
    model: StrictStr
    description: StrictStr
    photo: StrictStr
    screen_photos: List[StrictStr]
    created_at: datetime
    updated_at: datetime
