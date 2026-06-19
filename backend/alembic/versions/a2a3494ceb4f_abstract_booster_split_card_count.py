"""abstract booster split card count

Revision ID: a2a3494ceb4f
Revises: 4d3fa7e9b2c1
Create Date: 2026-06-16 19:38:26.214761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a2a3494ceb4f'
down_revision: Union[str, Sequence[str], None] = '4d3fa7e9b2c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("abstract_booster")}

    if "set_card_count" not in existing_columns:
        op.add_column(
            "abstract_booster",
            sa.Column("set_card_count", sa.Integer(), nullable=True),
        )
    if "energy_card_count" not in existing_columns:
        op.add_column(
            "abstract_booster",
            sa.Column("energy_card_count", sa.Integer(), nullable=True),
        )
    if "special_card_count" not in existing_columns:
        op.add_column(
            "abstract_booster",
            sa.Column("special_card_count", sa.Integer(), nullable=True),
        )

    op.execute(
        """
        UPDATE abstract_booster
        SET set_card_count = card_count,
            energy_card_count = 0,
            special_card_count = 0
        WHERE set_card_count IS NULL
           OR energy_card_count IS NULL
           OR special_card_count IS NULL
        """
    )

    op.alter_column(
        "abstract_booster",
        "set_card_count",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "abstract_booster",
        "energy_card_count",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "abstract_booster",
        "special_card_count",
        existing_type=sa.Integer(),
        nullable=False,
    )

    existing_constraints = {
        constraint["name"]
        for constraint in inspector.get_unique_constraints("abstract_booster")
    }
    if "uq_set_card_count_booster" not in existing_constraints:
        op.create_unique_constraint(
            "uq_set_card_count_booster",
            "abstract_booster",
            ["set_id", "set_card_count"],
        )

    if "uq_card_number_booster" in existing_constraints:
        op.drop_constraint(
            "uq_card_number_booster", "abstract_booster", type_="unique"
        )

    if "card_count" in existing_columns:
        op.drop_column("abstract_booster", "card_count")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("abstract_booster")}

    if "card_count" not in existing_columns:
        op.add_column(
            "abstract_booster",
            sa.Column("card_count", mysql.INTEGER(), autoincrement=False, nullable=True),
        )

    op.execute(
        """
        UPDATE abstract_booster
        SET card_count = set_card_count
        WHERE card_count IS NULL
        """
    )
    op.alter_column(
        "abstract_booster",
        "card_count",
        existing_type=mysql.INTEGER(),
        nullable=False,
    )

    existing_constraints = {
        constraint["name"]
        for constraint in inspector.get_unique_constraints("abstract_booster")
    }
    if "uq_card_number_booster" not in existing_constraints:
        op.create_unique_constraint(
            "uq_card_number_booster",
            "abstract_booster",
            ["set_id", "card_count"],
        )

    if "uq_set_card_count_booster" in existing_constraints:
        op.drop_constraint(
            "uq_set_card_count_booster", "abstract_booster", type_="unique"
        )

    if "special_card_count" in existing_columns:
        op.drop_column("abstract_booster", "special_card_count")
    if "energy_card_count" in existing_columns:
        op.drop_column("abstract_booster", "energy_card_count")
    if "set_card_count" in existing_columns:
        op.drop_column("abstract_booster", "set_card_count")
