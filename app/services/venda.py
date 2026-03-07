from sqlalchemy.orm import Session
from app.repositories.venda import VendaRepository
from app.repositories.produto import ProdutoRepository
from app.schemas.venda import VendaCreate, VendaUpdate
from app.core.exceptions import VendaNotFoundError
from app.models.venda import VendaStatus
from datetime import datetime, timezone, timedelta


class VendaService:
    def __init__(self, repository_venda: VendaRepository, repository_produto: ProdutoRepository):
        self.repository = repository_venda
        self.produto_repository = repository_produto

    def create(self, db: Session, venda: VendaCreate):
        dados = venda.model_dump()
        dados["total"] = 0.0
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

    def atualizar_total(self, db: Session, venda_id: int):
        venda = self.get(db, venda_id)
        subtotal = sum(item.subtotal for item in venda.itens)
        subtotal += venda.acrescimo or 0
        subtotal -= venda.desconto or 0
        venda.total = subtotal
        db.commit()
        db.refresh(venda)
        return venda

    def update(self, db: Session, venda_id: int, venda_atualizada: VendaUpdate):
        venda = self.get(db, venda_id)
        dados = venda_atualizada.model_dump(exclude_unset=True)
        
        if venda.forma_pagamento and ('acrescimo' in dados or 'desconto' in dados):
            raise ValueError("Não é possível alterar acréscimo/desconto após forma de pagamento ser criada")
        
        self.repository.update(db, venda, dados)
        db.commit()
        return self.atualizar_total(db, venda_id)

    def finalizar(self, db: Session, venda_id: int):
        venda = self.get(db, venda_id)

        if venda.status != VendaStatus.ABERTA:
            raise ValueError(f"Venda não pode ser finalizada. Status atual: {venda.status.value}")

        if not venda.itens:
            raise ValueError("Venda não pode ser finalizada sem itens")

        if not venda.forma_pagamento:
            raise ValueError("Venda não pode ser finalizada sem forma de pagamento")

        venda = self.atualizar_total(db, venda_id)
        venda.status = VendaStatus.CONCLUIDA
        venda.data_venda = datetime.now(timezone.utc)
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

        venda.status = VendaStatus.CANCELADA
        db.add(venda)
        db.commit()
        db.refresh(venda)
        return venda