# app/api/pests/endpoints.py
from fastapi import APIRouter, HTTPException,UploadFile, File
from app.api.pests.models import Pest
from app.db import db

router = APIRouter()


@router.post("/detect", 
             summary="Detect pests using an image",
             responses={
                 200: {"description": "Pest detection successfully"},
                 422: {"description": "Invalid data provided."},
                 500: {"description": "Internal Server Error."}
             })
async def detect_pest(image: UploadFile = File(...)):
    try:
        # Process the image using the provided model
        processed_data = process_image(image)
        return {"data": processed_data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while creating the pest entry.")

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
