from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.modules.users.model import ConsumerProfile


async def get_profile_by_user_id(db: AsyncSession, user_id: str) -> Optional[ConsumerProfile]:
    result = await db.execute(select(ConsumerProfile).where(ConsumerProfile.user_id == user_id))
    return result.scalar_one_or_none()


async def upsert_profile(db: AsyncSession, user_id: str, profile_data: dict) -> ConsumerProfile:
    profile = await get_profile_by_user_id(db, user_id)
    if profile:
        for key, value in profile_data.items():
            setattr(profile, key, value)
    else:
        profile = ConsumerProfile(user_id=user_id, **profile_data)
        db.add(profile)
    await db.flush()
    return profile
