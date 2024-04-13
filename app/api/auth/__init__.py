
from fastapi import APIRouter
from . import endpoints
from .models import User,Role
router = APIRouter()
router.include_router(endpoints.router, prefix="/auth",tags=["Auth"])
