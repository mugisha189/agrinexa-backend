from typing import List, Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
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


def has_role(*allowed_roles: str):
    async def _has_role(roles: List[str] = Depends(get_current_user_roles)):
        if not allowed_roles:
            return  # No roles specified means any role is allowed
        for role in allowed_roles:
            if role in roles:
                return  # User has at least one allowed role
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Required roles: " + ", ".join(allowed_roles),
        )

    return _has_role
