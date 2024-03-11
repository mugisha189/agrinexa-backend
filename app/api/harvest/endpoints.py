from fastapi import APIRouter, Depends, HTTPException
from app.api.harvest.models import Harvest
from app.db import db

router = APIRouter()

@router.post("/")
async def create_harvest(harvest: Harvest):
    new_harvest = harvest.dict()
    harvest_id = db.harvests.insert_one(new_harvest).inserted_id
    return {"id": str(harvest_id), **new_harvest}

@router.get("/")
async def get_harvests():
    harvests = list(db.harvests.find())
    return harvests

@router.get("/{harvest_id}")
async def get_harvest(harvest_id: str):
    harvest = db.harvests.find_one({"_id": harvest_id})
    if harvest:
        return harvest
    else:
        raise HTTPException(status_code=404, detail="Harvest not found")

@router.put("/{harvest_id}")
async def update_harvest(harvest_id: str, updated_harvest: Harvest):
    updated_harvest_data = updated_harvest.dict()
    result = db.harvests.update_one({"_id": harvest_id}, {"$set": updated_harvest_data})
    if result.modified_count == 1:
        return {"message": "Harvest updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Harvest not found")

@router.delete("/{harvest_id}")
async def delete_harvest(harvest_id: str):
    result = db.harvests.delete_one({"_id": harvest_id})
    if result.deleted_count == 1:
        return {"message": "Harvest deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Harvest not found")
