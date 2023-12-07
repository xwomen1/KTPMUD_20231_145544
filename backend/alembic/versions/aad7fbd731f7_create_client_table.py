"""create_client_table

Revision ID: aad7fbd731f7
Revises: 3aed911a32b5
Create Date: 2023-12-02 10:40:35.882018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aad7fbd731f7'
down_revision: Union[str, None] = '3aed911a32b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('client',
                    sa.Column("makh", sa.Integer(), nullable=False),
                    sa.Column("full_name", sa.String(255), nullable=False),
                    sa.Column("email", sa.String(255), nullable=False, unique=True),
                    sa.Column("username", sa.String(255), nullable=False),
                    sa.Column("password", sa.String(255), nullable=False),
                    sa.Column("gender", sa.Boolean, nullable=False),
                    sa.Column("dateofbirth", sa.DATE, nullable=False),
                    sa.Column("address", sa.String()),
                    sa.Column("phonenumber", sa.String(20), nullable=False, unique=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column("is_active", sa.Boolean, default=False),
                    sa.PrimaryKeyConstraint("makh"))

def downgrade() -> None:
    op.drop_table('client')
