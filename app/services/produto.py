from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.produto import ProdutoRepository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    def create(self, db:Session, produto: ProdutoCreate):
        return self.repository.create(db, produto.model_dump())

    def list(self, db:Session):
        return self.repository.list(db)

    def get(self, db: Session, produto_id: int):
        produto = self.repository.get(db, produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
        return produto
    
    def update(self, db:Session, produto_id: int, update_produto: ProdutoUpdate):
        produto = self.repository.get(db, produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return self.repository.update(db, produto, update_produto)

    def delete(self, db:Session, produto_id: int):
        produto = self.repository.get(db, produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return self.repository.delete(db, produto_id)
    
    def buscar_por_nome(self, db:Session, nome: str):
        return self.repository.buscar_por_nome(db, nome)
