from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis import get_redis
from redis.asyncio import Redis


async def resolve_restaurant_id(
    x_restaurant_id: str = Header(None, alias="X-Restaurant-ID"),
) -> str:
    if not x_restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Restaurant-ID header is required",
        )
    return x_restaurant_id


async def get_db_session() -> AsyncSession:
    async for session in get_db():
        yield session


async def get_redis_client() -> Redis:
    return await get_redis()
