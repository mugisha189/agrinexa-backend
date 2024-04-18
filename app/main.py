# app/main.py
from fastapi import FastAPI
from app.db import db
from app.api import auth,fields,plantings,harvest,nutrients,weather,pests,users,dashboard
app = FastAPI(    title="Agrinexa",
    description="This is the documentation for Agrinexa, a platform for tracking fields and nutrients in agriculture. Backend developed by Mugisha Yves",)
@app.head("/")
async def handle_head_request():
    return "Hello Agrinexa"
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(fields.router)
app.include_router(plantings.router)
app.include_router(harvest.router)
app.include_router(nutrients.router)
app.include_router(weather.router)
app.include_router(pests.router)
