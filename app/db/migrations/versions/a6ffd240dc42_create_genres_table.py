"""create genres_table

Revision ID: a6ffd240dc42
Revises: 7deafa202989
Create Date: 2023-05-27 11:37:30.608453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6ffd240dc42'
down_revision = '7deafa202989'
branch_labels = None
depends_on = None


def create_genres_table():
    op.create_table(
        "genres",
        sa.Column("imdb_id", sa.VARCHAR(10), nullable=False, index=True),
        sa.Column("genre", sa.VARCHAR, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )

def create_constraints():
    op.create_unique_constraint(
        "genres_unique_constraint",
        "genres",
        ["imdb_id", "genre"]
    )
    op.create_foreign_key(
            "fk_genres_imdb_id",
            "genres",
            "movies",
            ["imdb_id"],
            ["imdb_id"],
            ondelete="CASCADE",
        )

def upgrade() -> None:
    create_genres_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("genres")
