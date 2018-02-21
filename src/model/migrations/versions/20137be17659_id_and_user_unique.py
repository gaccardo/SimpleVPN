"""id and user unique

Revision ID: 20137be17659
Revises: 1a75e5116ac1
Create Date: 2018-02-21 08:52:07.601254

"""

# revision identifiers, used by Alembic.
revision = '20137be17659'
down_revision = '1a75e5116ac1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index("uq_username", "user", ["username"],
                    unique=True)


def downgrade():
    op.drop_index("uq_username")
