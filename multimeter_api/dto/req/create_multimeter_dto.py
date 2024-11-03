from pydantic import BaseModel, Field, StrictStr
from typing import List, Optional
from datetime import datetime


class CreateMultimeterDTO(BaseModel):
    serial_no: StrictStr
    model: StrictStr
    description: StrictStr
    photo: StrictStr
    screen_photos: List[StrictStr]
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: Optional[bool] = Field(default=True)
    created_by : StrictStr
