import csv
import io
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.menus.model import MenuItem
from app.modules.menus.repository import bulk_create_menu_items


async def parse_csv_menu(file_content: bytes, restaurant_id: str) -> List[MenuItem]:
    text = file_content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    items = []
    for row in reader:
        item = MenuItem(
            restaurant_id=restaurant_id,
            name=row.get("name", "").strip(),
            description=row.get("description", "").strip(),
            price=float(row.get("price", 0)),
            category=row.get("category", "").strip(),
            ingredients=[x.strip() for x in row.get("ingredients", "").split(",") if x.strip()],
            allergens=[x.strip() for x in row.get("allergens", "").split(",") if x.strip()],
            cuisine_type=row.get("cuisine_type", "").strip(),
            is_available=row.get("is_available", "true").lower() == "true",
        )
        items.append(item)
    return items


async def bulk_upload_menu(db: AsyncSession, restaurant_id: str, file_content: bytes, file_type: str) -> int:
    if file_type == "csv":
        items = await parse_csv_menu(file_content, restaurant_id)
    else:
        raise ValueError("Unsupported file type")

    await bulk_create_menu_items(db, items)
    return len(items)
