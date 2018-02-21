"""one rule name per profile

Revision ID: 213f429b5bb4
Revises: 56ca92a0972f
Create Date: 2018-02-21 14:52:47.494931

"""

# revision identifiers, used by Alembic.
revision = '213f429b5bb4'
down_revision = '56ca92a0972f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index("uq_rulename", "rule", ["name", "profile_id"], unique=True)


def downgrade():
    op.drop_index("uq_rulename")
