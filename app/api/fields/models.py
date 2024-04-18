# app/api/fields/models.py
from pydantic import BaseModel
from  app.api.users.models import User

class Field(BaseModel):
    name: str
    lat: float
    long: float
    size: float
    user_id:str
    

class CreateField(BaseModel):
    name: str
    lat: float
    long: float
    size: float
