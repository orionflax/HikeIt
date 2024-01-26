"""empty message

Revision ID: de89c53451f9
Revises: 
Create Date: 2024-01-26 21:50:34.262539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'de89c53451f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('route_mappings', postgresql.ARRAY(sa.Integer(), dimensions=2), nullable=False),
    sa.Column('distance', sa.Integer(), nullable=False),
    sa.Column('ascent', sa.Integer(), nullable=False),
    sa.Column('max_height', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('routes')
    # ### end Alembic commands ###