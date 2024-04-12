from fastapi import APIRouter, HTTPException, Depends, status
from .models import LoginModel, AuthResponseModel, RegisterUserModel, ForgotPasswordModel, \
    ForgotPasswordResponseModel, Role
from app.utils import send_email, render_template,create_access_token,create_refresh_token,generate_verification_code,store_verification_code,verify_password, get_password_hash
from app.db import db

router = APIRouter()



def authenticate_user(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None
    return user




@router.post("/login", response_model=AuthResponseModel, status_code=status.HTTP_200_OK)
async def login(cred: LoginModel):
    creds = dict(cred)
    user = authenticate_user(creds["email"], creds["password"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    try:


        access_token_data = {
            "id": str(user["_id"]),
            "email": user["email"],
            "phone": user["phone"]
        }
        access_token = create_access_token(
            data=access_token_data
        )

        refresh_token_data = {
            "id": str(user["_id"]),
            "email": user["email"],
            "phone": user["phone"]
        }
        refresh_token = create_refresh_token(
            data=refresh_token_data
        )

        return {
            "user": {
                "firstname": user["firstname"],
                "lastname": user["lastname"],
                "email": user["email"],
                "phone": user["phone"],
                "location": user["location"]
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Successfully Logged In"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/register", response_model=AuthResponseModel, status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUserModel):
    existing_user = db.users.find_one({"$or": [{"email": user.email}, {"phone": user.phone}]})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this email or phone already exists")

    user_data = user.dict()
    user_data["password"] = get_password_hash(user_data.pop("password"))
    user_data["role"] = Role.Admin
    user_data["emailVerified"] = False
    user_data["phoneVerified"] = False

    try:
        user_id = db.users.insert_one(user_data).inserted_id
        user_in_db = db.users.find_one({"_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")

    access_token_data = {
        "id": str(user_in_db["_id"]),
        "email": user_in_db["email"],
        "phone": user_in_db["phone"]
    }
    access_token = create_access_token(
        data=access_token_data,
    )

    refresh_token_data = {
        "id": str(user_in_db["_id"]),
        "email": user_in_db["email"],
        "phone": user_in_db["phone"]
    }
    refresh_token = create_refresh_token(
        data=refresh_token_data,
    )
    return {
        "user": {
            "firstname": user_in_db["firstname"],
            "lastname": user_in_db["lastname"],
            "email": user_in_db["email"],
            "phone": user_in_db["phone"],
            "location": user_in_db["location"]
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "An email has been sent to your account with a verification code. Please check your inbox."
    }


@router.post("/forgot-password", response_model=ForgotPasswordResponseModel, status_code=status.HTTP_200_OK)
async def forgot_password(cred: ForgotPasswordModel):
    creds = dict(cred)
    user = db.users.find_one({"email": creds["email"]})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Oops! We couldn't find a user with the specified email. Please double-check your email or consider signing up.")
    verification_code = generate_verification_code()

    try:
        await send_email([creds["email"]], "Forgot Password - Verification Code",
                         render_template("forgot-password.html", verification_code=verification_code))
        store_verification_code(creds["email"], verification_code)

        return {
            "message": "A verification code has been sent to your email. Please check your inbox.",
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
