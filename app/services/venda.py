from sqlalchemy.orm import Session
from app.repositories.venda import VendaRepository
# from app.repositories.usuario import UsuarioRepository
from app.schemas.venda import VendaCreate, VendaUpdate
from app.core.exceptions import VendaNotFoundError, UsuarioNotFoundError
from datetime import datetime

class VendaService:
    def __init__(self, repository_venda: VendaRepository):
        self.repository = repository_venda
        # self.usuario_repository = UsuarioRepository()
    
    # def _validar_usuario_existe(self, db: Session, usuario_id: int):
    #     usuario = self.usuario_repository.get(db, usuario_id)
    #     if not usuario:
    #         raise UsuarioNotFoundError()
    #     return usuario
    
    def create(self, db: Session, venda: VendaCreate):
        # self._validar_usuario_existe(db, venda.usuario_id)
        
        dados = venda.model_dump()
        dados["total"] = 0.0  # Será atualizado ao adicionar itens
        
        return self.repository.create(db, dados)
    
    def list(self, db: Session):
        return self.repository.list(db)
    
    def get(self, db: Session, venda_id: int):
        venda = self.repository.get(db, venda_id)
        if not venda:
            raise VendaNotFoundError()
        return venda
    
    # def list_por_usuario(self, db: Session, usuario_id: int):
    #     self._validar_usuario_existe(db, usuario_id)
    #     return self.repository.buscar_por_usuario(db, usuario_id)
    
    def list_por_data(self, db: Session, data_inicio: datetime, data_fim: datetime):
        return self.repository.buscar_por_data(db, data_inicio, data_fim)
    
    def list_ultimas_vendas(self, db: Session, limite: int = 10):
        return self.repository.buscar_ultimas_vendas(db, limite)
    
    # def list_por_usuario_e_data(self, db: Session, usuario_id: int, data_inicio: datetime, data_fim: datetime):
    #     self._validar_usuario_existe(db, usuario_id)
    #     return self.repository.buscar_por_usuario_e_data(db, usuario_id, data_inicio, data_fim)
    
    # def total_vendas_usuario(self, db: Session, usuario_id: int):
    #     self._validar_usuario_existe(db, usuario_id)
    #     return self.repository.total_vendas_usuario(db, usuario_id)
    
    def update(self, db: Session, venda_id: int, venda_atualizada: VendaUpdate):
        venda = self.get(db, venda_id)
        
        # if venda_atualizada.usuario_id is not None:
        #     self._validar_usuario_existe(db, venda_atualizada.usuario_id)
        #     venda.usuario_id = venda_atualizada.usuario_id
        
        return self.repository.update(db, venda_id, venda.__dict__)
    
    def atualizar_total(self, db: Session, venda_id: int):
        """Recalcula o total da venda baseado nos itens"""
        venda = self.get(db, venda_id)
        venda.total = sum(item.subtotal for item in venda.itens)
        db.commit()
        db.refresh(venda)
        return venda
    
    # def cancelar_venda(self, db: Session, venda_id: int):
    #     """Cancela a venda (soft delete)"""
    #     venda = self.get(db, venda_id)
    #     # Se você quiser implementar soft delete, adicione um campo 'ativo' no modelo
    #     return self.repository.delete(db, venda_id)
    
    def delete(self, db: Session, venda_id: int):
        venda = self.get(db, venda_id)
        return self.repository.delete(db, venda_id)