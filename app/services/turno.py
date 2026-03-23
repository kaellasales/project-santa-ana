from sqlalchemy.orm import Session
from app.repositories.turno import TurnoRepository
from app.repositories.venda import VendaRepository
from app.schemas.turno import TurnoAbrir, TurnoFechar
from app.models.turno import TurnoStatus
from app.models.venda import VendaStatus
from app.models.pagamento import TipoPagamento
from datetime import datetime, timezone


class TurnoService:
    def __init__(self, repository: TurnoRepository, venda_repository: VendaRepository):
        self.repository = repository
        self.venda_repository = venda_repository

    def abrir(self, db: Session, dados: TurnoAbrir, usuario_id: int):
        turno_ativo = self.repository.get_turno_ativo(db, usuario_id)
        if turno_ativo:
            raise ValueError("Usuário já possui um turno aberto")

        obj = self.repository.create(db, {
            "usuario_id": usuario_id,
            "valor_inicial": dados.valor_inicial,
            "status": TurnoStatus.ABERTO,
        })
        db.commit()
        db.refresh(obj)
        return obj

    def get_turno_ativo(self, db: Session, usuario_id: int):
        turno = self.repository.get_turno_ativo(db, usuario_id)
        if turno:
            turno.usuario_nome = turno.usuario.nome if turno.usuario else None
        return turno

    def fechar(self, db: Session, dados: TurnoFechar, usuario_id: int):
        turno = self.repository.get_turno_ativo(db, usuario_id)
        if not turno:
            raise ValueError("Nenhum turno aberto encontrado")

        # Busca vendas concluídas do turno
        vendas = [v for v in turno.vendas if v.status == VendaStatus.CONCLUIDA]

        # Totais gerais
        total_vendas = sum(v.total for v in vendas)
        quantidade_vendas = len(vendas)

        # Breakdown por forma de pagamento
        por_forma_pagamento = self._calcular_por_forma_pagamento(vendas)

        # Conferência de caixa
        valor_esperado = turno.valor_inicial + total_vendas
        diferenca = round(valor_esperado - dados.valor_informado, 2)

        # Persiste o fechamento
        self.repository.update(db, turno, {
            "status": TurnoStatus.FECHADO,
            "data_fechamento": datetime.now(timezone.utc),
            "total_vendas": total_vendas,
            "quantidade_vendas": quantidade_vendas,
            "valor_informado": dados.valor_informado,
            "valor_esperado": valor_esperado,
            "diferenca": diferenca,
            "observacoes": dados.observacoes,
        })
        db.commit()
        db.refresh(turno)

        # Monta o resumo com o breakdown (não persiste)
        resumo = turno.__dict__.copy()
        resumo["por_forma_pagamento"] = por_forma_pagamento
        return resumo

    def listar_por_usuario(self, db: Session, usuario_id: int):
        return self.repository.listar_por_usuario(db, usuario_id)
    
    def listar_todos(self, db: Session):
        turnos = self.repository.listar_todos(db)
        for turno in turnos:
            turno.usuario_nome = turno.usuario.nome if turno.usuario else None
        return turnos

    def _calcular_por_forma_pagamento(self, vendas) -> dict[str, float]:
        totais = {
            "Dinheiro": 0.0,
            "Cartão Débito": 0.0,
            "Cartão Crédito": 0.0,
            "Pix": 0.0,
        }
        mapa = {
            TipoPagamento.DINHEIRO: "Dinheiro",
            TipoPagamento.CARTAO_DEBITO: "Cartão Débito",
            TipoPagamento.CARTAO_CREDITO: "Cartão Crédito",
            TipoPagamento.PIX: "Pix",
        }
        for venda in vendas:
            if venda.forma_pagamento:
                chave = mapa.get(venda.forma_pagamento.tipo)
                if chave:
                    totais[chave] += venda.total
        return totais

    def atualizar_totais(self, db: Session, turno_id: int):
        turno = self.repository.get(db, turno_id)
        if not turno:
            return

        vendas_concluidas = [v for v in turno.vendas if v.status == VendaStatus.CONCLUIDA]
        total_vendas = sum(v.total for v in vendas_concluidas)
        quantidade_vendas = len(vendas_concluidas)

        self.repository.update(db, turno, {
            "total_vendas": total_vendas,
            "quantidade_vendas": quantidade_vendas,
        })