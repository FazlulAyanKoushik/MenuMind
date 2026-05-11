from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db_session, resolve_restaurant_id
from app.core.security import get_current_user_id
from app.modules.menus.schema import MenuItemRequest, MenuItemResponse, MenuItemUpdate
from app.modules.menus.model import MenuItem
from app.modules.menus.repository import (
    get_menu_items, get_menu_item_by_id, create_menu_item,
    update_menu_item, delete_menu_item,
)
from app.modules.menus.service import bulk_upload_menu

router = APIRouter(prefix="/owner", tags=["menu"])


@router.get("/menu")
async def list_menu(
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    items = await get_menu_items(db, restaurant_id)
    return {"success": True, "data": items}


@router.post("/menu", status_code=201)
async def create_item(
    request: MenuItemRequest,
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    item = MenuItem(restaurant_id=restaurant_id, **request.model_dump())
    item = await create_menu_item(db, item)
    return {"success": True, "data": item}


@router.put("/menu/{item_id}")
async def update_item(
    item_id: str,
    request: MenuItemUpdate,
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    item = await get_menu_item_by_id(db, item_id)
    if not item or item.restaurant_id != restaurant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    data = {k: v for k, v in request.model_dump().items() if v is not None}
    item = await update_menu_item(db, item, data)
    return {"success": True, "data": item}


@router.delete("/menu/{item_id}")
async def delete_item(
    item_id: str,
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    item = await get_menu_item_by_id(db, item_id)
    if not item or item.restaurant_id != restaurant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    await delete_menu_item(db, item_id)
    return {"success": True, "message": "Deleted"}


@router.post("/menu/bulk-upload")
async def bulk_upload(
    file: UploadFile = File(...),
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    if file.filename and not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported")
    content = await file.read()
    count = await bulk_upload_menu(db, restaurant_id, content, "csv")
    return {"success": True, "data": {"items_created": count}}
