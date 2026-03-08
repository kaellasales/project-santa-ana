from pydantic import BaseModel, Field
from datetime import datetime
from app.models.movimentacao import TipoMovimentacao, MotivoMovimentacao


class MovimentacaoEstoqueBase(BaseModel):
    tipo: TipoMovimentacao
    motivo: MotivoMovimentacao
    quantidade: int = Field(gt=0)


class MovimentacaoEstoqueCreate(MovimentacaoEstoqueBase):
    produto_id: int = Field(gt=0)
    venda_id: int | None = None


class MovimentacaoEstoqueResponse(MovimentacaoEstoqueBase):
    id: int
    produto_id: int
    venda_id: int | None = None
    data: datetime

    class ConfigDict:
        from_attributes = True