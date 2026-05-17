"""Switch card-pokemon link to many-to-many

Revision ID: 4d3fa7e9b2c1
Revises: ec729a8c1801
Create Date: 2026-04-21 11:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d3fa7e9b2c1"
down_revision: Union[str, Sequence[str], None] = "ec729a8c1801"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "card_pokemon_association",
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["card_id"], ["card.id"]),
        sa.ForeignKeyConstraint(["pokemon_id"], ["pokemon.id"]),
        sa.PrimaryKeyConstraint("card_id", "pokemon_id"),
    )

    # Backfill the new association table from the legacy nullable FK.
    op.execute(
        sa.text(
            """
            INSERT INTO card_pokemon_association (card_id, pokemon_id)
            SELECT id, pokemon_id
            FROM card
            WHERE pokemon_id IS NOT NULL
            """
        )
    )

    bind = op.get_bind()
    inspector = sa.inspect(bind)
    foreign_keys = inspector.get_foreign_keys("card")
    for fk in foreign_keys:
        fk_name = fk.get("name")
        if fk.get("constrained_columns") == ["pokemon_id"] and isinstance(fk_name, str):
            op.drop_constraint(fk_name, "card", type_="foreignkey")
            break

    with op.batch_alter_table("card") as batch_op:
        batch_op.drop_column("pokemon_id")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("card") as batch_op:
        batch_op.add_column(sa.Column("pokemon_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_card_pokemon_id_pokemon", "pokemon", ["pokemon_id"], ["id"]
        )

    # If a card has multiple pokemons, pick the smallest id for legacy single FK.
    op.execute(
        sa.text(
            """
            UPDATE card
            SET pokemon_id = (
                SELECT MIN(rel.pokemon_id)
                FROM card_pokemon_association AS rel
                WHERE rel.card_id = card.id
            )
            WHERE EXISTS (
                SELECT 1
                FROM card_pokemon_association AS rel
                WHERE rel.card_id = card.id
            )
            """
        )
    )

    op.drop_table("card_pokemon_association")
