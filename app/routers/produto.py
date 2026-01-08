from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.repositories.produto import ProdutoRepository
from app.services.produto import ProdutoService
from app.models.produto import Produto
from app.core.exceptions import ProdutoNotFoundError

router = APIRouter()
repo = ProdutoRepository()
service = ProdutoService(repo)

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(nome: str | None = None, db: Session = Depends(get_db)):
    if nome:
        return service.buscar_por_nome(db, nome)
    return service.list(db)

@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return service.create(db, produto)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int,db: Session = Depends(get_db)):
    return service.get(db, produto_id)

@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, update_produto:ProdutoUpdate, db: Session = Depends(get_db)):
    update_data = update_produto.model_dump(exclude_unset=True)
    return service.update(db, produto_id, update_data)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    service.delete(db, produto_id)
    return None 

