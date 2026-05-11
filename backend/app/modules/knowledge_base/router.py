from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session, resolve_restaurant_id
from app.modules.knowledge_base.schema import KnowledgeChunkRequest, KnowledgeChunkUpdate
from app.modules.knowledge_base.model import KnowledgeChunk
from app.modules.knowledge_base.repository import get_chunks, get_chunk_by_id, create_chunk, update_chunk, delete_chunk

router = APIRouter(prefix="/owner", tags=["knowledge-base"])


@router.get("/knowledge-base")
async def list_chunks(
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    chunks = await get_chunks(db, restaurant_id)
    return {"success": True, "data": chunks}


@router.post("/knowledge-base", status_code=201)
async def create_chunk_endpoint(
    request: KnowledgeChunkRequest,
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    chunk = KnowledgeChunk(restaurant_id=restaurant_id, **request.model_dump())
    chunk = await create_chunk(db, chunk)
    return {"success": True, "data": chunk}


@router.put("/knowledge-base/{chunk_id}")
async def update_chunk_endpoint(
    chunk_id: str,
    request: KnowledgeChunkUpdate,
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    chunk = await get_chunk_by_id(db, chunk_id)
    if not chunk or chunk.restaurant_id != restaurant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chunk not found")
    data = {k: v for k, v in request.model_dump().items() if v is not None}
    chunk = await update_chunk(db, chunk, data)
    return {"success": True, "data": chunk}


@router.delete("/knowledge-base/{chunk_id}")
async def delete_chunk_endpoint(
    chunk_id: str,
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    chunk = await get_chunk_by_id(db, chunk_id)
    if not chunk or chunk.restaurant_id != restaurant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chunk not found")
    await delete_chunk(db, chunk_id)
    return {"success": True, "message": "Deleted"}
