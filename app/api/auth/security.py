from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from typing import Optional

from decouple import config

SECRET_KEY = config("SECRET_KEY")
REFRESH_SECRET_KEY = config("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def token_header(x_token: str = Header(...)):
    if x_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Token header is missing")
    return x_token


def get_current_user(token: str = Depends(token_header)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
