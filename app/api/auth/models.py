from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class Role(str, Enum):
    User = "User"
    Admin = "Admin"


class User(BaseModel):
    firstname: str
    lastname: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    location: str
    role: Role
    emailVerified: Optional[bool] = False
    phoneVerified: Optional[bool] = False


class RegisterUserModel(BaseModel):
    firstname: str
    lastname: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    location: str


class UserInDB(User):
    id: str


class EmailCode(BaseModel):
    email: EmailStr
    code: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordModel(BaseModel):
    email: EmailStr


class ForgotPasswordResponseModel(BaseModel):
    message: str


class PartialUser(BaseModel):
    firstname: str
    lastname: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: str
    role: Role


class AuthResponseModel(BaseModel):
    access_token: str
    refresh_token: str
    message: Optional[str] = None
    user: PartialUser
