"""initial

Revision ID: 0001
Revises: 
Create Date: 2025-05-11 12:11:44.701437

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('simplestream_sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('index_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('simplestream_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('arch', sa.Enum('AMD64', 'ARM64', 'ARMHF', 'I386', 'PPC64EL', 'S390X', name='simplestreamproductarch'),nullable=False),
    sa.Column('os', sa.String(), nullable=False),
    sa.Column('properties', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('simplestream_product_versions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('channel', sa.Enum('STABLE', 'CANDIDATE', 'DAILY', name='simplestreamchannel'), nullable=False),
    sa.Column('properties', sa.JSON(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['simplestream_products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('simplestream_product_versions')
    op.drop_table('simplestream_products')
    op.drop_table('simplestream_sources')
    # ### end Alembic commands ###
