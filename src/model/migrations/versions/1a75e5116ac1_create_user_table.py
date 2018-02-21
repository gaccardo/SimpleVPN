"""create user table

Revision ID: 1a75e5116ac1
Revises: None
Create Date: 2018-02-20 20:32:18.253171

"""

# revision identifiers, used by Alembic.
revision = '1a75e5116ac1'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(256), nullable=False),
        sa.Column('fullname', sa.String(256), nullable=True),
        sa.Column('email', sa.String(256), nullable=False),
        sa.Column('certificate', sa.String(256), nullable=True)
    )


def downgrade():
    op.drop_table('user')
