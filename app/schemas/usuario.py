from pydantic import BaseModel, Field
from app.models.usuario import RoleUsuario


class UsuarioBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=50)


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=6, max_length=72)
    role: RoleUsuario = RoleUsuario.VENDEDOR
    

class UsuarioUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=100)
    username: str | None = Field(None, min_length=3, max_length=50)
    senha: str | None = Field(None, min_length=6, max_length=72)
    ativo: bool | None = None


class UsuarioResponse(UsuarioBase):
    id: int
    role: RoleUsuario
    ativo: bool

    class ConfigDict:
        from_attributes = True