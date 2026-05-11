import io
import qrcode
import base64
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from qrcode.image.svg import SvgImage

from app.core.dependencies import get_db_session, resolve_restaurant_id
from app.modules.qr.model import QRCode
from app.modules.tenants.repository import get_restaurant_by_id

router = APIRouter(prefix="/owner", tags=["qr-code"])


@router.get("/qr-code")
async def get_qr_code(
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    restaurant = await get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    chat_url = f"/chat/{restaurant.slug}"

    qr = qrcode.make(chat_url)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "success": True,
        "data": {
            "slug": restaurant.slug,
            "chat_url": chat_url,
            "qr_png_base64": img_b64,
        },
    }


@router.post("/qr-code/regenerate")
async def regenerate_qr(
    restaurant_id: str = Depends(resolve_restaurant_id),
    db: AsyncSession = Depends(get_db_session),
):
    from app.common.utils.slug import generate_slug
    restaurant = await get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    restaurant.slug = generate_slug(12)
    await db.flush()

    chat_url = f"/chat/{restaurant.slug}"
    qr = qrcode.make(chat_url)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "success": True,
        "data": {
            "slug": restaurant.slug,
            "chat_url": chat_url,
            "qr_png_base64": img_b64,
        },
    }
