from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.modules.auth.model import User
from app.modules.auth.schema import RegisterRequest
from app.modules.auth.repository import get_user_by_email, create_user
from app.modules.tenants.repository import create_restaurant
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.constants import UserRole
from app.modules.tenants.model import Restaurant


async def register_user(db: AsyncSession, request: RegisterRequest) -> dict:
    existing = await get_user_by_email(db, request.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
        role=request.role,
    )
    user = await create_user(db, user)

    restaurant = None
    if request.role == UserRole.OWNER:
        if not request.restaurant_name:
            raise HTTPException(status_code=400, detail="Restaurant name required for owner registration")
        restaurant = await create_restaurant(db, Restaurant(name=request.restaurant_name, owner_id=user.id))

    tokens = {
        "access_token": create_access_token({"sub": user.id, "role": user.role.value}),
        "refresh_token": create_refresh_token({"sub": user.id}),
    }
    return {
        "user": {"id": user.id, "email": user.email, "role": user.role.value},
        "restaurant": {"id": restaurant.id, "name": restaurant.name} if restaurant else None,
        **tokens,
    }


async def login_user(db: AsyncSession, email: str, password: str) -> dict:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return {
        "access_token": create_access_token({"sub": user.id, "role": user.role.value}),
        "refresh_token": create_refresh_token({"sub": user.id}),
        "user": {"id": user.id, "email": user.email, "role": user.role.value},
    }


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict:
    from app.core.security import decode_token
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user = await get_user_by_email(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {
        "access_token": create_access_token({"sub": user.id, "role": user.role.value}),
    }
