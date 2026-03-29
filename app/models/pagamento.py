from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum as SAEnum
from enum import Enum as PyEnum
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid                                    
from sqlalchemy.dialects.postgresql import UUID 


class TipoPagamento(PyEnum):
    DINHEIRO = "DINHEIRO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    PIX = "PIX"


class FormaPagamento(Base):
    __tablename__ = "formas_pagamento"

    id = Column(Integer, primary_key=True, index=True)
    id_offline = Column(UUID(as_uuid=True), unique=True, nullable=True, index=True)  
    venda_id = Column(Integer, ForeignKey("vendas.id", ondelete="RESTRICT"), nullable=False)
    tipo = Column(SAEnum(TipoPagamento), nullable=False)
    valor_recebido = Column(Float, nullable=False)
    troco = Column(Float, default=0.0, nullable=False)

    venda = relationship("Venda", back_populates="forma_pagamento")

    def __repr__(self):
        return f"<FormaPagamento(id={self.id}, tipo={self.tipo}, troco={self.troco})>"