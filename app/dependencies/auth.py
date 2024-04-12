from typing import List
from fastapi import Depends, HTTPException, status
import jwt
from . import settings

ALGORITHM = "HS256"


async def get_current_user_roles(token: str = Depends(settings.oauth2_scheme)) -> List[str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        roles = payload.get("roles")
        if roles is None:
            raise credentials_exception
        return roles
    except JWTError:
        raise credentials_exception
