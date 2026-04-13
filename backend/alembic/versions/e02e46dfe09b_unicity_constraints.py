"""unicity constraints

Revision ID: e02e46dfe09b
Revises: 0397c9f20fc7
Create Date: 2026-02-19 22:05:16.669533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e02e46dfe09b'
down_revision: Union[str, Sequence[str], None] = '0397c9f20fc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        "uq_card_set_number",
        "card",
        ["set_id", "number"]
    )
    op.create_unique_constraint(
        "uq_set_abbreviation",
        "set",
        ["abbreviation"]
    )
    op.create_unique_constraint(
        "uq_pokemon_name",
        "pokemon",
        ["name"]
    )
    op.create_unique_constraint(
        "uq_era_name",
        "era",
        ["name"]
    )
    op.create_unique_constraint(
        "uq_set_name",
        "set",
        ["name"]
    )


def downgrade():
    op.drop_constraint("uq_card_set_number", "card", type_="unique")
    op.drop_constraint("uq_set_abbreviation", "set", type_="unique")
    op.drop_constraint("uq_pokemon_name", "pokemon", type_="unique")
    op.drop_constraint("uq_era_name", "era", type_="unique")
    op.drop_constraint("uq_set_name", "set", type_="unique")
