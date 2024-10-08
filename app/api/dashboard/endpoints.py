
from fastapi import APIRouter, Depends, HTTPException,status
from app.api.users.models import User,Role
from app.db import db
import random
from bson import ObjectId
from app.dependencies import AuthRole,get_current_user
from app.utils import get_thingspeak_data

router = APIRouter()




from fastapi import HTTPException, status
from app.db import db
from app.dependencies import get_current_user
from app.api.users.models import User
from .models import DashboardModel

AGRICULTURE_TIPS = [
    {"title": "Tip 1", "body": "Ensure proper irrigation for your crops."},
    {"title": "Tip 2", "body": "Use organic fertilizers to improve soil health."},
    {"title": "Tip 3", "body": "Rotate crops to maintain soil fertility."},
    {"title": "Tip 4", "body": "Monitor soil moisture levels regularly."},
    {"title": "Tip 5", "body": "Implement integrated pest management strategies."},
    {"title": "Tip 6", "body": "Utilize drip irrigation to conserve water."},
    {"title": "Tip 7", "body": "Select crop varieties suited to your climate."},
    {"title": "Tip 8", "body": "Practice conservation tillage to reduce soil erosion."},
    {"title": "Tip 9", "body": "Plant cover crops to enhance soil structure."},
    {"title": "Tip 10", "body": "Implement crop rotation to prevent pests and diseases."},
    {"title": "Tip 11", "body": "Use mulch to retain soil moisture."},
    {"title": "Tip 12", "body": "Test soil regularly for nutrient levels."},
    {"title": "Tip 13", "body": "Adopt precision farming techniques."},
    {"title": "Tip 14", "body": "Harvest crops at the right time to ensure quality."},
    {"title": "Tip 15", "body": "Practice agroforestry for sustainable farming."},
    {"title": "Tip 16", "body": "Ensure proper storage of harvested crops."},
    {"title": "Tip 17", "body": "Use high-quality seeds for better yields."},
    {"title": "Tip 18", "body": "Implement water-saving techniques."},
    {"title": "Tip 19", "body": "Maintain farm equipment regularly."},
    {"title": "Tip 20", "body": "Practice good farm hygiene to prevent disease."},
]

@router.get(
    "/",
    summary="Get the dashboard for the logged-in user",
    response_model=DashboardModel,
    responses={
        200: {"description": "Dashboard retrieved successfully."},
        401: {"description": "Unauthorized - User is not authenticated."},
        500: {"description": "Internal Server Error."},
    },
)

async def get_dashboard_for_logged_in_user(user: User = Depends(get_current_user)) -> dict[str, any]:
    try:
        user_data = db.users.find_one({"_id": user["_id"]})
        user_fields = db.fields.find({"user_id": str(user["_id"])})
        fields_with_ids = []
        for field in user_fields:
            field["id"] = str(field["_id"])
            data = get_thingspeak_data()
            print(data)
            field["moisture"] = data[0]["field1"]
            field["temperature"] = data[0]["field2"]
            field["humidity"] = data[0]["field3"]
            fields_with_ids.append(field)
        
        if user_data:
            # Randomly select 5 tips from the list of agriculture tips
            random_tips = random.sample(AGRICULTURE_TIPS, 5)
            return {"user": user_data, "fields": fields_with_ids, "tips": random_tips}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User data not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user data."
        )


