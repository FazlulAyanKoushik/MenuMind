from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.dependencies import get_db_session, resolve_restaurant_id
from app.modules.chats.model import ChatSession, ChatMessage
from app.modules.menus.model import MenuItem

router = APIRouter(prefix="/owner", tags=["owner"])


@router.get("/dashboard")
async def owner_dashboard(
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    from datetime import date, timedelta
    today = date.today()

    session_count = await db.execute(
        select(func.count(ChatSession.id))
        .where(ChatSession.restaurant_id == restaurant_id)
    )
    total_sessions = session_count.scalar() or 0

    today_sessions = await db.execute(
        select(func.count(ChatSession.id))
        .where(ChatSession.restaurant_id == restaurant_id)
        .where(func.date(ChatSession.started_at) == today)
    )
    today_count = today_sessions.scalar() or 0

    items_count = await db.execute(
        select(func.count(MenuItem.id))
        .where(MenuItem.restaurant_id == restaurant_id)
    )
    menu_count = items_count.scalar() or 0

    return {
        "success": True,
        "data": {
            "total_sessions": total_sessions,
            "today_sessions": today_count,
            "menu_items": menu_count,
            "embedding_status": "active",
        },
    }


@router.get("/analytics")
async def owner_analytics(
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    from app.modules.admin.model import DailyStat
    from datetime import date, timedelta

    seven_days_ago = date.today() - timedelta(days=7)
    stats = await db.execute(
        select(DailyStat)
        .where(DailyStat.restaurant_id == restaurant_id)
        .where(DailyStat.date >= seven_days_ago)
    )
    daily_stats = stats.scalars().all()

    return {
        "success": True,
        "data": {
            "daily_stats": [
                {"date": str(s.date), "chats": s.chat_count, "tokens": s.token_count}
                for s in daily_stats
            ]
        },
    }
