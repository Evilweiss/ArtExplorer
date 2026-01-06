import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Painting(Base):
    __tablename__ = "paintings"
    __table_args__ = (UniqueConstraint("artist_slug", "painting_slug", name="uq_artist_painting_slug"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    artist_name: Mapped[str] = mapped_column(Text, nullable=False)
    artist_slug: Mapped[str] = mapped_column(String(200), nullable=False)
    painting_slug: Mapped[str] = mapped_column(String(200), nullable=False)
    museum_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    genre_name: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    license_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    license_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    facts = relationship("Fact", back_populates="painting", cascade="all, delete-orphan")
