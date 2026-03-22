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