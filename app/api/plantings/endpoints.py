from fastapi import APIRouter, Depends, HTTPException
from app.api.plantings.models import Planting
from app.db import db

router = APIRouter()

@router.post("/")
async def create_planting(planting: Planting):
    new_planting = planting.dict()
    planting_id = db.plantings.insert_one(new_planting).inserted_id
    return {"id": str(planting_id), **new_planting}

@router.get("/")
async def get_plantings():
    plantings = list(db.plantings.find())
    return plantings

@router.get("/{planting_id}")
async def get_planting(planting_id: str):
    planting = db.plantings.find_one({"_id": planting_id})
    if planting:
        return planting
    else:
        raise HTTPException(status_code=404, detail="Planting not found")

@router.put("/{planting_id}")
async def update_planting(planting_id: str, updated_planting: Planting):
    updated_planting_data = updated_planting.dict()
    result = db.plantings.update_one({"_id": planting_id}, {"$set": updated_planting_data})
    if result.modified_count == 1:
        return {"message": "Planting updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Planting not found")

@router.delete("/{planting_id}")
async def delete_planting(planting_id: str):
    result = db.plantings.delete_one({"_id": planting_id})
    if result.deleted_count == 1:
        return {"message": "Planting deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Planting not found")
