from fastapi import APIRouter, HTTPException, Depends, status
from .models import LoginModel, AuthResponseModel, RegisterUserModel, ForgotPasswordModel, \
    VerifyAccountModel,ResetPasswordModel,AuthResponseModel2
from app.api.users.models import Role
from app.utils import send_email, render_template,create_access_token,create_refresh_token,generate_verification_code,store_verification_code,verify_password, get_password_hash,verify_verification_code,delete_verification_code,decode_refresh_token
from app.db import db
from app.settings import authScheme
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
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"],
                "role":user["role"]
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Successfully Logged In"
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/register", response_model=AuthResponseModel, status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUserModel):
    if user.email and len(user.email) > 0:
        existing_user = db.users.find_one({"email": user.email})
    elif user.phone and len(user.phone) > 0:
        existing_user = db.users.find_one({"phone": user.phone})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this email or phone already exists")
    user_data = user.dict()
    user_data["password"] = get_password_hash(user_data.pop("password"))
    user_data["role"] = Role.User
    user_data["emailVerified"] = False
    user_data["phoneVerified"] = False
    try:
        user_id = db.users.insert_one(user_data).inserted_id
        user_in_db = db.users.find_one({"_id": user_id})
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
            "name": user_in_db["name"],
            "email": user_in_db["email"],
            "phone": user_in_db["phone"],
            "role":user_in_db["role"]
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "Account created"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")


@router.post("/forgot-password", response_model=AuthResponseModel2, status_code=status.HTTP_200_OK)
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



@router.post("/verify-account", response_model=AuthResponseModel2, status_code=status.HTTP_200_OK, responses={
    404: {"description": "User with the specified email not found"},
    401: {"description": "Invalid verification code"},
    500: {"description": "Internal server error"}
})
async def verify_account(cred: VerifyAccountModel):
    try:
        user = db.users.find_one({"email": cred.email})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with the specified email not found. Please double-check your email or consider signing up.")
        if not verify_verification_code(cred.email, cred.code):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid verification code. Please double-check your email.")
        db.users.update_one({"email": user["email"]}, {"$set": {"emailVerified": True}})
        return {"message": "Account verified successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error. Please try again later.")
        
        
        

@router.post("/reset-password", response_model=AuthResponseModel2, status_code=status.HTTP_200_OK, responses={
    404: {"description": "User with the specified email not found"},
    401: {"description": "Invalid verification code"},
    500: {"description": "Internal server error"}
})
async def reset_password(cred: ResetPasswordModel):
    try:
        user = db.users.find_one({"email": cred.email})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with the specified email not found. Please double-check your email or consider signing up.")
        if not verify_verification_code(cred.email, cred.code):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid verification code. Please double-check your email.")
        db.users.update_one({"email": cred.email}, {"$set": {"password": get_password_hash(cred.password)}})
        delete_verification_code(cred.email)
        return {"message": "Password reset successful. You can now log in with your new password."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error. Please try again later.")
        
        
        

@router.post("/verify-token", response_model=AuthResponseModel2, status_code=status.HTTP_200_OK, responses={
    401: {"description": "Invalid Token"},
    500: {"description": "Internal server error"}
})
async def verify_token(token: str = Depends(authScheme) ):
    try:
        user = decode_refresh_token(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid refresh token. Please login again to get a new refresh token.")
        new_access_token = create_access_token(user)  
        new_refresh_token = create_refresh_token(user)  
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error. Please try again later.")