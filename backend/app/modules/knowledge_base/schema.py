from pydantic import BaseModel
from typing import Optional


class KnowledgeChunkRequest(BaseModel):
    content: str
    source_type: str = "editor"


class KnowledgeChunkUpdate(BaseModel):
    content: Optional[str] = None


class KnowledgeChunkResponse(BaseModel):
    id: str
    restaurant_id: str
    content: str
    source_type: str
    created_at: str
