"""Initial migration

Revision ID: 88ce22a5a5b5
Revises: eaa0b3169ac5
Create Date: 2024-08-13 10:12:06.867856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88ce22a5a5b5'
down_revision: Union[str, None] = 'eaa0b3169ac5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
