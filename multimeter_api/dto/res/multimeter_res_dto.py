from pydantic import BaseModel, Field, StrictStr
from typing import List
from datetime import datetime


class MultimeterResDTO(BaseModel):
    id: StrictStr = Field(..., description="The ID of the multimeter")
    serial_no: StrictStr = Field(..., description="The serial number of the multimeter")
    model: StrictStr = Field(..., description="The model of the multimeter")
    description: StrictStr = Field(..., description="A description of the multimeter")
    photo: StrictStr = Field(..., description="A photo URL of the multimeter")
    screen_photos: List[StrictStr] = Field(
        ..., description="A list of screen photo URLs of the multimeter"
    )
    created_at: datetime
    updated_at: datetime
