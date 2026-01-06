from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate
from fastapi import HTTPException

class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def create(self, categoria: CategoriaCreate):
        return self.repository.create(categoria.model_dump())

    def list(self):
        return self.repository.list()

    def get(self, categoria_id: int):
        categoria = self.repository.get(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return categoria

    def buscar_por_nome(self, nome: str):
        return self.repository.buscar_por_nome(nome)
