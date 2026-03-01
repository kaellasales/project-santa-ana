from sqlalchemy.orm import Session
from app.repositories.pagamento import FormaPagamentoRepository
from app.repositories.venda import VendaRepository
from app.schemas.pagamento import FormaPagamentoCreate
from app.models.pagamento import TipoPagamento
from app.core.exceptions import VendaNotFoundError

class FormaPagamentoService:
    def __init__(self, repo_forma_pagamento: FormaPagamentoRepository, repo_venda: VendaRepository):
        self.repository = repo_forma_pagamento
        self.venda_repository = repo_venda

    def create(self, db: Session, venda_id: int, forma: FormaPagamentoCreate):
        venda = self.venda_repository.get(db, venda_id)
        if not venda:
            raise VendaNotFoundError()

        if venda.forma_pagamento:
            raise ValueError("Venda já possui forma de pagamento registrada")

        if forma.valor_recebido < venda.total:
            raise ValueError(f"Valor recebido insuficiente. Total da venda: {venda.total}")

        troco = 0.0
        if forma.tipo == TipoPagamento.DINHEIRO:
            troco = round(forma.valor_recebido - venda.total, 2)

        dados = forma.model_dump()
        dados["venda_id"] = venda_id
        dados["troco"] = troco

        obj = self.repository.create(db, dados)
        db.commit()
        db.refresh(obj)
        return obj

    def get_por_venda(self, db: Session, venda_id: int):
        venda = self.venda_repository.get(db, venda_id)
        if not venda:
            raise VendaNotFoundError()
        return venda.forma_pagamento