from app.core.config import get_settings
from app.core.constants import PLAN_LIMITS


async def check_token_budget(restaurant_id: str, plan: str, current_monthly_tokens: int) -> dict:
    settings = get_settings()
    plan_key = plan.lower()
    limits = PLAN_LIMITS.get(plan_key)

    if not limits:
        return {"within_budget": True, "warning": None}

    monthly_chats = limits.get("monthly_chats", 999999)
    usage_pct = (current_monthly_tokens / (monthly_chats * 500)) * 100 if monthly_chats > 0 else 0

    warning = None
    if usage_pct > 80:
        warning = f"Token usage at {usage_pct:.0f}% of monthly plan limit."

    return {
        "within_budget": usage_pct < 100,
        "warning": warning,
        "usage_pct": usage_pct,
    }
