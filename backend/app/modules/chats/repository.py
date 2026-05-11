from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.modules.chats.model import ChatSession, ChatMessage


async def create_session(db: AsyncSession, session: ChatSession) -> ChatSession:
    db.add(session)
    await db.flush()
    return session


async def get_session_by_id(db: AsyncSession, session_id: str) -> Optional[ChatSession]:
    result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    return result.scalar_one_or_none()


async def get_sessions_by_restaurant(db: AsyncSession, restaurant_id: str, skip: int = 0, limit: int = 20) -> List[ChatSession]:
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.restaurant_id == restaurant_id)
        .order_by(desc(ChatSession.started_at))
        .offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_sessions_by_user(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 20) -> List[ChatSession]:
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(desc(ChatSession.started_at))
        .offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_message(db: AsyncSession, message: ChatMessage) -> ChatMessage:
    db.add(message)
    await db.flush()
    return message


async def get_messages_by_session(db: AsyncSession, session_id: str, limit: int = 50) -> List[ChatMessage]:
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .limit(limit)
    )
    return result.scalars().all()
