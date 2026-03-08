from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.produto import ProdutoRepository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.core.exceptions import ProdutoNotFoundError, EstoqueInsuficienteError
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.models.movimentacao import TipoMovimentacao, MotivoMovimentacao


class ProdutoService:
    def __init__(self, repository: ProdutoRepository, movimentacao_repository: MovimentacaoEstoqueRepository):
        self.repository = repository
        self.movimentacao_repository = movimentacao_repository

    def create(self, db: Session, produto: ProdutoCreate):
        obj = self.repository.create(db, produto.model_dump())
        
        if obj.estoque > 0:
            self.movimentacao_repository.create(db, {
                "produto_id": obj.id,
                "venda_id": None,
                "tipo": TipoMovimentacao.ENTRADA,
                "motivo": MotivoMovimentacao.CADASTRO_INICIAL,
                "quantidade": obj.estoque
            })

        db.commit()
        db.refresh(obj)
        return obj

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.list(db, skip=skip, limit=limit)

    def _get_or_raise(self, db:Session, produto_id: int):
        produto = self.repository.get(db, produto_id)
        if not produto:
            raise ProdutoNotFoundError()
        return produto

    def get(self, db: Session, produto_id: int):
        return self._get_or_raise(db, produto_id)
    
    def update(self, db: Session, produto_id: int, update_produto: ProdutoUpdate):
        produto = self._get_or_raise(db, produto_id)
        update_data = update_produto.model_dump(exclude_unset=True)
        obj = self.repository.update(db, produto, update_data)
        db.commit()
        return obj

    def delete(self, db: Session, produto_id: int):
        produto = self._get_or_raise(db, produto_id)
        self.repository.deactivate(db, produto_id)
        db.commit()
    
    def buscar_por_nome(self, db:Session, nome: str):
        return self.repository.buscar_por_nome(db, nome)

    def buscar_por_codigo_barra(self, db:Session, codigo_barra: str):
        return self.repository.buscar_por_codigo_barra(db, codigo_barra)    

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
