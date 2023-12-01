"""create_table_event

Revision ID: 79b36623ee32
Revises: 83c721e39dfa
Create Date: 2023-12-01 10:15:24.331712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79b36623ee32'
down_revision: Union[str, None] = '83c721e39dfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('sukien',
                    sa.Column("maCT", sa.String(20), nullable=False),
                    sa.Column("name", sa.String(20), nullable=False),
                    sa.Column("detail", sa.String(100)),
                    sa.Column("owner_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('maCT')
                    )
    op.create_foreign_key("sukien_fk", source_table="sukien", referent_table="nguoidung",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint('sukien_fk', table_name="sukien")
    op.drop_table('sukien')
