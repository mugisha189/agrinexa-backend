
from fastapi import APIRouter, Depends, HTTPException
from app.api.fields.models import Field
from app.db import db

router = APIRouter()

@router.post("/")
async def create_field(field: Field):
    new_field = field.dict()
    field_id = db.fields.insert_one(new_field).inserted_id
    return {"id": str(field_id), **new_field}

@router.get("/")
async def get_fields():
    fields = list(db.fields.find())
    return fields

@router.get("/{field_id}")
async def get_field(field_id: str):
    field = db.fields.find_one({"_id": field_id})
    if field:
        return field
    else:
        raise HTTPException(status_code=404, detail="Field not found")

@router.put("/{field_id}")
async def update_field(field_id: str, updated_field: Field):
    updated_field_data = updated_field.dict()
    result = db.fields.update_one({"_id": field_id}, {"$set": updated_field_data})
    if result.modified_count == 1:
        return {"message": "Field updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Field not found")

@router.delete("/{field_id}")
async def delete_field(field_id: str):
    result = db.fields.delete_one({"_id": field_id})
    if result.deleted_count == 1:
        return {"message": "Field deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Field not found")
