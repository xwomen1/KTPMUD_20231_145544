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
                    sa.Column("full_name", sa.String(255), nullable=False),
                    sa.Column("email", sa.String(255), nullable=False, unique=True),
                    sa.Column("username", sa.String(255), nullable=False),
                    sa.Column("password", sa.String(255), nullable=False),
                    sa.Column("gender", sa.Boolean, nullable=False),
                    sa.Column("dateofbirth", sa.DATE, nullable=False),
                    sa.Column("address", sa.String()),
                    sa.Column("phonenumber", sa.String(20), nullable=False, unique=True),
                    sa.Column("salary", sa.Float(), nullable=False),
                    sa.Column("ngaybatdaucongtac", sa.DATE(), nullable=False),
                    sa.Column("ngayketthuccongtac", sa.DATE(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column("is_active", sa.Boolean, default=False),
                    sa.Column("owner_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint("manv"))


def downgrade() -> None:
    op.drop_table("employee")