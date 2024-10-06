from pydantic import BaseModel, Field, StrictStr
from typing import Optional


class UpdateWorkerDTO(BaseModel):
    name: Optional[StrictStr]
    password: Optional[StrictStr]
    photo: Optional[StrictStr]
