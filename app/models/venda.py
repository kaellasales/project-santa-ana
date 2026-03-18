from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from enum import Enum as PyEnum


class VendaStatus(PyEnum):
    ABERTA = "ABERTA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"


class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_venda = Column(DateTime(timezone=True), nullable=True) 
    total = Column(Float, default=0.0, nullable=False)
    status = Column(SAEnum(VendaStatus), default=VendaStatus.ABERTA, nullable=False)
    desconto = Column(Float, default=0.0, nullable=False)
    acrescimo = Column(Float, default=0.0, nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    forma_pagamento = relationship("FormaPagamento", back_populates="venda", uselist=False)
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="venda")
    
    def __repr__(self):
        # return f"<Venda(id={self.id}, usuario_id={self.usuario_id}, total={self.total})>"
        return f"<Venda(id={self.id}, total={self.total})>"
