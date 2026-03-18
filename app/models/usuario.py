from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class RoleUsuario(PyEnum):
    ADMIN = "ADMIN"
    VENDEDOR = "VENDEDOR"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    role = Column(SAEnum(RoleUsuario), default=RoleUsuario.VENDEDOR, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    vendas = relationship("Venda", back_populates="usuario")
    turnos = relationship("Turno", back_populates="usuario")
    def __repr__(self):
        return f"<Usuario(id={self.id}, username={self.username}, role={self.role})>"
