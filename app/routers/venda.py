from fastapi import APIRouter, Depends, status, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_usuario_logado
from app.schemas.venda import VendaCreate, VendaResponse, VendaUpdate, VendaDetalhada
from app.repositories.venda import VendaRepository
from app.repositories.turno import TurnoRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.services.venda import VendaService

router = APIRouter()
repo_venda = VendaRepository()
repo_produto = ProdutoRepository()
repo_movimentacao = MovimentacaoEstoqueRepository()
repo_turno = TurnoRepository()
service = VendaService(repo_venda, repo_produto, repo_movimentacao, repo_turno)


@router.post("/", response_model=VendaDetalhada, status_code=status.HTTP_201_CREATED)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db), current_user=Depends(get_usuario_logado)):
    return service.create(db, venda, current_user.id)

@router.get("/", response_model=list[VendaResponse])
def listar_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list(db, skip=skip, limit=limit)

@router.get("/ultimas", response_model=list[VendaResponse])
def listar_ultimas_vendas(limite: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return service.list_ultimas_vendas(db, limite)

@router.get("/periodo", response_model=list[VendaResponse])
def listar_vendas_por_periodo(
    data_inicio: datetime = Query(...),
    data_fim: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return service.list_por_data(db, data_inicio, data_fim)

@router.get("/usuario/{usuario_id}", response_model=list[VendaResponse])
def listar_vendas_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.list_por_usuario(db, usuario_id)

@router.get("/usuario/{usuario_id}/periodo", response_model=list[VendaResponse])
def listar_vendas_usuario_por_periodo(
    usuario_id: int = Path(gt=0),
    data_inicio: datetime = Query(...),
    data_fim: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return service.list_por_usuario_e_data(db, usuario_id, data_inicio, data_fim)

@router.get("/usuario/{usuario_id}/total")
def obter_total_vendas_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
    total = service.total_vendas_usuario(db, usuario_id)
    return {"usuario_id": usuario_id, "total": total}

@router.get("/{venda_id}", response_model=VendaDetalhada)
def obter_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.get(db, venda_id)

@router.put("/{venda_id}", response_model=VendaResponse)
def atualizar_venda(
    venda_id: int = Path(gt=0),
    venda_atualizada: VendaUpdate = None,
    db: Session = Depends(get_db)
):
    return service.update(db, venda_id, venda_atualizada)

@router.put("/{venda_id}/recalcular-total", response_model=VendaResponse)
def recalcular_total_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.atualizar_total(db, venda_id)

@router.patch("/{venda_id}/finalizar", response_model=VendaResponse)
def finalizar_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.finalizar(db, venda_id)

@router.patch("/{venda_id}/cancelar", response_model=VendaResponse)
def cancelar_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.cancelar(db, venda_id)