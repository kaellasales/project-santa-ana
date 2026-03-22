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

    def relatorio_margem(self, db: Session, data_inicio: datetime, data_fim: datetime):
        produtos = self.repository.margem_por_produto(db, data_inicio, data_fim)

        receita_bruta = sum(float(p.receita or 0) for p in produtos)
        custo_total = sum(float(p.custo or 0) for p in produtos)
        lucro_bruto = receita_bruta - custo_total
        margem_percentual = round((lucro_bruto / receita_bruta) * 100, 2) if receita_bruta > 0 else 0

        return {
            "receita_bruta": receita_bruta,
            "custo_total": custo_total,
            "lucro_bruto": lucro_bruto,
            "margem_percentual": margem_percentual,
            "detalhamento": [
                {
                    "nome": p.nome,
                    "qtd_vendida": p.qtd_vendida,
                    "receita": float(p.receita or 0),
                    "custo": float(p.custo or 0),
                    "lucro": float(p.receita or 0) - float(p.custo or 0),
                    "margem_percentual": round(((float(p.receita or 0) - float(p.custo or 0)) / float(p.receita or 1)) * 100, 2)
                }
                for p in produtos
            ]
        }

    def relatorio_caixa(self, db: Session, data_inicio: datetime, data_fim: datetime):
        turnos = self.repository.resumo_caixa(db, data_inicio, data_fim)

        total_faturado = sum(t.total_vendas or 0 for t in turnos)
        diferenca_total = sum(t.diferenca or 0 for t in turnos)

        return {
            "turnos_no_periodo": len(turnos),
            "total_faturado": total_faturado,
            "diferenca_total": diferenca_total,
            "historico": [
                {
                    "id": t.id,
                    "abertura": t.data_abertura,
                    "fechamento": t.data_fechamento,
                    "valor_inicial": t.valor_inicial,
                    "total_faturado": t.total_vendas,
                    "diferenca": t.diferenca,
                    "status": t.status.value
                }
                for t in turnos
            ]
        }

    def relatorio_geral(self, db: Session, data_inicio: datetime, data_fim: datetime):
        resumo = self.repository.resumo_vendas(db, data_inicio, data_fim)
        por_forma = self.repository.por_forma_pagamento(db, data_inicio, data_fim)
        mais_vendidos = self.repository.produtos_mais_vendidos(db, data_inicio, data_fim)
        margem = self.repository.margem_por_produto(db, data_inicio, data_fim)

        receita_bruta = sum(float(p.receita or 0) for p in margem)
        custo_total = sum(float(p.custo or 0) for p in margem)
        lucro_bruto = receita_bruta - custo_total

        forma_pagamento = {"DINHEIRO": 0.0, "CARTAO_DEBITO": 0.0, "CARTAO_CREDITO": 0.0, "PIX": 0.0}
        for item in por_forma:
            forma_pagamento[item.tipo.value] = float(item.total or 0)

        produto_top = mais_vendidos[0].nome if mais_vendidos else None

        return {
            "total_vendas": float(resumo.total_vendas or 0),
            "ticket_medio": float(resumo.ticket_medio or 0),
            "lucro_bruto": lucro_bruto,
            "produto_top": produto_top,
            "por_forma_pagamento": forma_pagamento,
            "top_produtos": [
                {"nome": p.nome, "quantidade_total": p.quantidade_total}
                for p in mais_vendidos
            ]
        }