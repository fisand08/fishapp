"""modified portfolio model

Revision ID: 258599166602
Revises: 2aeb80987778
Create Date: 2024-04-08 13:14:17.972871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '258599166602'
down_revision = '2aeb80987778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stock_list', sa.String(length=256), nullable=False))
        batch_op.create_index(batch_op.f('ix_portfolio_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_portfolio_name'))
        batch_op.drop_column('stock_list')

    # ### end Alembic commands ###