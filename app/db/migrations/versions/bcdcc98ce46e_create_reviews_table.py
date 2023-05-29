"""create reviews_table

Revision ID: bcdcc98ce46e
Revises: a6ffd240dc42
Create Date: 2023-05-29 12:52:13.639437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcdcc98ce46e'
down_revision = 'a6ffd240dc42'
branch_labels = None
depends_on = None


def create_reviews_table():
    op.create_table(
        "reviews",
        sa.Column("id", sa.INTEGER, primary_key=True, autoincrement=True, server_default="1"),
        sa.Column("imdb_id", sa.VARCHAR(10), nullable=False, index=True),
        sa.Column("rating", sa.VARCHAR, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )

def create_constraints():
    op.create_unique_constraint(
        "reviews_unique_constraint",
        "reviews",
        ["imdb_id", "rating"]
    )
    op.create_foreign_key(
            "fk_reviews_imdb_id",
            "reviews",
            "movies",
            ["imdb_id"],
            ["imdb_id"],
            ondelete="CASCADE",
        )

def upgrade() -> None:
    create_reviews_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("reviews")
