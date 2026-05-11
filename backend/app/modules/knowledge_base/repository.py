from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.modules.knowledge_base.model import KnowledgeChunk


async def get_chunks(db: AsyncSession, restaurant_id: str, skip: int = 0, limit: int = 50) -> List[KnowledgeChunk]:
    result = await db.execute(
        select(KnowledgeChunk)
        .where(KnowledgeChunk.restaurant_id == restaurant_id)
        .offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_chunk_by_id(db: AsyncSession, chunk_id: str) -> Optional[KnowledgeChunk]:
    result = await db.execute(select(KnowledgeChunk).where(KnowledgeChunk.id == chunk_id))
    return result.scalar_one_or_none()


async def create_chunk(db: AsyncSession, chunk: KnowledgeChunk) -> KnowledgeChunk:
    db.add(chunk)
    await db.flush()
    return chunk


async def update_chunk(db: AsyncSession, chunk: KnowledgeChunk, data: dict) -> KnowledgeChunk:
    for key, value in data.items():
        setattr(chunk, key, value)
    await db.flush()
    return chunk


async def delete_chunk(db: AsyncSession, chunk_id: str) -> bool:
    result = await db.execute(delete(KnowledgeChunk).where(KnowledgeChunk.id == chunk_id))
    return result.rowcount > 0
