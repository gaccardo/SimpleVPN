"""create rule table

Revision ID: 56ca92a0972f
Revises: ea068a98511
Create Date: 2018-02-21 13:55:50.591329

"""

# revision identifiers, used by Alembic.
revision = '56ca92a0972f'
down_revision = 'ea068a98511'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'rule',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(256), nullable=True),
        sa.Column('cidr', sa.String(256), nullable=True, default="0.0.0.0/0"),
        sa.Column('proto', sa.String(256), nullable=True, default="tcp"),
        sa.Column('port', sa.String(256), nullable=False),
        sa.Column('profile_id', sa.Integer, sa.ForeignKey('profile.id'))
    )


def downgrade():
    op.drop_table('rule')
