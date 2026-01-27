from sqlalchemy.orm import Session
from app.models.itemVenda import ItemVenda as ItemVendaModel
from app.schemas.itemVenda import ItemVendaCreate
from .base import BaseRepository

class ItemVendaRepository(BaseRepository[ItemVendaModel]):
    def __init__(self):
        super().__init__(ItemVendaModel)
    
    def buscar_por_venda(self, db: Session, venda_id: int):
        return db.query(ItemVendaModel).filter(ItemVendaModel.venda_id == venda_id).all()
    
    def buscar_por_produto(self, db: Session, produto_id: int):
        return db.query(ItemVendaModel).filter(ItemVendaModel.produto_id == produto_id).all()
    
    def buscar_por_venda_e_produto(self, db: Session, venda_id: int, produto_id: int):
        return db.query(ItemVendaModel).filter(
            ItemVendaModel.venda_id == venda_id,
            ItemVendaModel.produto_id == produto_id
        ).first()