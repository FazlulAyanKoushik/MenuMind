from pydantic import BaseModel
from typing import Optional
from app.core.constants import RestaurantStatus, PlanTier


class RestaurantResponse(BaseModel):
    id: str
    slug: str
    name: str
    logo_url: Optional[str] = None
    plan: PlanTier
    status: RestaurantStatus
    owner_id: str
    created_at: str


class UpdateRestaurantStatusRequest(BaseModel):
    status: RestaurantStatus


class UpdateRestaurantPlanRequest(BaseModel):
    plan: PlanTier
