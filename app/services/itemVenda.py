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
        venda = self._validar_venda_existe(db, venda_id)
        produto = self._validar_produto_existe(db, item.produto_id)
        
        # Validar estoque
        if produto.estoque < item.quantidade:
            raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque}")
        
        preco_unitario = float(produto.preco_venda)
        subtotal = self._calcular_subtotal(item.quantidade, preco_unitario)
        
        dados = item.model_dump()
        dados["venda_id"] = venda_id
        dados["subtotal"] = subtotal
        dados["preco_unitario"] = preco_unitario

        produto.estoque -= item.quantidade
        db.add(produto)
        item_criado = self.repository.create(db, dados)

        db.refresh(venda)
        venda.total = sum(i.subtotal for i in venda.itens)
        db.add(venda)
        db.commit()

        return item_criado
        
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
        produto = self._validar_produto_existe(db, item.produto_id)
        venda = self._validar_venda_existe(db, item.venda_id)

        if dados_atualizacao.quantidade is not None:
            diferenca = dados_atualizacao.quantidade - item.quantidade
            if diferenca > 0 and produto.estoque < diferenca:
                raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque}")
            produto.estoque -= diferenca
            self.produto_repository.update(db, produto, {"estoque": produto.estoque})
            item.quantidade = dados_atualizacao.quantidade

        item.subtotal = self._calcular_subtotal(item.quantidade, item.preco_unitario)
        self.repository.update(db, item, {"quantidade": item.quantidade, "subtotal": item.subtotal})

        db.refresh(venda)
        venda.total = sum(i.subtotal for i in venda.itens)
        self.venda_repository.update(db, venda, {"total": venda.total})

        db.commit()
        db.refresh(item)
        return item

    def delete(self, db: Session, item_id: int):
        item = self.get(db, item_id)
        produto = self._validar_produto_existe(db, item.produto_id)
        venda = self._validar_venda_existe(db, item.venda_id)

        produto.estoque += item.quantidade
        db.add(produto)

        self.repository.delete(db, item_id)

        db.refresh(venda)
        venda.total = sum(i.subtotal for i in venda.itens)
        db.add(venda)
        db.commit()