from pydantic import BaseModel, Field
from datetime import datetime
from app.models.turno import TurnoStatus


class TurnoAbrir(BaseModel):
    valor_inicial: float = Field(gt=0)


class TurnoFechar(BaseModel):
    valor_informado: float = Field(ge=0)
    observacoes: str | None = Field(None, max_length=500)


class TurnoAtivoResponse(BaseModel):
    id: int
    status: TurnoStatus
    data_abertura: datetime
    valor_inicial: float
    total_vendas: float
    quantidade_vendas: int
    usuario_nome: str | None = None

    class ConfigDict:
        from_attributes = True


class TurnoResumoResponse(TurnoAtivoResponse):
    data_fechamento: datetime | None = None
    valor_informado: float | None = None
    valor_esperado: float | None = None
    diferenca: float | None = None
    observacoes: str | None = None

    por_forma_pagamento: dict[str, float] = {}

    class ConfigDict:
        from_attributes = True