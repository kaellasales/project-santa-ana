from sqlalchemy import update
from sqlalchemy.orm import Session
from app.models.produto import Produto as produtoModel
from .base import BaseRepository

class ProdutoRepository(BaseRepository[produtoModel]):
    def __init__(self):
        super().__init__(produtoModel)

    def buscar_por_nome(self, db:Session, nome: str):
        return db.query(produtoModel).filter(produtoModel.nome.ilike(f"%{nome}%")).all()

    def alterar_estoque(self, db: Session, produto_id: int, delta: int):
        """
        Muda o estoque de forma atômica.
        delta: positivo para entrada, negativo para saída.
        Retorna: True se alterou, False se produto não existe.
        """
        stmt = (
            update(produtoModel)
            .where(produtoModel.id == produto_id)
            .values(estoque=produtoModel.estoque + delta)
            .execution_options(synchronize_session="fetch") 
        )
        result = db.execute(stmt)
        db.flush() 
        return result.rowcount > 0