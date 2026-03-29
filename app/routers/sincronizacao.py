from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_usuario_logado
from app.schemas.sincronizacao import SyncPayload, SyncResponse
from app.services.sincronizacao import SincronizacaoService
from app.repositories.turno import TurnoRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.repositories.venda import VendaRepository

router = APIRouter()

repo_turno = TurnoRepository()
repo_produto = ProdutoRepository()
repo_movimentacao = MovimentacaoEstoqueRepository()
repo_venda = VendaRepository()

service = SincronizacaoService(repo_turno, repo_produto, repo_movimentacao, repo_venda)


@router.post(
    "/",
    response_model=SyncResponse,
    status_code=status.HTTP_200_OK,
    summary="Sincronizar dados offline",
    description="Recebe o pacote completo de um turno offline (turno + vendas + itens + pagamentos) e persiste tudo em ordem dentro de uma transação.",
)
def sincronizar(
    payload: SyncPayload,
    db: Session = Depends(get_db),
    current_user=Depends(get_usuario_logado),
):
    return service.sincronizar(db, payload, current_user.id)