from typing import Optional
from fastapi import Depends, HTTPException, status
from app.settings import authScheme
from app.db import db
from app.utils import decode_token
from app.api.auth import User
from bson import ObjectId




async def get_current_user(token: str = Depends(authScheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(dict(token)["credentials"])
        user_id = payload["id"]
        if user_id is None:
            raise credentials_exception
        user =db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        raise credentials_exception


class AuthRole:
    def __init__(self, roles: list[str]) -> None:
        self.roles = roles
    async def __call__(self, user: User= Depends(get_current_user)) -> bool:
        print("Being called")
        if(user["role"] not in self.roles):
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Sorry, your current role does not have access to this resource.'
                )
        return True
