from pydantic import BaseModel, Field, StrictStr
from typing import List, Optional
from datetime import datetime


class CreateMultimeterDTO(BaseModel):
    serial_no: StrictStr = Field(..., description="The serial number of the multimeter")
    model: StrictStr = Field(..., description="The model of the multimeter")
    description: StrictStr = Field(..., description="A description of the multimeter")
    photo: StrictStr = Field(..., description="A photo URL of the multimeter")
    screen_photos: List[StrictStr] = Field(
        ..., description="A list of screen photo URLs of the multimeter"
    )
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
