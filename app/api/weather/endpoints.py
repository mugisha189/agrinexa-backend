# app/api/weather/endpoints.py
from fastapi import APIRouter, HTTPException
from app.api.weather.models import WeatherData
from app.db import db

router = APIRouter()

@router.post("/", tags=["Weather"])
async def create_weather(weather_data: WeatherData):
    new_weather_data = weather_data.dict()
    weather_id = db.weather.insert_one(new_weather_data).inserted_id
    return {"id": str(weather_id), **new_weather_data}

@router.get("/", tags=["Weather"])
async def get_weather():
    weather_data = list(db.weather.find())
    return weather_data

@router.get("/{weather_id}", tags=["Weather"])
async def get_specific_weather(weather_id: str):
    weather_data = db.weather.find_one({"_id": weather_id})
    if weather_data:
        return weather_data
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")

@router.put("/{weather_id}", tags=["Weather"])
async def update_weather(weather_id: str, updated_weather: WeatherData):
    updated_weather_data = updated_weather.dict()
    result = db.weather.update_one({"_id": weather_id}, {"$set": updated_weather_data})
    if result.modified_count == 1:
        return {"message": "Weather data updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")

@router.delete("/{weather_id}", tags=["Weather"])
async def delete_weather(weather_id: str):
    result = db.weather.delete_one({"_id": weather_id})
    if result.deleted_count == 1:
        return {"message": "Weather data deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")