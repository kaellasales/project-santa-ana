from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.relatorio import RelatorioRepository


class RelatorioService:
    def __init__(self, repository: RelatorioRepository):
        self.repository = repository

    def relatorio_vendas(self, db: Session, data_inicio: datetime, data_fim: datetime):
        resumo = self.repository.resumo_vendas(db, data_inicio, data_fim)
        por_forma = self.repository.por_forma_pagamento(db, data_inicio, data_fim)
        mais_vendidos = self.repository.produtos_mais_vendidos(db, data_inicio, data_fim)

        forma_pagamento = {"DINHEIRO": 0.0, "CARTAO_DEBITO": 0.0, "CARTAO_CREDITO": 0.0, "PIX": 0.0}
        for item in por_forma:
            forma_pagamento[item.tipo.value] = float(item.total or 0)

        return {
            "total_vendas": float(resumo.total_vendas or 0),
            "num_transacoes": resumo.num_transacoes or 0,
            "ticket_medio": float(resumo.ticket_medio or 0),
            "por_forma_pagamento": forma_pagamento,
            "produtos_mais_vendidos": [
                {"nome": p.nome, "quantidade_total": p.quantidade_total}
                for p in mais_vendidos
            ]
        }

    def relatorio_estoque(self, db: Session):
        resumo = self.repository.resumo_estoque(db)
        listagem = self.repository.listagem_produtos(db)

        return {
            "produtos_ativos": resumo["produtos_ativos"],
            "inativos": resumo["inativos"],
            "estoque_baixo": resumo["estoque_baixo"],
            "listagem": [
                {
                    "id": p.id,
                    "nome": p.nome,
                    "categoria": p.categoria_nome,
                    "estoque": p.estoque,
                    "estoque_minimo": p.estoque_minimo,
                    "preco_compra": float(p.preco_compra) if p.preco_compra else None,
                    "preco_venda": float(p.preco_venda)
                }
                for p in listagem
            ]
        }