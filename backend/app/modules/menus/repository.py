from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.modules.menus.model import MenuItem


async def get_menu_items(db: AsyncSession, restaurant_id: str, skip: int = 0, limit: int = 50) -> List[MenuItem]:
    result = await db.execute(
        select(MenuItem)
        .where(MenuItem.restaurant_id == restaurant_id)
        .offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_menu_item_by_id(db: AsyncSession, item_id: str) -> Optional[MenuItem]:
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    return result.scalar_one_or_none()


async def create_menu_item(db: AsyncSession, item: MenuItem) -> MenuItem:
    db.add(item)
    await db.flush()
    return item


async def update_menu_item(db: AsyncSession, item: MenuItem, data: dict) -> MenuItem:
    for key, value in data.items():
        setattr(item, key, value)
    await db.flush()
    return item


async def delete_menu_item(db: AsyncSession, item_id: str) -> bool:
    result = await db.execute(delete(MenuItem).where(MenuItem.id == item_id))
    return result.rowcount > 0


async def bulk_create_menu_items(db: AsyncSession, items: List[MenuItem]) -> List[MenuItem]:
    db.add_all(items)
    await db.flush()
    return items
