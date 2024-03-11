# app/api/fields/models.py
from pydantic import BaseModel

class Field(BaseModel):
    name: str
    location: str
    size: float
