"""add user table

Revision ID: d5bb845dc66d
Revises: ca9223ef5df6
Create Date: 2023-01-31 19:53:30.825156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5bb845dc66d'
down_revision = 'ca9223ef5df6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
