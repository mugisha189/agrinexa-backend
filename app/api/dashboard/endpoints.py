
from fastapi import APIRouter, Depends, HTTPException,status
from app.api.users.models import User,Role
from app.db import db
from bson import ObjectId
from app.dependencies import AuthRole,get_current_user

router = APIRouter()




from fastapi import HTTPException, status
from app.db import db
from app.dependencies import get_current_user
from app.api.users.models import User

@router.get("/", 
            summary="Get the dashboard for the logged in user",
            response_model=User,
            responses={
                200: {"description": "Dashboard retrieved successfully."},
                401: {"description": "Unauthorized - User is not authenticated."},
                500: {"description": "Internal Server Error."},
            })
async def get_dashboard_for_logged_in_user(user: User = Depends(get_current_user)) -> User:
    try:
        user_data = db.users.find_one({"_id": user.id}, {"balance": 1, "history": 1})
        if user_data:
            return user_data
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User data not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user data."
        )


