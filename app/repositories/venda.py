
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.venda import Venda as VendaModel
from app.schemas.venda import VendaCreate
from .base import BaseRepository
from datetime import datetime, timedelta

class VendaRepository(BaseRepository[VendaModel]):
    def __init__(self):
        super().__init__(VendaModel)
    
    # def buscar_por_usuario(self, db: Session, usuario_id: int):
    #     return db.query(VendaModel).filter(VendaModel.usuario_id == usuario_id).all()
    
    def buscar_por_data(self, db: Session, data_inicio: datetime, data_fim: datetime):
        return db.query(VendaModel).filter(
            VendaModel.data_venda.between(data_inicio, data_fim)
        ).all()
    
    def buscar_ultimas_vendas(self, db: Session, limite: int = 10):
        return db.query(VendaModel).order_by(desc(VendaModel.data_venda)).limit(limite).all()
    
    # def buscar_por_usuario_e_data(self, db: Session, usuario_id: int, data_inicio: datetime, data_fim: datetime):
    #     return db.query(VendaModel).filter(
    #         VendaModel.usuario_id == usuario_id,
    #         VendaModel.data_venda.between(data_inicio, data_fim)
    #     ).all()
    
    # def total_vendas_usuario(self, db: Session, usuario_id: int):
    #     resultado = db.query(VendaModel).filter(VendaModel.usuario_id == usuario_id).all()
    #     return sum(venda.total for venda in resultado)