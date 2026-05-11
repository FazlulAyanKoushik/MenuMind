from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.core.security import decode_token
from app.modules.auth.repository import get_user_by_id
from app.core.constants import UserRole

security = HTTPBearer()


async def require_role(role: UserRole):
    async def _check(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db_session),
    ):
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        user = await get_user_by_id(db, user_id)
        if not user or user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return _check


require_admin = require_role(UserRole.ADMIN)
require_owner = require_role(UserRole.OWNER)
require_consumer = require_role(UserRole.CONSUMER)
