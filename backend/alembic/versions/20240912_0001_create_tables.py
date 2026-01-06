"""create paintings and facts tables

Revision ID: 20240912_0001
Revises: 
Create Date: 2024-09-12 00:01:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20240912_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "paintings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("artist_name", sa.Text(), nullable=False),
        sa.Column("artist_slug", sa.String(length=200), nullable=False),
        sa.Column("painting_slug", sa.String(length=200), nullable=False),
        sa.Column("museum_name", sa.Text(), nullable=True),
        sa.Column("genre_name", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("license_name", sa.Text(), nullable=True),
        sa.Column("license_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("artist_slug", "painting_slug", name="uq_artist_painting_slug"),
    )

    op.create_table(
        "facts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("painting_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("paintings.id"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description_md", sa.Text(), nullable=False),
        sa.Column("geometry_type", sa.Text(), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("w", sa.Float(), nullable=False),
        sa.Column("h", sa.Float(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("x >= 0 AND x <= 1", name="ck_facts_x"),
        sa.CheckConstraint("y >= 0 AND y <= 1", name="ck_facts_y"),
        sa.CheckConstraint("w > 0 AND w <= 1", name="ck_facts_w"),
        sa.CheckConstraint("h > 0 AND h <= 1", name="ck_facts_h"),
    )
    op.create_index("ix_facts_painting_id", "facts", ["painting_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_facts_painting_id", table_name="facts")
    op.drop_table("facts")
    op.drop_table("paintings")
