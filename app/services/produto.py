from app.repositories.produto import ProdutoRepository
from app.schemas.produto import ProdutoCreate
from fastapi import HTTPException

class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    def create(self, produto: ProdutoCreate):
        return self.repository.create(produto.model_dump())

    def list(self):
        return self.repository.list()

    def get(self, produto_id: int):
        produto = self.repository.get(produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
        return produto
    
    def delete(self, produto_id: int):
        produto = self.repository.get(produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return self.repository.delete(produto_id)
    
    def buscar_por_nome(self, nome: str):
        return self.repository.buscar_por_nome(nome)
