"""create_nhanvien_table

Revision ID: 4e883f2a03df
Revises: a714836f77ac
Create Date: 2023-11-27 23:45:39.130350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e883f2a03df'
down_revision: Union[str, None] = 'a714836f77ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('nhanvien',
                    sa.Column('maNV', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String, nullable=False),
                    sa.Column('gender', sa.Boolean, nullable=False),
                    # sa.Column('dateofbirth', sa.String, nullable=False),
                    sa.Column('diachi', sa.String, nullable=False),
                    sa.Column('phonenumber', sa.String, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('cosalary', sa.String, nullable=False),
                    sa.PrimaryKeyConstraint('maNV'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('phonenumber'),
                    )


def downgrade() -> None:
    op.drop_table('nhanvien')
