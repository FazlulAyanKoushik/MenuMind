import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        restaurant_id = request.headers.get("X-Restaurant-ID")
        request.state.restaurant_id = restaurant_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
