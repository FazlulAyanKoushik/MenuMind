import uuid
from datetime import datetime, timezone, date
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DailyStat(Base):
    __tablename__ = "daily_stats"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(String, ForeignKey("restaurants.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    chat_count: Mapped[int] = mapped_column(Integer, default=0)
    token_count: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("restaurant_id", "date", name="uq_restaurant_date"),
    )

    restaurant = relationship("Restaurant", back_populates="daily_stats")
