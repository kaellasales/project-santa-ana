from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    codigo_barra: str = Field(...)
    preco_venda: Decimal = Field(..., gt=0)
    preco_compra: Optional[Decimal] = Field(None, gt=0)
    categoria_id: int
    codigo_barra: Optional[str] = Field(None, max_length=50)


class ProdutoCreate(ProdutoBase):
    pass 


class ProdutoResponse(ProdutoBase):
    id: int
    estoque: int
    categoria_nome: Optional[str]

    class ConfigDict:
        from_attributes = True
