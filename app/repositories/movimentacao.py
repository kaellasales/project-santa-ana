from app.repositories.base import BaseRepository
from app.models.movimentacao import MovimentacaoEstoque
from sqlalchemy.orm import Session
from datetime import datetime


class MovimentacaoEstoqueRepository(BaseRepository[MovimentacaoEstoque]):
    def __init__(self):
        super().__init__(MovimentacaoEstoque)

    def listar_por_produto(self, db: Session, produto_id: int):
        return db.query(MovimentacaoEstoque).filter(
            MovimentacaoEstoque.produto_id == produto_id
        ).order_by(MovimentacaoEstoque.data.desc()).all()

    def listar_por_venda(self, db: Session, venda_id: int):
        return db.query(MovimentacaoEstoque).filter(
            MovimentacaoEstoque.venda_id == venda_id
        ).all()

    def listar_por_periodo(self, db: Session, data_inicio: datetime, data_fim: datetime, tipo=None):
        query = db.query(MovimentacaoEstoque).filter(
            MovimentacaoEstoque.data >= data_inicio,
            MovimentacaoEstoque.data <= data_fim
        )
        if tipo:
            query = query.filter(MovimentacaoEstoque.tipo == tipo)
        return query.order_by(MovimentacaoEstoque.data.desc()).all()

