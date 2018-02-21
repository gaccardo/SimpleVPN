"""add certificate table

Revision ID: 40ed682ecd28
Revises: 20137be17659
Create Date: 2018-02-21 09:43:56.218743

"""

# revision identifiers, used by Alembic.
revision = '40ed682ecd28'
down_revision = '20137be17659'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'certificate',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('valid', sa.Boolean, default=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'))
    )


def downgrade():
    op.drop_table('certificate')
