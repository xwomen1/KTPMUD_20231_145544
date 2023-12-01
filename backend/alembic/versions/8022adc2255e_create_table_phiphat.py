"""create_table_phiphat

Revision ID: 8022adc2255e
Revises: e0d524a2ef36
Create Date: 2023-12-01 11:19:18.563563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8022adc2255e'
down_revision: Union[str, None] = 'e0d524a2ef36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("phiphat",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("giaidoan", sa.Integer(), nullable=False),
                    sa.Column("phiphat", sa.Integer()),
                    sa.Column("mahopdong", sa.String(50), nullable=False),
                    sa.PrimaryKeyConstraint("id"))
    op.create_foreign_key('phiphat_fk', source_table="phiphat", referent_table="hopdong",
                          local_cols=['mahopdong'], remote_cols=['mahopdong'], ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint("phiphat_fk","phiphat")
    op.drop_table("phiphat")
