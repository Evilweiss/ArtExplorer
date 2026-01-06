import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PaintingAlias(Base):
    __tablename__ = "painting_aliases"
    __table_args__ = (
        UniqueConstraint("artist_slug", "painting_slug", name="uq_painting_alias_pair"),
        UniqueConstraint("combined_slug", name="uq_painting_alias_combined"),
        CheckConstraint(
            "(combined_slug IS NOT NULL AND artist_slug IS NULL AND painting_slug IS NULL) OR "
            "(combined_slug IS NULL AND artist_slug IS NOT NULL AND painting_slug IS NOT NULL)",
            name="ck_painting_alias_one_shape",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    painting_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("paintings.id"), nullable=False)
    artist_slug: Mapped[str | None] = mapped_column(String(200), nullable=True)
    painting_slug: Mapped[str | None] = mapped_column(String(200), nullable=True)
    combined_slug: Mapped[str | None] = mapped_column(String(400), nullable=True)

    painting = relationship("Painting", back_populates="aliases")
