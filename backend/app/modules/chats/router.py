from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse
import json

from app.core.dependencies import get_db_session, resolve_restaurant_id
from app.core.security import get_current_user_id_optional
from app.modules.chats.model import ChatSession, ChatMessage
from app.modules.chats.schema import ChatRequest
from app.modules.chats.repository import (
    create_session, get_session_by_id, create_message, get_messages_by_session,
)
from app.core.constants import ChatMessageRole

router = APIRouter(prefix="/consumer", tags=["chat"])


@router.get("/chat/{restaurant_slug}/history")
async def get_chat_history(
    restaurant_slug: str,
    db: AsyncSession = Depends(get_db_session),
):
    from app.modules.tenants.repository import get_restaurant_by_slug
    restaurant = await get_restaurant_by_slug(db, restaurant_slug)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return {"success": True, "data": {"restaurant": {"name": restaurant.name, "slug": restaurant.slug}}}


@router.post("/chat/{restaurant_slug}/message")
async def send_message(
    restaurant_slug: str,
    request: ChatRequest,
    restaurant_id: str = Depends(resolve_restaurant_id),
    user_id: str = Depends(get_current_user_id_optional),
    db: AsyncSession = Depends(get_db_session),
):
    from app.modules.tenants.repository import get_restaurant_by_slug
    restaurant = await get_restaurant_by_slug(db, restaurant_slug)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    session_id = request.session_id
    if not session_id:
        session = ChatSession(restaurant_id=restaurant.id, user_id=user_id)
        session = await create_session(db, session)
        session_id = session.id
    else:
        session = await get_session_by_id(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

    msg = ChatMessage(session_id=session_id, role=ChatMessageRole.USER, content=request.message)
    await create_message(db, msg)

    async def event_generator():
        yield {"event": "message", "data": json.dumps({"delta": "Hello! I'm MenuMind, your AI food assistant. How can I help you today?", "done": False})}
        yield {"event": "message", "data": json.dumps({"done": True})}

    return EventSourceResponse(event_generator())
