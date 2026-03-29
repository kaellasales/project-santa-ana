from pydantic import BaseModel, Field, field_validator
from uuid import UUID                          


class ItemVendaBase(BaseModel):
    quantidade: int = Field(gt=0)

class ItemVendaCreate(ItemVendaBase):
    produto_id: int

    @field_validator("quantidade")
    @classmethod
    def validar_quantidade(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que 0")
        return v


class ItemVendaResponse(ItemVendaBase):
    id: int
    venda_id: int
    produto_id: int
    preco_unitario: float
    subtotal: float

    class ConfigDict:
        from_attributes = True


class ItemVendaUpdate(BaseModel):
    quantidade: int | None = Field(None, gt=0)


class ItemVendaSync(BaseModel):
    id_offline: UUID
    produto_id: int
    quantidade: int = Field(gt=0)