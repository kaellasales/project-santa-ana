from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.venda import Venda, VendaStatus
from app.models.pagamento import FormaPagamento, TipoPagamento
from app.models.itemVenda import ItemVenda
from app.models.produto import Produto
from datetime import datetime


class RelatorioRepository:

    def resumo_vendas(self, db: Session, data_inicio: datetime, data_fim: datetime):
        resultado = db.query(
            func.count(Venda.id).label("num_transacoes"),
            func.sum(Venda.total).label("total_vendas"),
            func.avg(Venda.total).label("ticket_medio")
        ).filter(
            Venda.status == VendaStatus.CONCLUIDA,
            Venda.data_venda.between(data_inicio, data_fim)
        ).first()
        return resultado

    def por_forma_pagamento(self, db: Session, data_inicio: datetime, data_fim: datetime):
        return db.query(
            FormaPagamento.tipo,
            func.sum(Venda.total).label("total")
        ).join(Venda, Venda.id == FormaPagamento.venda_id).filter(
            Venda.status == VendaStatus.CONCLUIDA,
            Venda.data_venda.between(data_inicio, data_fim)
        ).group_by(FormaPagamento.tipo).all()

    def produtos_mais_vendidos(self, db: Session, data_inicio: datetime, data_fim: datetime, limite: int = 3):
        return db.query(
            Produto.nome,
            func.sum(ItemVenda.quantidade).label("quantidade_total")
        ).join(ItemVenda, ItemVenda.produto_id == Produto.id
        ).join(Venda, Venda.id == ItemVenda.venda_id).filter(
            Venda.status == VendaStatus.CONCLUIDA,
            Venda.data_venda.between(data_inicio, data_fim)
        ).group_by(Produto.nome).order_by(func.sum(ItemVenda.quantidade).desc()).limit(limite).all()