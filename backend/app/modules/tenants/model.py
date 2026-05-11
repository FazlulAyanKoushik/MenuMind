import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.constants import RestaurantStatus, PlanTier
from app.common.utils.slug import generate_slug


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, default=lambda: generate_slug(12))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    plan: Mapped[PlanTier] = mapped_column(SAEnum(PlanTier), default=PlanTier.FREE)
    status: Mapped[RestaurantStatus] = mapped_column(SAEnum(RestaurantStatus), default=RestaurantStatus.PENDING)
    owner_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    owner = relationship("User")
    menu_items = relationship("MenuItem", back_populates="restaurant")
    knowledge_chunks = relationship("KnowledgeChunk", back_populates="restaurant")
    chat_sessions = relationship("ChatSession", back_populates="restaurant")
    qr_codes = relationship("QRCode", back_populates="restaurant")
    daily_stats = relationship("DailyStat", back_populates="restaurant")
