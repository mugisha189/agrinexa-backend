from pydantic import BaseModel

class WeatherData(BaseModel):
    date: str
    temperature: float
    humidity: float
    precipitation: float
