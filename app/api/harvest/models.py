from pydantic import BaseModel
from datetime import date

class Harvest(BaseModel):
    field_id: str
    crop: str
    harvest_date: date
    quantity: int
