from pydantic import BaseModel, Field, StrictStr
from typing import List, Optional
from datetime import datetime


class UpdateMultimeterDTO(BaseModel):
    model: Optional[StrictStr]
    description: Optional[StrictStr]
    photo: Optional[StrictStr]
    screen_photos: Optional[List[StrictStr]]
    updated_at: Optional[datetime] = None
