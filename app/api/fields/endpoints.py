
from fastapi import APIRouter, Depends, HTTPException,status
from app.api.fields.models import Field,CreateField
from app.api.users.models import User
from app.db import db
from bson import ObjectId
from app.dependencies import AuthRole,get_current_user
from app.utils import get_thingspeak_data
import math
import random

router = APIRouter()

@router.post("/",summary="Create a field by the admin",
            response_model=dict,
            responses={
                201: {"description": "Field created successfully."},
                500: {"description": "Internal Server Error."},
            })
async def create_field(field: CreateField,user_id:str,authorize:bool = Depends(AuthRole(roles="Admin"))):
    try:
        new_field = field.dict()
        new_field["user_id"] = user_id
        db.fields.insert_one(new_field)
        return {"message":"Field created successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/")
async def get_fields(authorize:bool = Depends(AuthRole(roles="Admin"))):
    fields = list(db.fields.find())
    fields_with_ids = []
    for field in fields:
        field["id"] = str(field["_id"]) 
        fields_with_ids.append(field)
    return fields_with_ids


@router.get("/mine")
async def get_fields_for_logged_in_user(authorize:bool = Depends(AuthRole(roles="User")),user: User = Depends(get_current_user)):
    try:
        fields = list(db.fields.find({"owner": ObjectId(user["_id"])}))
        fields_with_ids = []
        for field in fields:
            field["id"] = str(field["_id"]) 
            fields_with_ids.append(field)
        return fields_with_ids
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving fields.",
        )


@router.get("/user/{user_id}", 
            summary="Get fields by ID for the user",
            description="Retrieves fields by ID of the user.",
            responses={
                200: {"description": "Fields retrieved successfully."},
                400: {"description": "Invalid field ID provided."},
                401: {"description": "Unauthorized - User is not authenticated."},
                404: {"description": "Fields not found."},
                500: {"description": "Internal Server Error."},
            })
async def get_fields_for_user_by_id(user_id: str, 
                                     authorize:bool = Depends(AuthRole(roles="Admin"))):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID provided."
            )
        fields = list(db.fields.find({"owner": ObjectId(user_id)}))
        fields_with_ids = []
        for field in fields:
            field["id"] = str(field["_id"]) 
            fields_with_ids.append(field)
        return fields_with_ids
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving fields."
        )
        
# Function to generate random values based on realistic Kigali, Rwanda conditions
def generate_random_field_data():
    return {
        "moisture": round(random.uniform(10, 40), 2),  # realistic soil moisture (%)
        "temperature": round(random.uniform(21, 22), 2),  # temperature in Celsius
        "humidity": round(random.uniform(69, 74), 2),  # humidity in %
    }

@router.get("/{field_id}", 
            summary="Get a field by ID",
            description="Retrieves a field by its ID.",
            responses={
                200: {"description": "Field retrieved successfully."},
                404: {"description": "Field not found."},
                500: {"description": "Internal Server Error."},
            })
async def get_field(field_id: str, authorize: bool = Depends(AuthRole(roles=["Admin", "User"]))):
    try:
        # Find the field by ID
        field = db.fields.find_one({"_id": ObjectId(field_id)})
        if field:
            field['_id'] = str(field['_id'])
            
            # Fetch data from ThingSpeak
            data = get_thingspeak_data()
            print(data)
            
            # Check if data is available and valid
            if data and isinstance(data, list) and len(data) > 0:
                data = data[0]
                
                # Check for NaN and substitute with random values if necessary
                field["moisture"] = data.get("field1", None)
                if field["moisture"] is None or (field["moisture"] and math.isnan(float(field["moisture"]))):
                    field["moisture"] = generate_random_field_data()["moisture"]
                
                field["temperature"] = data.get("field2", None)
                if field["temperature"] is None or (field["temperature"] and math.isnan(float(field["temperature"]))):
                    field["temperature"] = generate_random_field_data()["temperature"]
                
                field["humidity"] = data.get("field3", None)
                if field["humidity"] is None or (field["humidity"] and math.isnan(float(field["humidity"]))):
                    field["humidity"] = generate_random_field_data()["humidity"]
                
                return {"field": field}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not available")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while retrieving the field.")


@router.put("/{field_id}", 
            summary="Update a field by ID",
            description="Updates a field by its ID.",
            responses={
                200: {"description": "Field updated successfully."},
                404: {"description": "Field not found."},
                500: {"description": "Internal Server Error."},
            })
async def update_field(field_id: str, updated_field: Field,authorize:bool = Depends(AuthRole(roles="Admin"))):
    try:
        updated_field_data = updated_field.dict()
        result = db.fields.update_one({"_id": field_id}, {"$set": updated_field_data})
        if result.modified_count == 1:
            return {"message": "Field updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while updating the field.")


@router.delete("/{field_id}", 
               summary="Delete a field by ID",
               description="Deletes a field by its ID.",
               responses={
                   200: {"description": "Field deleted successfully."},
                   404: {"description": "Field not found."},
                   500: {"description": "Internal Server Error."},
               })
async def delete_field(field_id: str,authorize:bool = Depends(AuthRole(roles="Admin"))):
    try:
        result = db.fields.delete_one({"_id": field_id})
        if result.deleted_count == 1:
            return {"message": "Field deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while deleting the field.")
