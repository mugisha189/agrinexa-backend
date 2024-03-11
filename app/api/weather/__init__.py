# app/api/weather/__init__.py
from fastapi import APIRouter
from . import endpoints

router = APIRouter()

router.include_router(endpoints.router, prefix="/weather",tags=["Weather"])
