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
                    sa.Column("owner_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('makh'))

    op.create_foreign_key('owner_id_fk', source_table="client", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE", onupdate="CASCADE")

def downgrade() -> None:
    op.drop_constraint('owner_id_fk', table_name="infouser")
    op.drop_table('client')
