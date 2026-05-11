from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.core.security import get_current_user_id
from app.modules.users.schema import ProfileRequest, ProfileResponse
from app.modules.users.repository import upsert_profile, get_profile_by_user_id

router = APIRouter(prefix="/consumer", tags=["consumer"])


@router.get("/profile")
async def get_profile(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    profile = await get_profile_by_user_id(db, user_id)
    if not profile:
        return {"success": True, "data": None}
    return {
        "success": True,
        "data": ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            preferences=profile.preferences or [],
            allergies=profile.allergies or [],
            region=profile.region,
            updated_at=str(profile.updated_at),
        ),
    }


@router.put("/profile")
async def update_profile(
    request: ProfileRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    data = {k: v for k, v in request.model_dump().items() if v is not None}
    profile = await upsert_profile(db, user_id, data)
    return {
        "success": True,
        "data": ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            preferences=profile.preferences or [],
            allergies=profile.allergies or [],
            region=profile.region,
            updated_at=str(profile.updated_at),
        ),
    }
