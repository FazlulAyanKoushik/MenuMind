from pydantic import BaseModel
from typing import Optional, List


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    tokens_used: int
    created_at: str


class ChatSessionResponse(BaseModel):
    id: str
    restaurant_id: str
    user_id: Optional[str] = None
    started_at: str
    messages: List[ChatMessageResponse] = []


class ChatRequest(BaseModel):
    message: Optional[str] = None
    session_id: Optional[str] = None


class ChatHistoryResponse(BaseModel):
    sessions: List[ChatSessionResponse]
