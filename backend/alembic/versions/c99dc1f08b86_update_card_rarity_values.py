"""update card rarity values

Revision ID: c99dc1f08b86
Revises: 76b89d562ee9
Create Date: 2026-02-19 21:43:09.743664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c99dc1f08b86'
down_revision: Union[str, Sequence[str], None] = '76b89d562ee9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
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
            'double_shiny',
            'promo',
            'tech'
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
