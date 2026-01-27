

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    # usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Float, default=0.0, nullable=False)
    
    # Relacionamentos
    # usuario = relationship("Usuario", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    # formas_pagamento = relationship("FormaDePagamento", back_populates="vendas", cascade="all, delete-orphan")
    
    def __repr__(self):
        # return f"<Venda(id={self.id}, usuario_id={self.usuario_id}, total={self.total})>"
        return f"<Venda(id={self.id}, total={self.total})>"
