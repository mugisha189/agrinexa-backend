# app/api/auth/models.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    hashed_password: str

class UserInDB(User):
    id: str


class EmailCode(BaseModel):
    email: str
    code: str