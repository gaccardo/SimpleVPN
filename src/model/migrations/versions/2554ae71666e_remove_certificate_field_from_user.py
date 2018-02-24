"""remove certificate field from user

Revision ID: 2554ae71666e
Revises: 213f429b5bb4
Create Date: 2018-02-24 17:39:43.111967

"""

# revision identifiers, used by Alembic.
revision = '2554ae71666e'
down_revision = '213f429b5bb4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('certificate')

def downgrade():
    op.add_column('user', sa.Column(sa.String, 'certificate'))
