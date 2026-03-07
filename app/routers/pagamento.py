from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.pagamento import FormaPagamentoCreate, FormaPagamentoResponse
from app.services.pagamento import FormaPagamentoService
from app.repositories.pagamento import FormaPagamentoRepository
from app.repositories.venda import VendaRepository

router = APIRouter()

repo_forma_pagamento = FormaPagamentoRepository()
repo_venda = VendaRepository()

service = FormaPagamentoService(repo_forma_pagamento, repo_venda)

@router.post("/{venda_id}/pagamento", response_model=FormaPagamentoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pagamento(
    venda_id: int = Path(gt=0),
    forma: FormaPagamentoCreate = None,
    db: Session = Depends(get_db)
):
    return service.create(db, venda_id, forma)
    
@router.put("/{venda_id}/pagamento", response_model=FormaPagamentoResponse)
def atualizar_pagamento(
    venda_id: int = Path(gt=0),
    forma: FormaPagamentoCreate = None,
    db: Session = Depends(get_db)
):
    return service.update(db, venda_id, forma)

@router.get("/{venda_id}/pagamento", response_model=FormaPagamentoResponse)
def obter_pagamento(
    venda_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return service.get_por_venda(db, venda_id)