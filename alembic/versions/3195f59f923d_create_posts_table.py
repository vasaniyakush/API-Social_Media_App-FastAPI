"""create posts table

Revision ID: 3195f59f923d
Revises: 
Create Date: 2023-01-31 19:34:02.087479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3195f59f923d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts2', sa.Column('id',sa.Integer(), nullable=False, primary_key=True)
    ,sa.Column('title', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts2')
    pass