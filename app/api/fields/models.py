# app/api/fields/models.py
from pydantic import BaseModel
from  app.api.users.models import User
from typing import Optional
class Field(BaseModel):
    id:Optional[str]
    name: str
    lat: float
    long: float
    size: float
    user_id:str
    moisture:float
    temperature:float
    humidity:float
    

class CreateField(BaseModel):
    name: str
    lat: float
    long: float
    size: float
