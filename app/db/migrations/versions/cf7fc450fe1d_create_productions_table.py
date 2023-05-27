"""create productions_table

Revision ID: cf7fc450fe1d
Revises: e9142f0cbe68
Create Date: 2023-05-27 10:49:47.456464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf7fc450fe1d'
down_revision = 'e9142f0cbe68'
branch_labels = None
depends_on = None


def create_productions_table():
    op.create_table(
        "productions",
        sa.Column("id", sa.INTEGER, primary_key=True, autoincrement=True, server_default="1"),
        sa.Column("imdb_id", sa.VARCHAR(10), nullable=False, index=True),
        sa.Column("director", sa.VARCHAR, nullable=True),
        sa.Column("country", sa.VARCHAR, nullable=True),
        sa.Column("producer", sa.VARCHAR, nullable=True),
        sa.Column("language", sa.VARCHAR, nullable=True),
        sa.Column("distributor", sa.VARCHAR, nullable=True),
        sa.Column("company", sa.VARCHAR, nullable=True),
        sa.Column("cost", sa.INTEGER, nullable=True),
        sa.Column("date", sa.VARCHAR, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )

def create_constraints():
    op.create_foreign_key(
            "fk_productions_imdb_id",
            "productions",
            "movies",
            ["imdb_id"],
            ["imdb_id"],
            ondelete="CASCADE",
        )

def upgrade() -> None:
    create_productions_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("productions")
