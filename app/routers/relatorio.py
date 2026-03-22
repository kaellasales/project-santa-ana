from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.services.relatorio import RelatorioService
from app.repositories.relatorio import RelatorioRepository

router = APIRouter()

repository = RelatorioRepository()
service = RelatorioService(repository)


@router.get("/vendas")
def relatorio_vendas(
    data_inicio: datetime,
    data_fim: datetime,
    db: Session = Depends(get_db)
):
    return service.relatorio_vendas(db, data_inicio, data_fim)

@router.get("/estoque")
def relatorio_estoque(db: Session = Depends(get_db)):
    return service.relatorio_estoque(db)