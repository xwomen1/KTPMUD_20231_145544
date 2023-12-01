"""crate_table_detail_event

Revision ID: 33e10b7bda9a
Revises: 79b36623ee32
Create Date: 2023-12-01 10:26:41.600523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33e10b7bda9a'
down_revision: Union[str, None] = '79b36623ee32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('chitietsukien',
                    sa.Column("id", sa.Integer(), nullable=False, unique=True),
                    sa.Column("maKH", sa.Integer(), nullable=False),
                    sa.Column("maCT", sa.String(20), nullable=False),
                    sa.Column("maNV", sa.Integer(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column("ngaybatdau", sa.DATE(), nullable=False),
                    sa.Column("ngayketthuc", sa.DATE(), nullable=False),
                    sa.Column("detail", sa.String()),
                    sa.Column("songuoithamgia", sa.Integer(), nullable=False),
                    sa.Column("diadiem", sa.String(100), nullable=False),
                    sa.Column("mucphat", sa.Integer()),
                    sa.PrimaryKeyConstraint("id"))


    op.create_foreign_key("chitietsukien_maKH_fk", source_table="chitietsukien", referent_table="khachhang",
                          local_cols=['maKH'], remote_cols=['maKH'])
    op.create_foreign_key("chitietsukien_maCT_fk", source_table="chitietsukien", referent_table="sukien",
                          local_cols=['maCT'], remote_cols=['maCT'])
    op.create_foreign_key("chitietsukien_maNV_fk", source_table="chitietsukien", referent_table="nhanvien",
                          local_cols=['maNV'], remote_cols=['maNV'])


def downgrade() -> None:
    op.drop_constraint('chitietsukien_maKH_fk', table_name="chitietsukien")
    op.drop_constraint('chitietsukien_maCT_fk', table_name="chitietsukien")
    op.drop_constraint('chitietsukien_maNV_fk', table_name="chitietsukien")
    op.drop_table("chitietsukien")
