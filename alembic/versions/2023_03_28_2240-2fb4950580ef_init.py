"""init

Revision ID: 2fb4950580ef
Revises: 
Create Date: 2023-03-28 22:40:21.666909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fb4950580ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('financial_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('open_price', sa.Float(precision=2), nullable=False),
    sa.Column('close_price', sa.Float(precision=2), nullable=False),
    sa.Column('volume', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol', 'date', name='symbol_date_uc')
    )
    op.create_index(op.f('ix_financial_data_date'), 'financial_data', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_financial_data_date'), table_name='financial_data')
    op.drop_table('financial_data')
    # ### end Alembic commands ###
