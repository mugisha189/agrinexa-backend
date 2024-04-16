from fastapi import APIRouter
from . import endpoints

router = APIRouter()

router.include_router(endpoints.router, prefix="/users",tags=["Users"])
