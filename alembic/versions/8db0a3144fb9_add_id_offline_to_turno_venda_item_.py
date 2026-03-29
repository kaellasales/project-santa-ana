"""add id_offline to turno, venda, item_venda, pagamento

Revision ID: 8db0a3144fb9
Revises: 7cf26d5a921b
Create Date: 2026-03-29 18:51:08.624245

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '8db0a3144fb9'
down_revision: Union[str, None] = '7cf26d5a921b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade():
    op.add_column("turnos",
        sa.Column("id_offline", UUID(as_uuid=True), nullable=True, unique=True))
    op.create_index("ix_turnos_id_offline", "turnos", ["id_offline"])

    op.add_column("vendas",
        sa.Column("id_offline", UUID(as_uuid=True), nullable=True, unique=True))
    op.create_index("ix_vendas_id_offline", "vendas", ["id_offline"])

    op.add_column("itens_venda",
        sa.Column("id_offline", UUID(as_uuid=True), nullable=True, unique=True))
    op.create_index("ix_itens_venda_id_offline", "itens_venda", ["id_offline"])

    op.add_column("formas_pagamento",
        sa.Column("id_offline", UUID(as_uuid=True), nullable=True, unique=True))
    op.create_index("ix_formas_pagamento_id_offline", "formas_pagamento", ["id_offline"])


def downgrade():
    op.drop_index("ix_turnos_id_offline", "turnos")
    op.drop_column("turnos", "id_offline")

    op.drop_index("ix_vendas_id_offline", "vendas")
    op.drop_column("vendas", "id_offline")

    op.drop_index("ix_itens_venda_id_offline", "itens_venda")
    op.drop_column("itens_venda", "id_offline")

    op.drop_index("ix_formas_pagamento_id_offline", "formas_pagamento")
    op.drop_column("formas_pagamento", "id_offline")