from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship


class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    produtos = relationship("Produto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome={self.nome})>"
    