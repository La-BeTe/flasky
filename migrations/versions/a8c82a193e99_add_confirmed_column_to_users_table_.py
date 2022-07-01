"""Add confirmed column to users table, make username unique

Revision ID: a8c82a193e99
Revises: b48bacbaa512
Create Date: 2022-06-30 20:23:06.826865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8c82a193e99'
down_revision = 'b48bacbaa512'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###