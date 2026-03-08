from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.schemas.movimentacao import MovimentacaoEstoqueCreate, MovimentacaoEstoqueResponse
from app.services.movimentacao import MovimentacaoEstoqueService
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.repositories.produto import ProdutoRepository
from app.models.movimentacao import TipoMovimentacao

router = APIRouter()

repository = MovimentacaoEstoqueRepository()
produto_repository = ProdutoRepository()
service = MovimentacaoEstoqueService(repository, produto_repository)


@router.post("/", response_model=MovimentacaoEstoqueResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(dados: MovimentacaoEstoqueCreate, db: Session = Depends(get_db)):
    return service.registrar(db, dados)

@router.get("/produto/{produto_id}", response_model=list[MovimentacaoEstoqueResponse])
def listar_por_produto(produto_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.listar_por_produto(db, produto_id)

@router.get("/venda/{venda_id}", response_model=list[MovimentacaoEstoqueResponse])
def listar_por_venda(venda_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.listar_por_venda(db, venda_id)

@router.get("/exportar")
def exportar(
    data_inicio: datetime,
    data_fim: datetime,
    tipo: TipoMovimentacao | None = None,
    db: Session = Depends(get_db)
):
    return service.exportar_excel(db, data_inicio, data_fim, tipo)