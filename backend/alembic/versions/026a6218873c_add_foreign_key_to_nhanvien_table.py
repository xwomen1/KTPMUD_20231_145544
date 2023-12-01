"""add_foreign_key_to_nhanvien_table

Revision ID: 026a6218873c
Revises: 4e883f2a03df
Create Date: 2023-11-27 23:58:28.173281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '026a6218873c'
down_revision: Union[str, None] = '4e883f2a03df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('nhanvien', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('nhanvien_fk', source_table="nhanvien", referent_table="nguoidung",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('nhanvien_fk', table_name="nhanvien")
    op.drop_column('nhanvien', 'owner_id')
