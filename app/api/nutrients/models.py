from pydantic import BaseModel

class Nutrient(BaseModel):
    name: str
    type: str
    quantity: float
