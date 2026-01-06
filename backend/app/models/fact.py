import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Fact(Base):
    __tablename__ = "facts"
    __table_args__ = (
        CheckConstraint("x >= 0 AND x <= 1", name="ck_facts_x"),
        CheckConstraint("y >= 0 AND y <= 1", name="ck_facts_y"),
        CheckConstraint("w > 0 AND w <= 1", name="ck_facts_w"),
        CheckConstraint("h > 0 AND h <= 1", name="ck_facts_h"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    painting_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("paintings.id"), index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description_md: Mapped[str] = mapped_column(Text, nullable=False)
    geometry_type: Mapped[str] = mapped_column(Text, nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    w: Mapped[float] = mapped_column(Float, nullable=False)
    h: Mapped[float] = mapped_column(Float, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    painting = relationship("Painting", back_populates="facts")
