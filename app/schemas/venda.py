from pydantic import BaseModel, Field
from pydantic import field_validator
from datetime import datetime
from typing import Optional, List

class VendaBase(BaseModel):
    pass
    # usuario_id: int = Field(gt=0)

class VendaCreate(VendaBase):
    pass

class VendaUpdate(BaseModel):
    pass

class VendaResponse(VendaBase):
    id: int
    data_venda: datetime
    total: float

    class ConfigDict:
        from_attributes = True

class VendaDetalhada(VendaResponse):
    itens: List = []
    # formas_pagamento: List = []