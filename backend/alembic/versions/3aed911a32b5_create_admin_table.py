"""create_table_users

Revision ID: 3aed911a32b5
Revises: 77df1f6b603c
Create Date: 2023-12-02 10:10:06.526264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aed911a32b5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column("email", sa.String(255), nullable=False, unique=True),
                    sa.Column("fullname", sa.String(255), nullable=False),
                    sa.Column("username", sa.String(255), nullable=False, unique=True),
                    sa.Column("password", sa.String(255), nullable=False),
                    sa.Column("gender", sa.Boolean, nullable=False),
                    sa.Column("dateofbirth", sa.DATE, nullable=False),
                    sa.Column("phonenumber", sa.String(20), nullable=False, unique=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column("role", sa.String(), nullable=False),
                    sa.Column("is_active", sa.Boolean, default=False),
                    sa.PrimaryKeyConstraint("id"))

def downgrade() -> None:
    op.drop_table("users")
