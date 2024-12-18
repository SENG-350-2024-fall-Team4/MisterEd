"""Add scheduled_hour to appointment

Revision ID: b5a0e2bbbe57
Revises: 28819229672e
Create Date: 2024-12-03 03:38:39.499169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5a0e2bbbe57'
down_revision = '28819229672e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('scheduled_hour', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.drop_column('scheduled_hour')

    # ### end Alembic commands ###
