"""update card types values

Revision ID: 0397c9f20fc7
Revises: 7d792f84d5bd
Create Date: 2026-02-19 21:54:22.231258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0397c9f20fc7'
down_revision: Union[str, Sequence[str], None] = '7d792f84d5bd'
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
            'tool',
            'energy'
        ) NOT NULL
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
