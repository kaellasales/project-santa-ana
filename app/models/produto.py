from sqlalchemy import Column, Integer, String,  ForeignKey, Numeric, CheckConstraint
from app.core.database import Base
from sqlalchemy.orm import relationship


class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_barra = Column(String(50), unique=True, index=True, nullable=True)
    nome = Column(String(100), index=True, nullable=False)
    preco_compra = Column(Numeric(10,2), nullable=True)
    preco_venda = Column(Numeric(10,2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False)
    
    categoria = relationship("Categoria", back_populates="produtos")
    itens_venda = relationship("ItemVenda", back_populates="produto")

    __table_args__ = (
        CheckConstraint('estoque >= 0', name='check_estoque_non_negative'),
    )

    def __repr__(self):
        return f"<Produto(id={self.id}, nome={self.nome}, preco_venda={self.preco_venda}, estoque={self.estoque})>"