from pydantic import BaseModel, EmailStr
from typing import Optional
from app.api.users.models import Role




class RegisterUserModel(BaseModel):
    firstName:str
    lastName:str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str



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
    
    
class ResetPasswordModel(BaseModel):
    email:EmailStr
    code:str
    password:str
    
    
class VerifyAccountModel(BaseModel):
    email:EmailStr
    code:str


class PartialUser(BaseModel):
    firstName:str
    lastName:str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Role


class AuthResponseModel(BaseModel):
    access_token: str
    refresh_token: str
    message: Optional[str] = None
    user: PartialUser
    
class AuthResponseModel2(BaseModel):
    message: str
