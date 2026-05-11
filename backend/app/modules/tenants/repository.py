from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.modules.tenants.model import Restaurant
from app.core.constants import RestaurantStatus


async def get_restaurant_by_id(db: AsyncSession, restaurant_id: str) -> Optional[Restaurant]:
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalar_one_or_none()


async def get_restaurant_by_slug(db: AsyncSession, slug: str) -> Optional[Restaurant]:
    result = await db.execute(select(Restaurant).where(Restaurant.slug == slug))
    return result.scalar_one_or_none()


async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Restaurant]:
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()


async def create_restaurant(db: AsyncSession, restaurant: Restaurant) -> Restaurant:
    db.add(restaurant)
    await db.flush()
    return restaurant


async def update_restaurant_status(db: AsyncSession, restaurant_id: str, status: RestaurantStatus) -> Optional[Restaurant]:
    restaurant = await get_restaurant_by_id(db, restaurant_id)
    if restaurant:
        restaurant.status = status
        await db.flush()
    return restaurant


async def update_restaurant_plan(db: AsyncSession, restaurant_id: str, plan: str) -> Optional[Restaurant]:
    restaurant = await get_restaurant_by_id(db, restaurant_id)
    if restaurant:
        restaurant.plan = plan
        await db.flush()
    return restaurant


async def delete_restaurant(db: AsyncSession, restaurant_id: str) -> bool:
    result = await db.execute(delete(Restaurant).where(Restaurant.id == restaurant_id))
    return result.rowcount > 0


async def count_restaurants(db: AsyncSession) -> int:
    result = await db.execute(select(Restaurant))
    return len(result.scalars().all())
