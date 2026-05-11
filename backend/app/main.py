from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import engine, Base
from app.common.middleware.tenant import TenantMiddleware
from app.common.middleware.rate_limit import RateLimitMiddleware
from app.common.exceptions.handlers import AppException, app_exception_handler, global_exception_handler
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.menus.router import router as menus_router
from app.modules.knowledge_base.router import router as kb_router
from app.modules.qr.router import router as qr_router
from app.modules.chats.router import router as chats_router
from app.modules.admin.router import router as admin_router
from app.modules.owner.router import router as owner_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TenantMiddleware)
app.add_middleware(RateLimitMiddleware)

app.exception_handler(AppException)(app_exception_handler)
app.exception_handler(Exception)(global_exception_handler)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(menus_router, prefix="/api/v1")
app.include_router(kb_router, prefix="/api/v1")
app.include_router(qr_router, prefix="/api/v1")
app.include_router(chats_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(owner_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/health")
async def health():
    return {"status": "healthy", "service": settings.app_name}
