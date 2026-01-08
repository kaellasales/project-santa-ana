from app.core.models import Produto as produtoModel
from sqlalchemy.orm import Session
from .base import BaseRepository


class ProdutoRepository(BaseRepository[produtoModel]):
    def __init__(self):
        super().__init__(produtoModel)

    def buscar_por_nome(self, db:Session, nome: str):
        return db.query(produtoModel).filter(produtoModel.nome.ilike(f"%{nome}%")).all()