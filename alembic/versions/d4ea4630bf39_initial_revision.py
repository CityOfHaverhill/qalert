"""Initial revision

Revision ID: d4ea4630bf39
Revises: 
Create Date: 2020-12-09 19:27:38.840051

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = 'd4ea4630bf39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('qalert_audits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qalert_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('create_date_unix', sa.Integer(), nullable=True),
    sa.Column('last_action', sa.DateTime(), nullable=True),
    sa.Column('last_action_unix', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('type_name', sa.VARCHAR(length=200), nullable=True),
    sa.Column('comments', sa.VARCHAR(length=5000), nullable=True),
    sa.Column('street_num', sa.VARCHAR(length=100), nullable=True),
    sa.Column('street_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('cross_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('city_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('point', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4269, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('qalert_requests')
    op.drop_table('qalert_audits')
    # ### end Alembic commands ###
