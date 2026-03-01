from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    preco_venda: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    preco_compra: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    categoria_id: Optional[int] = Field(None, gt=0)
    codigo_barra: Optional[str] = Field(None, max_length=50)
    estoque: int = Field(ge=0)


class ProdutoCreate(ProdutoBase):
    pass 

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    preco_venda: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    preco_compra: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    categoria_id: Optional[int] = Field(None, gt=0)
    codigo_barra: Optional[str] = Field(None, max_length=50)
    ativo: bool = True

class ProdutoResponse(ProdutoBase):
    id: int
    estoque: int
    categoria_nome: Optional[str]
    ativo: bool = True

    class ConfigDict:
        from_attributes = True
