"""empty message

Revision ID: 84a0381f80e1
Revises: 
Create Date: 2019-04-28 13:41:51.743000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84a0381f80e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_like',
    sa.Column('likeId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('questionId', sa.Integer(), nullable=True),
    sa.Column('likeTime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['questionId'], ['t_question.questionId'], ),
    sa.ForeignKeyConstraint(['userId'], ['t_user.userId'], ),
    sa.PrimaryKeyConstraint('likeId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_like')
    # ### end Alembic commands ###
