"""create_employee_table

Revision ID: a6b135847139
Revises: 4692803039df
Create Date: 2023-12-06 21:01:51.618239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6b135847139'
down_revision: Union[str, None] = '4692803039df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("employee",
                    sa.Column("manv", sa.Integer(), nullable=False),
                    sa.Column("salary", sa.Float(), nullable=False),
                    sa.Column("ngaybatdaucongtac", sa.DATE(), nullable=False),
                    sa.Column("ngayketthuccongtac", sa.DATE(), nullable=False),
                    sa.Column("owner_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint("manv"))
    op.create_foreign_key('employee_fk', source_table="employee", referent_table="users",
                          local_cols=['manv'], remote_cols=['id'], ondelete="CASCADE", onupdate="CASCADE")


def downgrade() -> None:
    op.drop_constraint("employee_fk","employee")
    op.drop_table("employee")