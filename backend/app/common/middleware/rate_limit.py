from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import get_settings
from app.core.redis import redis_client

settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.endswith("/message"):
            client_ip = request.client.host if request.client else "unknown"
            key = f"rate_limit:chat:{client_ip}"
            count = await redis_client.incr(key)
            if count == 1:
                await redis_client.expire(key, settings.rate_limit_window_seconds)
            if count > settings.rate_limit_chat_messages:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please wait before sending another message.",
                )
        response = await call_next(request)
        return response
