from sqlalchemy.orm import Session
from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate
from app.core.exceptions import CategoriaNotFoundError

class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def create(self, db:Session, categoria: CategoriaCreate):
        return self.repository.create(db, categoria.model_dump())

    def list(self, db:Session):
        return self.repository.list(db)

    def _get_or_raise(self, db:Session, categoria_id: int):
        categoria = self.repository.get(db, categoria_id)
        if not categoria:
            raise CategoriaNotFoundError()
        return categoria

    def get(self, db:Session, categoria_id: int):
        return self._get_or_raise(db, categoria_id)

    def buscar_por_nome(self, db:Session, nome: str):
        return self.repository.buscar_por_nome(db, nome)
