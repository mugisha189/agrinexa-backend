from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    firstname: str
    lastname: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    location: str
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


class PartialUser(BaseModel):
    firstname: str
    lastname: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: str


class AuthResponseModel(BaseModel):
    access_token: str
    refresh_token: str
    message: Optional[str] = None
    user: PartialUser
