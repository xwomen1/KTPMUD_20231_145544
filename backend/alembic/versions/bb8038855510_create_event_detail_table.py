"""create_event_detail_table

Revision ID: bb8038855510
Revises: ce0bab936bfe
Create Date: 2023-12-02 10:43:59.309560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb8038855510'
down_revision: Union[str, None] = 'ce0bab936bfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('detail_event',
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("songuoithamgia", sa.Integer(), nullable=False),
                    sa.Column("start_date", sa.DATE(), nullable=False),
                    sa.Column("end_date", sa.DATE(), nullable=False),
                    sa.Column("detail", sa.String()),
                    sa.Column("location", sa.String(100), nullable=False),
                    sa.Column("mucphat", sa.Integer()),
                    sa.Column("owner_event", sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint("id"))


    op.create_foreign_key("owner_sk_fk", source_table="detail_event", referent_table="event",
                          local_cols=['owner_event'], remote_cols=['mact'], ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint('owner_sk_fk', table_name="detail_event")
    op.drop_table("detail_event")
