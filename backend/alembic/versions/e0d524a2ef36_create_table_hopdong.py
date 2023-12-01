"""create_table_hopdong

Revision ID: e0d524a2ef36
Revises: 33e10b7bda9a
Create Date: 2023-12-01 11:12:54.698979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0d524a2ef36'
down_revision: Union[str, None] = '33e10b7bda9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hopdong',
                    sa.Column("mahopdong", sa.String(50), nullable=False, unique=True),
                    sa.Column("giaidoan", sa.Integer(), nullable=False),
                    sa.Column("phithanhtoan", sa.Integer(), nullable=False),
                    sa.Column("motaphi", sa.String(100)),
                    sa.Column("phuongthuctt", sa.String(50), nullable=False),
                    sa.Column("ngaytttheohd", sa.DATE(), nullable=False),
                    sa.Column("ngayttthucte", sa.DATE(), nullable=False),
                    sa.Column("owner_sk", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint("mahopdong"))
    op.create_foreign_key('hopdong_fk', source_table="hopdong", referent_table="chitietsukien",
                          local_cols=['owner_sk'], remote_cols=['id'], ondelete="CASCADE")
def downgrade() -> None:
    op.drop_constraint("hopdong_fk", "hopdong")
    op.drop_table("hopdong")
