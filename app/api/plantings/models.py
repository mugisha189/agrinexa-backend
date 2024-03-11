from pydantic import BaseModel
from datetime import date

class Planting(BaseModel):
    field_id: str
    crop: str
    planting_date: date
    quantity: int
