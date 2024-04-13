
from fastapi import APIRouter, Depends, HTTPException,status
from app.api.fields.models import Field
from app.api.auth import User
from app.db import db
from bson import ObjectId
from app.dependencies import AuthRole,get_current_user

router = APIRouter()

@router.post("/")
async def create_field(field: Field,authorize:bool = Depends(AuthRole(roles="Admin"))):
    new_field = field.dict()
    field_id = db.fields.insert_one(new_field).inserted_id
    return {"id": str(field_id), **new_field}


@router.get("/")
async def get_fields(authorize:bool = Depends(AuthRole(roles="Admin"))):
    fields = list(db.fields.find())
    return fields


@router.get("/mine")
async def get_fields_for_logged_in_user(authorize:bool = Depends(AuthRole(roles="User")),user: User = Depends(get_current_user)):
    try:
        fields = list(db.fields.find({"owner": ObjectId(user["_id"])}))
        return fields
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving fields.",
        )


@router.get("/user/:id")
async def get_fields_for_user_by_id(id:str):
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
