"""certificate name should be unique

Revision ID: fb38e496ad3
Revises: 40ed682ecd28
Create Date: 2018-02-21 10:22:19.955597

"""

# revision identifiers, used by Alembic.
revision = 'fb38e496ad3'
down_revision = '40ed682ecd28'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index("uq_name", "certificate", ["name"],
                    unique=True)


def downgrade():
    op.drop_index("uq_name")
