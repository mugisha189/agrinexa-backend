# app/api/pests/models.py
from pydantic import BaseModel

class Pest(BaseModel):
    name: str
    type: str
    severity: str
