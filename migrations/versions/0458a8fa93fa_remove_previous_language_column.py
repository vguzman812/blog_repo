"""remove previous language column

Revision ID: 0458a8fa93fa
Revises: ebaee91d89b5
Create Date: 2023-05-04 12:23:39.208108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0458a8fa93fa'
down_revision = 'ebaee91d89b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_column('language')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.VARCHAR(length=5), nullable=True))

    # ### end Alembic commands ###