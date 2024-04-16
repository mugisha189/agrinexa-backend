from pydantic import BaseModel,EmailStr
from typing import Optional,List
from enum import Enum



class Role(str, Enum):
    User = "User"
    Admin = "Admin"


class User(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Role
    emailVerified: Optional[bool] = False
    phoneVerified: Optional[bool] = False
