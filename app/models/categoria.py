from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, CheckConstraint
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)

    produtos = relationship("Produto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome={self.nome})>"
    