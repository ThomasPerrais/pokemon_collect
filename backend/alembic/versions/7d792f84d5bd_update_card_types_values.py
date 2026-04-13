"""update card types values

Revision ID: 7d792f84d5bd
Revises: c99dc1f08b86
Create Date: 2026-02-19 21:49:29.828072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d792f84d5bd'
down_revision: Union[str, Sequence[str], None] = 'c99dc1f08b86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE card
        MODIFY type ENUM(
            'pokemon',
            'object',
            'trainer',
            'stadium',
            'energy'
        ) NOT NULL
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
