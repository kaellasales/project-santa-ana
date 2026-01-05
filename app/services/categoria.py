from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate
from fastapi import HTTPException

class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def criar(self, categoria: CategoriaCreate):
        return self.repository.criar(categoria)

    def listar_todas(self):
        return self.repository.listar_todas()

    def buscar_por_id(self, categoria_id: int):
        categoria = self.repository.buscar_por_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return categoria

    def buscar_por_nome(self, nome: str):
        return self.repository.buscar_por_nome(nome)

    def atualizar(self, categoria_id: int, novo_nome: str):
        categoria = self.repository.buscar_por_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return self.repository.atualizar(categoria_id, novo_nome)

    def deletar(self, categoria_id: int):
        categoria = self.repository.buscar_por_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return self.repository.deletar(categoria_id)