# app/api/fields/models.py
from pydantic import BaseModel
from  app.api.auth import User

class Field(BaseModel):
    name: str
    location: str
    size: float
    sensorId:str
    owner:User
