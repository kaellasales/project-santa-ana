from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.repositories.produto import ProdutoRepository
from app.services.produto import ProdutoService
from app.core.models import Produto

router = APIRouter()

def get_produto_service(db: Session = Depends(get_db)) -> ProdutoService:
    repo = ProdutoRepository(db, Produto) 
    return ProdutoService(repo)

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(nome: str | None = None, service: ProdutoService = Depends(get_produto_service)):
    if nome:
        return service.buscar_por_nome(nome)
    return service.list()

@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, service: ProdutoService = Depends(get_produto_service)):
    return service.create(produto)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, service: ProdutoService = Depends(get_produto_service)):
    return service.get(produto_id)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, service: ProdutoService = Depends(get_produto_service)):
    service.delete(produto_id)
    return None 
