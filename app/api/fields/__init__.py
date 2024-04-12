
from fastapi import APIRouter
from . import endpoints

router = APIRouter()

router.include_router(endpoints.router, prefix="/fields",tags=["Fields"])
