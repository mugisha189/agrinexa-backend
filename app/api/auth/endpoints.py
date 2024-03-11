from fastapi import APIRouter, HTTPException, Depends
from app.api.auth.models import User, LoginModel,AuthResponseModel
from app.api.auth.security import verify_password, get_password_hash
from app.db import db
from jwt import jwt
from datetime import datetime, timedelta
import random
import string
from decouple import config

router = APIRouter()

SECRET_KEY = config("SECRET_KEY")
REFRESH_SECRET_KEY = config("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None
    return user


@router.post("/login",response_model=AuthResponseModel)
async def login(cred:LoginModel):
    creds = dict(user)
    user = authenticate_user(creds["email"], creds["password"])
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    return {
        "user": {
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "email": user["email"],
            "phone": user["phone"],  
        },
        "access_token": access_token,
    }


@router.post("/register",response_model=AuthResponseModel)
async def register_user(user: User):
    user_data = user.dict()
    user_data["password"] = get_password_hash(user_data.pop("password"))
    user_data["emailVerified"] = False
    user_data["phoneVerified"] = False
    user_id = db.users.insert_one(user_data).inserted_id
    user_in_db = db.users.find_one({"_id": user_id})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user_in_db["email"]},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user_in_db["email"]},
        expires_delta=refresh_token_expires
    )

    return {
        "user": {
            "firstname": user_in_db["firstname"],
            "lastname": user_in_db["lastname"],
            "email": user_in_db["email"],
            "phone": user_in_db["phone"],  
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
