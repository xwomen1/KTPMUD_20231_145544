"""create_contract_table

Revision ID: f4c390e9c080
Revises: bb8038855510
Create Date: 2023-12-02 10:47:19.126320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4c390e9c080'
down_revision: Union[str, None] = 'bb8038855510'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contract',
                    sa.Column("mahopdong", sa.String(50), nullable=False),
                    sa.Column("giaidoan", sa.Integer(), nullable=False),
                    sa.Column("phithanhtoan", sa.Integer(), nullable=False),
                    sa.Column("motaphi", sa.String(100)),
                    sa.Column("pt_thanhtoan", sa.String(50), nullable=False),
                    sa.Column("ngaytttheohd", sa.DATE(), nullable=False),
                    sa.Column("ngayttthucte", sa.DATE(), nullable=False),
                    sa.Column("owner", sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint("mahopdong"))

    op.create_foreign_key('hopdong_fk', source_table="contract", referent_table="event",
                          local_cols=['owner'], remote_cols=['mact'], ondelete="CASCADE")
def downgrade() -> None:
    op.drop_constraint("hopdong_fk", "contract")
    op.drop_table("contract")
