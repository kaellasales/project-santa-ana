from sqlalchemy.orm import Session
from app.repositories.produto import ProdutoRepository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.core.exceptions import ProdutoNotFoundError

class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    def create(self, db:Session, produto: ProdutoCreate):
        return self.repository.create(db, produto.model_dump())

    def list(self, db:Session):
        return self.repository.list(db)

    def _get_or_raise(self, db:Session, produto_id: int):
        produto = self.repository.get(db, produto_id)
        if not produto:
            raise ProdutoNotFoundError()
        return produto

    def get(self, db: Session, produto_id: int):
        return self._get_or_raise(db, produto_id)
    
    def update(self, db:Session, produto_id: int, update_produto: ProdutoUpdate):
        produto = self._get_or_raise(db, produto_id)
        update_data = update_produto.model_dump(exclude_unset=True)
        return self.repository.update(db, produto, update_produto)

    def delete(self, db:Session, produto_id: int):
        produto = self._get_or_raise(db, produto_id)
        return self.repository.delete(db, produto_id)
    
    def buscar_por_nome(self, db:Session, nome: str):
        return self.repository.buscar_por_nome(db, nome)

    def dar_baixa_estoque(self, db: Session, produto_id: int, quantidade: int):
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        try:
            sucesso = self.repository.alterar_estoque(db, produto_id, -quantidade)
            
            if not sucesso:
                raise ProdutoNotFoundError()
                
            db.commit() 
            
            return self.repository.get(db, produto_id)

        except IntegrityError as e:
            db.rollback()
            if "check_estoque_non_negative" in str(e.orig):
                raise EstoqueInsuficienteError("Não há estoque suficiente para esta venda.")
            raise e 
