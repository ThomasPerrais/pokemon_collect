"""trainer -> supporter

Revision ID: ec729a8c1801
Revises: 7906845c291d
Create Date: 2026-04-13 15:21:49.647682

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ec729a8c1801'
down_revision: Union[str, Sequence[str], None] = '7906845c291d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename card type trainer -> supporter in data, then tighten ENUM."""
    op.execute(
        """
        ALTER TABLE card
        MODIFY type ENUM(
            'pokemon',
            'object',
            'trainer',
            'supporter',
            'stadium',
            'energy',
            'tool'
        ) NOT NULL
        """
    )
    op.execute("UPDATE card SET type = 'supporter' WHERE type = 'trainer'")
    op.execute(
        """
        ALTER TABLE card
        MODIFY type ENUM(
            'pokemon',
            'object',
            'supporter',
            'stadium',
            'energy',
            'tool'
        ) NOT NULL
        """
    )


def downgrade() -> None:
    """Expand ENUM, map supporter -> trainer, restore previous ENUM."""
    op.execute(
        """
        ALTER TABLE card
        MODIFY type ENUM(
            'pokemon',
            'object',
            'trainer',
            'supporter',
            'stadium',
            'energy',
            'tool'
        ) NOT NULL
        """
    )
    op.execute("UPDATE card SET type = 'trainer' WHERE type = 'supporter'")
    op.execute(
        """
        ALTER TABLE card
        MODIFY type ENUM(
            'pokemon',
            'object',
            'trainer',
            'stadium',
            'energy',
            'tool'
        ) NOT NULL
        """
    )
