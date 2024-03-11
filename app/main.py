# app/main.py
from fastapi import FastAPI
from app.db import db
from app.api import auth,fields
app = FastAPI(    title="Agrinexa",
    description="This is the documentation for AGrinexa, a platform for tracking fields and nutrients in agriculture.",)
app.include_router(auth.router)
app.include_router(fields.router)
# app.include_router(plantings.router)
# app.include_router(harvests.router)
# app.include_router(nutrients.router)
# app.include_router(weather.router)
# app.include_router(pests.router)
