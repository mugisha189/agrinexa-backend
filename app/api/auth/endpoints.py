# app/api/auth/endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from app.api.auth.models import User, UserInDB, EmailCode
from app.api.auth.security import verify_password, get_password_hash
from app.db import db

router = APIRouter()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(username: str, password: str):
    user = db.users.find_one({"username": username})
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user


@router.post("/register", response_model=User)
async def register_user(user: User):
    user_data = user.dict()
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    user_id = db.users.insert_one(user_data).inserted_id
    user_in_db = db.users.find_one({"_id": user_id})
    return UserInDB(**user_in_db)


@router.post("/forgot-password")
async def forgot_password(email: str):
    user = db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    code = generate_code()  
    send_code_to_email(email, code)  
    db.codes.insert_one({"email": email, "code": code})
    return {"message": "Code sent successfully"}


@router.post("/verify")
async def verify_user(email_code: EmailCode):
    stored_code = db.codes.find_one({"email": email_code.email})
    if not stored_code or stored_code["code"] != email_code.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    db.users.update_one({"email": email_code.email}, {"$set": {"verified": True}})
    db.codes.delete_one({"email": email_code.email})
    return {"message": "User verified successfully"}


@router.post("/reset-password")
async def reset_password(email_code: EmailCode, new_password: str):
    stored_code = db.codes.find_one({"email": email_code.email})
    if not stored_code or stored_code["code"] != email_code.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # If code is valid, update user's password
    hashed_password = get_password_hash(new_password)
    db.users.update_one({"email": email_code.email}, {"$set": {"hashed_password": hashed_password}})
    # Remove code from the database after password reset
    db.codes.delete_one({"email": email_code.email})
    return {"message": "Password reset successfully"}
