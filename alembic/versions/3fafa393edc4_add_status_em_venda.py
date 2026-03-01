"""add status em venda e model forma de pagamento

Revision ID: 3fafa393edc4
Revises: 028da4e2b4e0
Create Date: 2026-03-01 20:13:27.140163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fafa393edc4'
down_revision: Union[str, None] = '028da4e2b4e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    vendastatus = sa.Enum('ABERTA', 'CONCLUIDA', 'CANCELADA', name='vendastatus')
    vendastatus.create(op.get_bind())
    op.add_column('vendas', sa.Column(
        'status',
        vendastatus,
        nullable=False,
        server_default='ABERTA'
    ))

def downgrade() -> None:
    op.drop_column('vendas', 'status')
    sa.Enum(name='vendastatus').drop(op.get_bind())