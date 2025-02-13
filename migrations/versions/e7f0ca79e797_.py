"""empty message

Revision ID: e7f0ca79e797
Revises: 7e673d9fa5cf
Create Date: 2024-03-20 14:10:12.725396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f0ca79e797'
down_revision = '7e673d9fa5cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('deadline', sa.DateTime(), nullable=False))

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('is_new', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('comment', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_column('comment')
        batch_op.drop_column('is_new')
        batch_op.drop_column('description')

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('deadline')
        batch_op.drop_column('description')

    # ### end Alembic commands ###
