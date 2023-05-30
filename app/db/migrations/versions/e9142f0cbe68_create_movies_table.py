"""create movies_table

Revision ID: e9142f0cbe68
Revises: 
Create Date: 2023-05-25 14:56:04.835213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9142f0cbe68'
down_revision = None
branch_labels = None
depends_on = None


def create_movies_table():
    op.create_table(
        "movies",
        sa.Column("imdb_id", sa.VARCHAR(10), nullable=False, index=True, primary_key=True),
        sa.Column("title", sa.VARCHAR, nullable=False, index=True),
        sa.Column("icaa_rating", sa.VARCHAR, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )
    

def create_constraints():
    op.create_unique_constraint(
        "uq_movies_imdb_id",
        "movies",
        ["imdb_id"]
    )
    op.create_unique_constraint(
        "uq_movies_title",
        "movies",
        ["title"]
    )


def upgrade() -> None:
    create_movies_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("movies")
