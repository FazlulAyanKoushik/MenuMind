from pydantic import BaseModel
from typing import List, Optional


class ProfileRequest(BaseModel):
    preferences: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    region: Optional[str] = None


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    preferences: List[str]
    allergies: List[str]
    region: Optional[str] = None
    updated_at: str
