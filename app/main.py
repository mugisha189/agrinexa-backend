# app/main.py
from fastapi import FastAPI
from app.db import db
from app.api import auth, fields, plantings, harvests, nutrients, weather, pests
app = FastAPI()
app.include_router(auth.router)
app.include_router(fields.router)
app.include_router(plantings.router)
app.include_router(harvests.router)
app.include_router(nutrients.router)
app.include_router(weather.router)
app.include_router(pests.router)
