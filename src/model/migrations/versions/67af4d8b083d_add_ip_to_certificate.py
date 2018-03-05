"""add ip to certificate

Revision ID: 67af4d8b083d
Revises: 2554ae71666e
Create Date: 2018-02-24 20:13:48.600610

"""

# revision identifiers, used by Alembic.
revision = '67af4d8b083d'
down_revision = '2554ae71666e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'certificate',
        sa.Column('ip', sa.String(256), nullable=True)
    )


def downgrade():
    op.drop_column('certificate', 'ip')
