from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from uuid import UUID                          
from app.schemas.itemVenda import ItemVendaResponse, ItemVendaSync          
from app.schemas.pagamento import FormaPagamentoResponse, FormaPagamentoSync 


class VendaBase(BaseModel):
    pass


class VendaCreate(VendaBase):
    pass


class VendaUpdate(BaseModel):
    forma_pagamento: str | None = None
    acrescimo: float | None = Field(None, ge=0)
    desconto: float | None = Field(None, ge=0)


class VendaResponse(VendaBase):
    id: int
    turno_id: int
    usuario_id: int
    usuario_nome: str | None = None
    data_venda: datetime | None = None
    total: float
    status: str
    forma_pagamento: FormaPagamentoResponse | None = None
    acrescimo: float | None = None
    desconto: float | None = None

    class ConfigDict:
        from_attributes = True


class VendaDetalhada(VendaResponse):
    itens: List[ItemVendaResponse] = []


class VendaSync(BaseModel):
    id_offline: UUID
    data_venda: datetime
    desconto: float = 0.0
    acrescimo: float = 0.0
    itens: List[ItemVendaSync]
    pagamento: FormaPagamentoSync

