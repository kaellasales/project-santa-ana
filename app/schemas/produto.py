from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    preco_venda: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    preco_compra: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    categoria_id: int | None = Field(None, gt=0)
    codigo_barra: str | None = Field(None, max_length=50)
    estoque: int = Field(ge=0)
    estoque_minimo: int = Field(default=10, ge=0)


class ProdutoCreate(ProdutoBase):
    pass 

class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=100)
    preco_venda: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    preco_compra: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    categoria_id: int | None = Field(None, gt=0)
    codigo_barra: str | None = Field(None, max_length=50)
    ativo: bool = True
    estoque_minimo: int | None = Field(None, ge=0)

class ProdutoResponse(ProdutoBase):
    id: int
    estoque: int
    categoria_nome: Optional[str]
    ativo: bool = True

    class ConfigDict:
        from_attributes = True
