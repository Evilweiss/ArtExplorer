"""add painting aliases table

Revision ID: 20240912_0003
Revises: 20240912_0002
Create Date: 2024-09-12 00:03:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20240912_0003"
down_revision = "20240912_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "painting_aliases",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("painting_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("paintings.id"), nullable=False),
        sa.Column("artist_slug", sa.String(length=200), nullable=True),
        sa.Column("painting_slug", sa.String(length=200), nullable=True),
        sa.Column("combined_slug", sa.String(length=400), nullable=True),
        sa.CheckConstraint(
            "(combined_slug IS NOT NULL AND artist_slug IS NULL AND painting_slug IS NULL) OR "
            "(combined_slug IS NULL AND artist_slug IS NOT NULL AND painting_slug IS NOT NULL)",
            name="ck_painting_alias_one_shape",
        ),
        sa.UniqueConstraint("artist_slug", "painting_slug", name="uq_painting_alias_pair"),
        sa.UniqueConstraint("combined_slug", name="uq_painting_alias_combined"),
    )
    op.create_index("ix_painting_aliases_painting_id", "painting_aliases", ["painting_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_painting_aliases_painting_id", table_name="painting_aliases")
    op.drop_table("painting_aliases")
