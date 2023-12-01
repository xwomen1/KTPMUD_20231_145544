"""create_nguoidung_table

Revision ID: a714836f77ac
Revises: 
Create Date: 2023-11-27 22:19:31.162818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a714836f77ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('nguoidung',
                    sa.Column('id', sa.Integer(), nullable=False,autoincrement=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('role', sa.String, nullable=False),
                    sa.Column('describe', sa.String),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))

def downgrade() -> None:
    op.drop_table('nguoidung')
