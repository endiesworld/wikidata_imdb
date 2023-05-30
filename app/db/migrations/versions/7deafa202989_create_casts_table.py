"""create casts_table

Revision ID: 7deafa202989
Revises: cf7fc450fe1d
Create Date: 2023-05-27 11:20:36.219645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7deafa202989'
down_revision = 'cf7fc450fe1d'
branch_labels = None
depends_on = None


def create_casts_table():
    op.create_table(
        "casts",
        sa.Column("imdb_id", sa.VARCHAR(10), nullable=False, index=True),
        sa.Column("name", sa.VARCHAR, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )

def create_constraints():
    op.create_unique_constraint(
        "casts_unique_constraint",
        "casts",
        ["imdb_id", "name"]
    )
    op.create_foreign_key(
            "fk_casts_imdb_id",
            "casts",
            "movies",
            ["imdb_id"],
            ["imdb_id"],
            ondelete="CASCADE",
        )

def upgrade() -> None:
    create_casts_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("casts")