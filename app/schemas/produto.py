from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    preco_venda: Decimal = Field(..., gt=0)
    preco_compra: Optional[Decimal] = Field(None, gt=0)
    categoria_id: int
    codigo_barra: Optional[str] = Field(None, max_length=50)


class ProdutoCreate(ProdutoBase):
    pass 

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    preco_venda: Optional[Decimal] = Field(None, gt=0)
    preco_compra: Optional[Decimal] = Field(None, gt=0)
    categoria_id: Optional[int]
    codigo_barra: Optional[str] = Field(None, max_length=50)

class ProdutoResponse(ProdutoBase):
    id: int
    estoque: int
    categoria_nome: Optional[str]

    class ConfigDict:
        from_attributes = True
