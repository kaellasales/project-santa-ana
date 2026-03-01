from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime

class CategoriaBase(BaseModel):
    nome: str = Field(min_length=1)

class CategoriaCreate(CategoriaBase):
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        if not v.strip():
            raise ValueError("nome não pode ser vazio.")
        return v

class CategoriaResponse(CategoriaBase):
    id: int
    ativo: bool = True

    class ConfigDict:
        from_attributes = True