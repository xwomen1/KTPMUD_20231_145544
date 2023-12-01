"""create_table_khachhang

Revision ID: 83c721e39dfa
Revises: 026a6218873c
Create Date: 2023-12-01 09:48:07.621688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83c721e39dfa'
down_revision: Union[str, None] = '026a6218873c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('khachhang',
                    sa.Column("maKH", sa.Integer(), nullable=False),
                    sa.Column("username", sa.String(255), nullable=False),
                    sa.Column("diachi", sa.String(255)),
                    sa.Column("phonenumber", sa.String(20), nullable=False, unique=True),
                    sa.Column("email", sa.String(50), nullable=False, unique=True),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('maKH'))
    op.create_foreign_key('khachhang_fk', source_table="khachhang", referent_table="nguoidung",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint('khachhang_fk', table_name="khachhang")
    op.drop_table('khachhang')
