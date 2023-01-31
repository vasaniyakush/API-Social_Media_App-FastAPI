"""add content column to posts table

Revision ID: ca9223ef5df6
Revises: 3195f59f923d
Create Date: 2023-01-31 19:47:32.357618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca9223ef5df6'
down_revision = '3195f59f923d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts2',sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts2', 'content')
    pass
