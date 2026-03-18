from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.repositories.produto import ProdutoRepository
from app.services.produto import ProdutoService
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.models.produto import Produto
from app.core.exceptions import ProdutoNotFoundError


router = APIRouter()
repo = ProdutoRepository()
repo_movimentacao = MovimentacaoEstoqueRepository()
service = ProdutoService(repo, repo_movimentacao)

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(nome: str | None = None, codigo_barra: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if nome:
        return service.buscar_por_nome(db, nome)
    if codigo_barra:
        produto = service.buscar_por_codigo_barra(db, codigo_barra)
        return [produto] if produto else []
    return service.list(db, skip=skip, limit=limit)

@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return service.create(db, produto)

@router.get("/inativos/", response_model=list[ProdutoResponse])
def listar_produtos_inativos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list_inactive(db, skip=skip, limit=limit)

@router.get("/codigo_barra/{codigo_barra}", response_model=ProdutoResponse)
def obter_produto_por_codigo_barra(codigo_barra: str, db: Session = Depends(get_db)):
    return service.buscar_por_codigo_barra(db, codigo_barra)
    
@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int,db: Session = Depends(get_db)):
    return service.get(db, produto_id)

@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, update_produto:ProdutoUpdate, db: Session = Depends(get_db)):
    return service.update(db, produto_id, update_produto)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    service.delete(db, produto_id)
    return None 



