# app/api/plantings/__init__.py
from fastapi import APIRouter
from . import endpoints

router = APIRouter()

router.include_router(endpoints.router, prefix="/nutrients",tags=["Nutrients"])
