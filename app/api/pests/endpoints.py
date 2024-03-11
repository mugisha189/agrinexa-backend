# app/api/pests/endpoints.py
from fastapi import APIRouter, HTTPException
from app.api.pests.models import Pest
from app.db import db

router = APIRouter()

@router.post("/", tags=["Pests"])
async def create_pest(pest: Pest):
    new_pest = pest.dict()
    pest_id = db.pests.insert_one(new_pest).inserted_id
    return {"id": str(pest_id), **new_pest}

@router.get("/", tags=["Pests"])
async def get_pests():
    pests = list(db.pests.find())
    return pests

@router.get("/{pest_id}", tags=["Pests"])
async def get_pest(pest_id: str):
    pest = db.pests.find_one({"_id": pest_id})
    if pest:
        return pest
    else:
        raise HTTPException(status_code=404, detail="Pest not found")

@router.put("/{pest_id}", tags=["Pests"])
async def update_pest(pest_id: str, updated_pest: Pest):
    updated_pest_data = updated_pest.dict()
    result = db.pests.update_one({"_id": pest_id}, {"$set": updated_pest_data})
    if result.modified_count == 1:
        return {"message": "Pest updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Pest not found")

@router.delete("/{pest_id}", tags=["Pests"])
async def delete_pest(pest_id: str):
    result = db.pests.delete_one({"_id": pest_id})
    if result.deleted_count == 1:
        return {"message": "Pest deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Pest not found")
