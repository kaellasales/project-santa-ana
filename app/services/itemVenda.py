from sqlalchemy.orm import Session
from app.repositories.itemVenda import ItemVendaRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.venda import VendaRepository
from app.schemas.itemVenda import ItemVendaCreate, ItemVendaUpdate
from app.core.exceptions import ItemVendaNotFoundError, VendaNotFoundError, ProdutoNotFoundError

class ItemVendaService:
    def __init__(self, repo_item_venda: ItemVendaRepository, repo_produto: ProdutoRepository, repo_venda: VendaRepository):
        self.repository = repo_item_venda
        self.produto_repository = repo_produto
        self.venda_repository = repo_venda
    
    def _validar_venda_existe(self, db: Session, venda_id: int):
        venda = self.venda_repository.get(db, venda_id)
        if not venda:
            raise VendaNotFoundError()
        return venda
    
    def _validar_produto_existe(self, db: Session, produto_id: int):
        produto = self.produto_repository.get(db, produto_id)
        if not produto:
            raise ProdutoNotFoundError()
        return produto
    
    def _calcular_subtotal(self, quantidade: int, preco_unitario: float) -> float:
        return quantidade * preco_unitario
    
    def create(self, db: Session, venda_id: int, item: ItemVendaCreate):
        self._validar_venda_existe(db, venda_id)
        produto = self._validar_produto_existe(db, item.produto_id)
        
        # Validar estoque
        if produto.estoque < item.quantidade:
            raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque}")
        
        subtotal = self._calcular_subtotal(item.quantidade, item.preco_unitario)
        
        dados = item.model_dump()
        dados["venda_id"] = venda_id
        dados["subtotal"] = subtotal
        
        return self.repository.create(db, dados)
    
    def list_por_venda(self, db: Session, venda_id: int):
        self._validar_venda_existe(db, venda_id)
        return self.repository.buscar_por_venda(db, venda_id)
    
    def get(self, db: Session, item_id: int):
        item = self.repository.get(db, item_id)
        if not item:
            raise ItemVendaNotFoundError()
        return item
    
    def update(self, db: Session, item_id: int, dados_atualizacao: ItemVendaUpdate):
        item = self.get(db, item_id)
        
        if dados_atualizacao.quantidade is not None:
            item.quantidade = dados_atualizacao.quantidade
        if dados_atualizacao.preco_unitario is not None:
            item.preco_unitario = dados_atualizacao.preco_unitario
        
        # Recalcular subtotal
        item.subtotal = self._calcular_subtotal(item.quantidade, item.preco_unitario)
        
        return self.repository.update(db, item_id, item.__dict__)
    
    def delete(self, db: Session, item_id: int):
        item = self.get(db, item_id)
        return self.repository.delete(db, item_id)