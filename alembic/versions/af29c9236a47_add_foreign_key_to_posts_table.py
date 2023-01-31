"""add foreign key to posts table

Revision ID: af29c9236a47
Revises: d5bb845dc66d
Create Date: 2023-01-31 21:29:45.783995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af29c9236a47'
down_revision = 'd5bb845dc66d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column('owner_id',sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts2',referent_table="users",local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE" )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name="posts2")
    op.drop_column('posts2','owner_id')
    pass
