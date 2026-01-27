from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.itemVenda import ItemVendaCreate, ItemVendaResponse, ItemVendaUpdate
from app.services.itemVenda import ItemVendaService
from app.repositories.itemVenda import ItemVendaRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.venda import VendaRepository

router = APIRouter()
repo_item_venda = ItemVendaRepository()
repo_produto= ProdutoRepository()
repo_venda = VendaRepository()

service = ItemVendaService(repo_item_venda, repo_produto, repo_venda)

@router.post("/{venda_id}/itens", response_model=ItemVendaResponse, status_code=status.HTTP_201_CREATED)
def criar_item_venda(
    venda_id: int = Path(gt=0),
    item: ItemVendaCreate = None,
    db: Session = Depends(get_db)
):
    return service.create(db, venda_id, item)

@router.get("/{venda_id}/itens", response_model=list[ItemVendaResponse])
def listar_itens_venda(
    venda_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return service.list_por_venda(db, venda_id)

@router.get("/{venda_id}/itens/{item_id}", response_model=ItemVendaResponse)
def obter_item_venda(
    venda_id: int = Path(gt=0),
    item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return service.get(db, item_id)

@router.put("/{venda_id}/itens/{item_id}", response_model=ItemVendaResponse)
def atualizar_item_venda(
    venda_id: int = Path(gt=0),
    item_id: int = Path(gt=0),
    item_atualizado: ItemVendaUpdate = None,
    db: Session = Depends(get_db)
):
    return service.update(db, item_id, item_atualizado)

@router.delete("/{venda_id}/itens/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_item_venda(
    venda_id: int = Path(gt=0),
    item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    service.delete(db, item_id)