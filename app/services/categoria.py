from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate


class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def create(self, db:Session, categoria: CategoriaCreate):
        return self.repository.create(db, categoria.model_dump())

    def list(self, db:Session):
        return self.repository.list(db)

    def get(self, db:Session, categoria_id: int):
        categoria = self.repository.get(db, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada.")
        return categoria

    def buscar_por_nome(self, db:Session, nome: str):
        return self.repository.buscar_por_nome(db, nome)
