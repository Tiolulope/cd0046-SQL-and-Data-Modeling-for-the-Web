"""empty message

Revision ID: 5848f6d8c7f4
Revises: f99e798e1d9d
Create Date: 2022-08-14 18:28:51.232866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5848f6d8c7f4'
down_revision = 'f99e798e1d9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website', sa.String(length=120), nullable=True))
    
    op.drop_column('venue', 'website_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.drop_column('venue', 'website')
    # ### end Alembic commands ###
