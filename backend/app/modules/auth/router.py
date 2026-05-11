from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.modules.auth.schema import RegisterRequest, LoginRequest, RefreshRequest, TokenResponse
from app.modules.auth.service import register_user, login_user, refresh_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db_session)):
    result = await register_user(db, request)
    return {"success": True, "data": result}


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    result = await login_user(db, request.email, request.password)
    return {"success": True, "data": result}


@router.post("/refresh")
async def refresh(request: RefreshRequest, db: AsyncSession = Depends(get_db_session)):
    result = await refresh_access_token(db, request.refresh_token)
    return {"success": True, "data": result}


@router.post("/logout")
async def logout():
    return {"success": True, "message": "Logged out"}
