from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional

class ItemVendaBase(BaseModel):
    quantidade: int = Field(gt=0)
    preco_unitario: float = Field(gt=0)

class ItemVendaCreate(ItemVendaBase):
    produto_id: int
    
    @field_validator("quantidade")
    @classmethod
    def validar_quantidade(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que 0")
        return v
    
    # @field_validator("preco_unitario")
    # @classmethod
    # def validar_preco(cls, v):
    #     if v <= 0:
    #         raise ValueError("Preço unitário deve ser maior que 0")
    #     return v

class ItemVendaResponse(ItemVendaBase):
    id: int
    venda_id: int
    produto_id: int
    subtotal: float

    class ConfigDict:
        from_attributes = True

class ItemVendaUpdate(BaseModel):
    quantidade: Optional[int] = Field(None, gt=0)
    # preco_unitario: Optional[float] = Field(None, gt=0)