from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SAEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base
from enum import Enum as PyEnum


class TipoMovimentacao(PyEnum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MotivoMovimentacao(PyEnum):
    CADASTRO_INICIAL = "CADASTRO_INICIAL"
    VENDA = "VENDA"
    AJUSTE = "AJUSTE"
    PERDA = "PERDA"
    COMPRA = "COMPRA"
    DEVOLUCAO = "DEVOLUCAO"


class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False)
    venda_id = Column(Integer, ForeignKey("vendas.id", ondelete="SET NULL"), nullable=True)
    tipo = Column(SAEnum(TipoMovimentacao), nullable=False)
    motivo = Column(SAEnum(MotivoMovimentacao), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    produto = relationship("Produto", back_populates="movimentacoes")
    venda = relationship("Venda", back_populates="movimentacoes")