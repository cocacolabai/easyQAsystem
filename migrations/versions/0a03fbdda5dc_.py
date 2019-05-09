"""empty message

Revision ID: 0a03fbdda5dc
Revises: 84a0381f80e1
Create Date: 2019-05-09 10:42:25.028000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a03fbdda5dc'
down_revision = '84a0381f80e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_user', sa.Column('lastLoginTime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_user', 'lastLoginTime')
    # ### end Alembic commands ###