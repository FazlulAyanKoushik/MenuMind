from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.model import User


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.flush()
    return user


async def update_user_role(db: AsyncSession, user_id: str, role: UserRole) -> User | None:
    user = await get_user_by_id(db, user_id)
    if user:
        user.role = role
        await db.flush()
    return user
