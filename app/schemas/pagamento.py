from pydantic import BaseModel, Field
from uuid import UUID                          
from app.models.pagamento import TipoPagamento


class FormaPagamentoCreate(BaseModel):
    tipo: TipoPagamento
    valor_recebido: float = Field(gt=0)


class FormaPagamentoResponse(BaseModel):
    id: int
    venda_id: int
    tipo: TipoPagamento
    valor_recebido: float
    troco: float

    class ConfigDict:
        from_attributes = True


class FormaPagamentoSync(BaseModel):
    id_offline: UUID
    tipo: TipoPagamento
    valor_recebido: float = Field(gt=0)