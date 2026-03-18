from pydantic import BaseModel, Field
from pydantic import field_validator
from datetime import datetime
from typing import Optional, List
from app.schemas.itemVenda import ItemVendaResponse
from app.schemas.pagamento import FormaPagamentoResponse
class VendaBase(BaseModel):
    pass
    # usuario_id: int = Field(gt=0)


class VendaCreate(VendaBase):
    pass


class VendaUpdate(BaseModel):
    forma_pagamento: str | None = None
    acrescimo: float | None = Field(None, ge=0)
    desconto: float | None = Field(None, ge=0)

class VendaResponse(VendaBase):
    id: int
    usuario_id: int
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