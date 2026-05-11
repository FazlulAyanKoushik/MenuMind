from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.modules.tenants.repository import get_restaurants, get_restaurant_by_id, update_restaurant_status, update_restaurant_plan
from app.modules.auth.repository import get_user_by_id, update_user_role
from app.modules.tenants.schema import UpdateRestaurantStatusRequest, UpdateRestaurantPlanRequest
from app.core.constants import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/restaurants")
async def list_restaurants(
    db: AsyncSession = Depends(get_db_session),
):
    restaurants = await get_restaurants(db)
    return {"success": True, "data": restaurants}


@router.put("/restaurants/{restaurant_id}/status")
async def change_restaurant_status(
    restaurant_id: str,
    request: UpdateRestaurantStatusRequest,
    db: AsyncSession = Depends(get_db_session),
):
    restaurant = await update_restaurant_status(db, restaurant_id, request.status)
    if not restaurant:
        return {"success": False, "message": "Restaurant not found"}
    return {"success": True, "data": restaurant}


@router.put("/restaurants/{restaurant_id}/plan")
async def change_restaurant_plan(
    restaurant_id: str,
    request: UpdateRestaurantPlanRequest,
    db: AsyncSession = Depends(get_db_session),
):
    restaurant = await update_restaurant_plan(db, restaurant_id, request.plan)
    if not restaurant:
        return {"success": False, "message": "Restaurant not found"}
    return {"success": True, "data": restaurant}


@router.get("/users")
async def list_users(
    db: AsyncSession = Depends(get_db_session),
):
    from app.modules.auth.model import User
    from sqlalchemy import select
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"success": True, "data": users}


@router.put("/users/{user_id}/role")
async def change_user_role(
    user_id: str,
    role: UserRole,
    db: AsyncSession = Depends(get_db_session),
):
    user = await update_user_role(db, user_id, role)
    if not user:
        return {"success": False, "message": "User not found"}
    return {"success": True, "data": user}


@router.get("/analytics/platform")
async def platform_analytics(
    db: AsyncSession = Depends(get_db_session),
):
    from app.modules.tenants.repository import count_restaurants
    from app.modules.chats.model import ChatSession
    from app.modules.admin.model import DailyStat
    from sqlalchemy import select, func

    total_restaurants = await count_restaurants(db)
    result = await db.execute(select(func.count(ChatSession.id)))
    total_chats = result.scalar() or 0
    result = await db.execute(select(func.coalesce(func.sum(DailyStat.token_count), 0)))
    total_tokens = result.scalar() or 0

    return {
        "success": True,
        "data": {
            "total_restaurants": total_restaurants,
            "total_chats": total_chats,
            "total_tokens_used": total_tokens,
        },
    }
