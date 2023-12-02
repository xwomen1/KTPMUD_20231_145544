"""create_phiphat_table

Revision ID: 4692803039df
Revises: f4c390e9c080
Create Date: 2023-12-02 10:48:16.553898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4692803039df'
down_revision: Union[str, None] = 'f4c390e9c080'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("phiphat",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("phiphat", sa.Integer()),
                    sa.Column("mahopdong", sa.String(50), nullable=False),
                    sa.PrimaryKeyConstraint("id"))
    op.create_foreign_key('phiphat_fk', source_table="phiphat", referent_table="contract",
                          local_cols=['mahopdong'], remote_cols=['mahopdong'], ondelete="CASCADE", onupdate="CASCADE")

def downgrade() -> None:
    op.drop_constraint("phiphat_fk","phiphat")
    op.drop_table("phiphat")

