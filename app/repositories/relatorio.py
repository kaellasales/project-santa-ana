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

    
    def resumo_estoque(self, db: Session):
        produtos_ativos = db.query(func.count(Produto.id)).filter(Produto.ativo).scalar()
        inativos = db.query(func.count(Produto.id)).filter(~Produto.ativo).scalar()
        estoque_baixo = db.query(func.count(Produto.id)).filter(
            Produto.ativo,
            Produto.estoque <= Produto.estoque_minimo
        ).scalar()

        return {
            "produtos_ativos": produtos_ativos,
            "inativos": inativos,
            "estoque_baixo": estoque_baixo
        }

    def listagem_produtos(self, db: Session):
        return db.query(Produto).filter(Produto.ativo).order_by(Produto.nome).all()

    def margem_por_produto(self, db: Session, data_inicio: datetime, data_fim: datetime):
        return db.query(
            Produto.nome,
            func.sum(ItemVenda.quantidade).label("qtd_vendida"),
            func.sum(ItemVenda.subtotal).label("receita"),
            func.sum(Produto.preco_compra * ItemVenda.quantidade).label("custo")
        ).join(ItemVenda, ItemVenda.produto_id == Produto.id
        ).join(Venda, Venda.id == ItemVenda.venda_id).filter(
            Venda.status == VendaStatus.CONCLUIDA,
            Venda.data_venda.between(data_inicio, data_fim)
        ).group_by(Produto.nome).all()