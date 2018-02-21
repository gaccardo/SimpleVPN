"""create profile table

Revision ID: ea068a98511
Revises: fb38e496ad3
Create Date: 2018-02-21 13:52:07.737232

"""

# revision identifiers, used by Alembic.
revision = 'ea068a98511'
down_revision = 'fb38e496ad3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'profile',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(256), nullable=False)
    )
    op.create_index("uq_profile_name", "profile", ["name"],
                    unique=True)


def downgrade():
    op.drop_index("uq_profile_name")
    op.drop_table("profile")
