from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.repositories.venda import VendaRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.schemas.venda import VendaCreate, VendaUpdate
from app.core.exceptions import VendaNotFoundError
from app.models.venda import VendaStatus
from app.models.movimentacao import TipoMovimentacao, MotivoMovimentacao, MovimentacaoEstoque
from app.repositories.turno import TurnoRepository
from app.core.exceptions import TurnoNotFoundError
from app.services.turno import TurnoService

class VendaService:
    def __init__(self, repository_venda: VendaRepository, repository_produto: ProdutoRepository, 
    repository_movimentacao: MovimentacaoEstoqueRepository, repository_turno: TurnoRepository
    ):
        self.repository = repository_venda
        self.produto_repository = repository_produto
        self.movimentacao_repository = repository_movimentacao
        self.turno_repository = repository_turno
        self.turno_service = TurnoService(repository_turno, repository_venda)

    def create(self, db: Session, venda: VendaCreate, usuario_id: int):
        turno = self.turno_repository.get_turno_ativo(db, usuario_id)
        if not turno:
            raise TurnoNotFoundError()

        dados = venda.model_dump()
        dados["total"] = 0.0
        dados["usuario_id"] = usuario_id
        dados["turno_id"] = turno.id
        obj = self.repository.create(db, dados)
        db.commit()
        db.refresh(obj)
        return obj

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.list(db, skip=skip, limit=limit)

    def get(self, db: Session, venda_id: int):
        venda = self.repository.get(db, venda_id)
        if not venda:
            raise VendaNotFoundError()
        return venda

    def list_por_data(self, db: Session, data_inicio: datetime, data_fim: datetime):
        return self.repository.buscar_por_data(db, data_inicio, data_fim)

    def list_ultimas_vendas(self, db: Session, limite: int = 10):
        return self.repository.buscar_ultimas_vendas(db, limite)

    def _recalcular_total(self, db: Session, venda_id: int):
        venda = self.get(db, venda_id)
        subtotal = sum(item.subtotal for item in venda.itens)
        subtotal += venda.acrescimo or 0
        subtotal -= venda.desconto or 0
        venda.total = subtotal
        db.flush()
        db.refresh(venda)
        return venda

    def atualizar_total(self, db: Session, venda_id: int):
        resultado = self._recalcular_total(db, venda_id)
        db.commit()
        return resultado
        
    def update(self, db: Session, venda_id: int, venda_atualizada: VendaUpdate):
        venda = self.get(db, venda_id)
        dados = venda_atualizada.model_dump(exclude_unset=True)
        
        if venda.forma_pagamento and ('acrescimo' in dados or 'desconto' in dados):
            raise ValueError("Não é possível alterar acréscimo/desconto após forma de pagamento ser criada")
        
        self.repository.update(db, venda, dados)
        resultado = self._recalcular_total(db, venda_id)
        db.commit()
        return resultado

    def finalizar(self, db: Session, venda_id: int):
        venda = self.get(db, venda_id)

        if venda.status != VendaStatus.ABERTA:
            raise ValueError(f"Venda não pode ser finalizada. Status atual: {venda.status.value}")

        if not venda.itens:
            raise ValueError("Venda não pode ser finalizada sem itens")

        if not venda.forma_pagamento:
            raise ValueError("Venda não pode ser finalizada sem forma de pagamento")

        for item in venda.itens:
            self.movimentacao_repository.create(db, {
                "produto_id": item.produto_id,
                "venda_id": venda_id,
                "tipo": TipoMovimentacao.SAIDA,
                "motivo": MotivoMovimentacao.VENDA,
                "quantidade": item.quantidade
            })

        venda = self._recalcular_total(db, venda_id)
        venda.status = VendaStatus.CONCLUIDA
        venda.data_venda = datetime.now(timezone.utc)
        self.turno_service.atualizar_totais(db, venda.turno_id)
        db.commit()
        db.refresh(venda)
        return venda

    def cancelar(self, db: Session, venda_id: int):
        venda = self.get(db, venda_id)

        if venda.status == VendaStatus.CANCELADA:
            raise ValueError("Venda já está cancelada")

        if venda.status == VendaStatus.CONCLUIDA:
            agora = datetime.now(timezone.utc)
            data_venda = venda.data_venda.replace(tzinfo=timezone.utc)
            if agora - data_venda > timedelta(minutes=20):
                raise ValueError("Venda não pode ser cancelada após 20 minutos da finalização")

        for item in venda.itens:
            produto = self.produto_repository.get(db, item.produto_id)
            if produto:
                produto.estoque += item.quantidade
                db.add(produto)
            self.movimentacao_repository.create(db, {
                "produto_id": item.produto_id,
                "venda_id": venda_id,
                "tipo": TipoMovimentacao.ENTRADA,
                "motivo": MotivoMovimentacao.DEVOLUCAO,
                "quantidade": item.quantidade
            })

        venda.status = VendaStatus.CANCELADA
        db.add(venda)
        self.turno_service.atualizar_totais(db, venda.turno_id)
        db.commit()
        db.refresh(venda)
        return venda