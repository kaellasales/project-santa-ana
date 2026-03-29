from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base
from enum import Enum as PyEnum
import uuid                                    
from sqlalchemy.dialects.postgresql import UUID 


class TurnoStatus(PyEnum):
    ABERTO = "ABERTO"
    FECHADO = "FECHADO"


class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    id_offline = Column(UUID(as_uuid=True), unique=True, nullable=True, index=True)  
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(SAEnum(TurnoStatus), default=TurnoStatus.ABERTO, nullable=False)

    data_abertura = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    data_fechamento = Column(DateTime(timezone=True), nullable=True)

    valor_inicial = Column(Float, nullable=False)
    valor_informado = Column(Float, nullable=True)
    valor_esperado = Column(Float, nullable=True)
    diferenca = Column(Float, nullable=True)

    total_vendas = Column(Float, default=0.0, nullable=False)
    quantidade_vendas = Column(Integer, default=0, nullable=False)

    observacoes = Column(String(500), nullable=True)

    usuario = relationship("Usuario", back_populates="turnos")
    vendas = relationship("Venda", back_populates="turno")

    def __repr__(self):
        return f"<Turno(id={self.id}, usuario_id={self.usuario_id}, status={self.status})>"