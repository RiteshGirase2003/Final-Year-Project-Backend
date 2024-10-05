from pydantic import BaseModel, Field
from bson import ObjectId

class Worker(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    reg_no: str
    password: str
    photo: str = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
