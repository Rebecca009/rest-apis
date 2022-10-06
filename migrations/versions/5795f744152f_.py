"""empty message

Revision ID: 5795f744152f
Revises: e237c426707f
Create Date: 2022-10-04 18:47:45.665156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5795f744152f'
down_revision = 'e237c426707f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'description')
    # ### end Alembic commands ###
