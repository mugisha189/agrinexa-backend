from fastapi import APIRouter, Depends, HTTPException
from .models import User,Role
from app.db import db
from typing import List
from app.dependencies import get_current_user,AuthRole

router = APIRouter()


@router.get("/", response_model=List[User], responses={200: {"description": "List of users retrieved successfully"}, 500: {"description": "Internal Server Error"}})
async def get_users(authorized:bool = Depends(AuthRole(roles=Role.Admin))):
    try:
        users = list(db.users.find())
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{user_id}", response_model=User, responses={200: {"description": " User retrieved successfully"}, 404: {"description": "Product not found"}, 500: {"description": "Internal Server Error"}})
async def get_user(user_id: str,authorized:bool = Depends(AuthRole(roles=[Role.Admin,Role.User]))):
    try:
        user = db.users.find_one({"_id": user_id})
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
    

@router.get("/my-profile", summary="Get the user's profile", response_model=User, responses={
    200: {"description": "User profile retrieved successfully"},
    404: {"description": "User not found"},
    500: {"description": "Internal Server Error"}
})
async def get_profile(user: User = Depends(get_current_user)):
    try:
        user_profile = db.users.find_one({"email": user.email})
        if user_profile:
            return user_profile
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/my-profile", summary="Update the user's profile", response_model=User, responses={
    200: {"description": "User profile updated successfully"},
    404: {"description": "User not found"},
    500: {"description": "Internal Server Error"}
})
async def update_profile(updated_user: User, user: User = Depends(get_current_user)):
    try:
        updated_user_data = updated_user.dict()
        result = db.users.update_one({"email": user.email}, {"$set": updated_user_data})
        if result.modified_count == 1:
            return updated_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    
    
@router.delete("/delete-my-account", summary="Delete the account of the currently logged-in user", response_model=dict, responses={
    200: {"description": "Account deleted successfully"},
    404: {"description": "Account not found"},
    500: {"description": "Internal Server Error"}
})
async def delete_my_account(user: User = Depends(get_current_user)):
    try:
        result = db.users.delete_one({"email": user.email})
        if result.deleted_count == 1:
            return {"message": "Account deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{user_id}", summary="Delete an account by user ID", response_model=dict, responses={
    200: {"description": "Account deleted successfully"},
    404: {"description": "Account not found"},
    500: {"description": "Internal Server Error"}
})
async def delete_account_by_id(user_id: str,authorize:bool = Depends(AuthRole(roles=Role.Admin))):
    try:
        result = db.users.delete_one({"_id": user_id})
        if result.deleted_count == 1:
            return {"message": "Account deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
