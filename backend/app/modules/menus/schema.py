from pydantic import BaseModel
from typing import List, Optional


class MenuItemRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    cuisine_type: Optional[str] = None
    is_available: bool = True
    image_url: Optional[str] = None


class MenuItemResponse(BaseModel):
    id: str
    restaurant_id: str
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    ingredients: List[str]
    allergens: List[str]
    cuisine_type: Optional[str] = None
    is_available: bool
    image_url: Optional[str] = None
    embedding_status: str
    created_at: str
    updated_at: str


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    cuisine_type: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
