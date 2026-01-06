from app.core.models import Produto as produtoModel
from .base import BaseRepository


class ProdutoRepository(BaseRepository):

    def buscar_por_nome(self, nome: str):
        return self.db.query(produtoModel).filter(produtoModel.nome.ilike(f"%{nome}%")).all()