# app/api/nutrients/endpoints.py
from fastapi import APIRouter, HTTPException
from app.api.nutrients.models import Nutrient
from app.db import db

router = APIRouter()

@router.post("/")
async def create_nutrient(nutrient: Nutrient):
    new_nutrient = nutrient.dict()
    nutrient_id = db.nutrients.insert_one(new_nutrient).inserted_id
    return {"id": str(nutrient_id), **new_nutrient}

@router.get("/")
async def get_nutrients():
    nutrients = list(db.nutrients.find())
    return nutrients

@router.get("/{nutrient_id}")
async def get_nutrient(nutrient_id: str):
    nutrient = db.nutrients.find_one({"_id": nutrient_id})
    if nutrient:
        return nutrient
    else:
        raise HTTPException(status_code=404, detail="Nutrient not found")

@router.put("/{nutrient_id}")
async def update_nutrient(nutrient_id: str, updated_nutrient: Nutrient):
    updated_nutrient_data = updated_nutrient.dict()
    result = db.nutrients.update_one({"_id": nutrient_id}, {"$set": updated_nutrient_data})
    if result.modified_count == 1:
        return {"message": "Nutrient updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Nutrient not found")

@router.delete("/{nutrient_id}")
async def delete_nutrient(nutrient_id: str):
    result = db.nutrients.delete_one({"_id": nutrient_id})
    if result.deleted_count == 1:
        return {"message": "Nutrient deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Nutrient not found")
