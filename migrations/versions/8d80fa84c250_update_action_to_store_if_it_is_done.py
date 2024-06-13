"""Update action to store if it is done

Revision ID: 8d80fa84c250
Revises: 4d933745539b
Create Date: 2024-06-13 20:59:07.655617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d80fa84c250'
down_revision: Union[str, None] = '4d933745539b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Action', sa.Column('is_done', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Action', 'is_done')
    # ### end Alembic commands ###