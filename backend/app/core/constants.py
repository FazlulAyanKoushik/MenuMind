from enum import Enum


class UserRole(str, Enum):
    CONSUMER = "consumer"
    OWNER = "owner"
    ADMIN = "admin"


class RestaurantStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"


class PlanTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class ChatMessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class KnowledgeSourceType(str, Enum):
    EDITOR = "editor"
    UPLOAD = "upload"
    SCRAPE = "scrape"


PLAN_LIMITS = {
    PlanTier.FREE: {"monthly_chats": 50},
    PlanTier.PRO: {"monthly_chats": 1000},
    PlanTier.ENTERPRISE: {"monthly_chats": 999999},
}
