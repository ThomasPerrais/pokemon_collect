"""new rarities

Revision ID: 82ed957acaef
Revises: e02e46dfe09b
Create Date: 2026-04-06 18:58:36.038233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82ed957acaef'
down_revision: Union[str, Sequence[str], None] = 'e02e46dfe09b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE card
        MODIFY rarity ENUM(
            'common',
            'uncommon',
            'rare',
            'holographic',
            'double_rare',
            'alternative',
            'ultra_rare',
            'secret',
            'alt_special_rare',
            'hyper_rare',
            'mega_hyper_rare',
            'special_rare',
            'shiny',
            'rainbow_rare',
            'gold_rare',
            'double_shiny',
            'promo',
            'tech'
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
