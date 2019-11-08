"""empty message

Revision ID: 3b4fb7211642
Revises: 
Create Date: 2019-11-08 08:23:46.813832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b4fb7211642'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gambar_lainnya')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gambar_lainnya',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('id_homestay', sa.INTEGER(), nullable=True),
    sa.Column('gambar1', sa.VARCHAR(length=150), nullable=True),
    sa.Column('gambar2', sa.VARCHAR(length=150), nullable=True),
    sa.Column('gambar3', sa.VARCHAR(length=150), nullable=True),
    sa.Column('gambar4', sa.VARCHAR(length=150), nullable=True),
    sa.Column('gambar5', sa.VARCHAR(length=150), nullable=True),
    sa.ForeignKeyConstraint(['id_homestay'], ['homestay.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###