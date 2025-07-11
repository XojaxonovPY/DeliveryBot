"""Create a baseline migrations

Revision ID: 5364b3678833
Revises: 66f3ed4576e5
Create Date: 2025-04-20 14:10:59.289963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5364b3678833'
down_revision: Union[str, None] = '66f3ed4576e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('status', sa.Enum('ACCEPTED', 'DELIVERY', 'DELIVERED', name='status_enum', create_constraint=True), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('Asia/Tashkent', NOW())"), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('Asia/Tashkent', NOW())"), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###
