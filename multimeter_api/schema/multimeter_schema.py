from pydantic import BaseModel
from typing import Optional

class MultimeterSchema(BaseModel):
    id: Optional[int]
    brand: str
    model: str
    serial_number: str
    calibration_date: Optional[str]
    measurement_type: str
    value: float
    unit: str

    class Config:
        orm_mode: True