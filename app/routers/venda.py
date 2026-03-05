from fastapi import APIRouter, Depends, status, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.schemas.venda import VendaCreate, VendaResponse, VendaUpdate, VendaDetalhada
from app.repositories.venda import VendaRepository
from app.repositories.produto import ProdutoRepository
from app.services.venda import VendaService

router = APIRouter()
repo_venda = VendaRepository()
repo_produto = ProdutoRepository()
service = VendaService(repo_venda, repo_produto)


# Criar nova venda
@router.post("/", response_model=VendaDetalhada, status_code=status.HTTP_201_CREATED)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    return service.create(db, venda)

# Listar todas as vendas
@router.get("/", response_model=list[VendaResponse])
def listar_vendas(db: Session = Depends(get_db)):
    return service.list(db)

# Listar últimas vendas (com limite)
@router.get("/ultimas", response_model=list[VendaResponse])
def listar_ultimas_vendas(limite: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return service.list_ultimas_vendas(db, limite)

# Listar vendas por período
@router.get("/periodo", response_model=list[VendaResponse])
def listar_vendas_por_periodo(
    data_inicio: datetime = Query(...),
    data_fim: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return service.list_por_data(db, data_inicio, data_fim)

# Obter venda por ID
@router.get("/{venda_id}", response_model=VendaDetalhada)
def obter_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.get(db, venda_id)

# # Listar vendas de um usuário
# @router.get("/usuarios/{usuario_id}/vendas", response_model=list[VendaResponse])
# def listar_vendas_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
#     return service.list_por_usuario(db, usuario_id)

# # Listar vendas de um usuário por período
# @router.get("/usuarios/{usuario_id}/vendas/periodo", response_model=list[VendaResponse])
# def listar_vendas_usuario_por_periodo(
#     usuario_id: int = Path(gt=0),
#     data_inicio: datetime = Query(...),
#     data_fim: datetime = Query(...),
#     db: Session = Depends(get_db)
# ):
#     return service.list_por_usuario_e_data(db, usuario_id, data_inicio, data_fim)

# # Obter total de vendas de um usuário
# @router.get("/usuarios/{usuario_id}/total-vendas")
# def obter_total_vendas_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
#     total = service.total_vendas_usuario(db, usuario_id)
#     return {"usuario_id": usuario_id, "total": total}

# Atualizar venda
@router.put("/{venda_id}", response_model=VendaResponse)
def atualizar_venda(
    venda_id: int = Path(gt=0),
    venda_atualizada: VendaUpdate = None,
    db: Session = Depends(get_db)
):
    return service.update(db, venda_id, venda_atualizada)

# Recalcular total da venda
@router.put("/{venda_id}/recalcular-total", response_model=VendaResponse)
def recalcular_total_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.atualizar_total(db, venda_id)

@router.patch("/{venda_id}/finalizar", response_model=VendaResponse)
def finalizar_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.finalizar(db, venda_id)

@router.patch("/{venda_id}/cancelar", response_model=VendaResponse)
def cancelar_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.cancelar(db, venda_id)