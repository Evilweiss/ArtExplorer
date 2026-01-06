"""store multiple genres per painting

Revision ID: 20240912_0002
Revises: 20240912_0001
Create Date: 2024-09-12 00:02:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20240912_0002"
down_revision = "20240912_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "paintings",
        "genre_name",
        existing_type=sa.Text(),
        type_=postgresql.ARRAY(sa.Text()),
        postgresql_using="string_to_array(genre_name, ',')",
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "paintings",
        "genre_name",
        existing_type=postgresql.ARRAY(sa.Text()),
        type_=sa.Text(),
        postgresql_using="array_to_string(genre_name, ',')",
        existing_nullable=True,
    )
