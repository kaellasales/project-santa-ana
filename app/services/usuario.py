from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.repositories.usuario import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.exceptions import UsuarioNotFoundError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def _hash_senha(self, senha: str) -> str:
        return pwd_context.hash(senha)

    def _verificar_senha(self, senha: str, hash: str) -> bool:
        return pwd_context.verify(senha, hash)

    def create(self, db: Session, usuario: UsuarioCreate):
        if self.repository.get_by_username(db, usuario.username):
            raise ValueError("Username já cadastrado")

        dados = usuario.model_dump()
        dados["senha"] = self._hash_senha(dados["senha"])
        obj = self.repository.create(db, dados)
        db.commit()
        db.refresh(obj)
        return obj

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.list(db, skip=skip, limit=limit)

    def get(self, db: Session, usuario_id: int):
        usuario = self.repository.get(db, usuario_id)
        if not usuario:
            raise UsuarioNotFoundError()
        return usuario

    def update(self, db: Session, usuario_id: int, usuario_atualizado: UsuarioUpdate):
        usuario = self.get(db, usuario_id)
        dados = usuario_atualizado.model_dump(exclude_unset=True)
        if "senha" in dados:
            dados["senha"] = self._hash_senha(dados["senha"])
        obj = self.repository.update(db, usuario, dados)
        db.commit()
        return obj

    def deactivate(self, db: Session, usuario_id: int):
        usuario = self.get(db, usuario_id)
        obj = self.repository.deactivate(db, usuario_id)
        db.commit()
        return obj

    def reativar(self, db: Session, usuario_id: int):
        obj = self.repository.reativar(db, usuario_id)
        if not obj:
            raise UsuarioNotFoundError()
        db.commit()
        return obj