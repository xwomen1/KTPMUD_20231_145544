"""create_employee_table

Revision ID: f5092c86e9e8
Revises: 4692803039df
Create Date: 2023-12-08 21:19:05.998666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5092c86e9e8'
down_revision: Union[str, None] = '4692803039df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("employee",
                    sa.Column("manv", sa.String(), nullable=False),
                    sa.Column("salary", sa.Integer(), nullable=False),
                    sa.Column("ngaybatdaucongtac", sa.DATE(), nullable=False),
                    sa.Column("ngayketthuccongtac", sa.DATE(), nullable=False),
                    sa.Column("owner_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint("manv"))

    op.create_foreign_key("employee_fk",source_table= "employee", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("employee_fk", "employee")
    op.drop_table("employee")

