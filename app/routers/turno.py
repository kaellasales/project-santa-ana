from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_usuario_logado
from app.schemas.turno import TurnoAbrir, TurnoFechar, TurnoAtivoResponse, TurnoResumoResponse
from app.repositories.turno import TurnoRepository
from app.repositories.venda import VendaRepository
from app.services.turno import TurnoService

router = APIRouter()

repository = TurnoRepository()
venda_repository = VendaRepository()
service = TurnoService(repository, venda_repository)

@router.post("/abrir", response_model=TurnoAtivoResponse, status_code=status.HTTP_201_CREATED)
def abrir_turno(dados: TurnoAbrir, db: Session = Depends(get_db), current_user=Depends(get_usuario_logado)):
    return service.abrir(db, dados, current_user.id)


@router.get("/ativo", response_model=TurnoAtivoResponse | None)
def get_turno_ativo(db: Session = Depends(get_db), current_user=Depends(get_usuario_logado)):
    return service.get_turno_ativo(db, current_user.id)


@router.post("/fechar", response_model=TurnoResumoResponse)
def fechar_turno(dados: TurnoFechar, db: Session = Depends(get_db), current_user=Depends(get_usuario_logado)):
    return service.fechar(db, dados, current_user.id)


@router.get("/historico", response_model=list[TurnoResumoResponse])
def listar_historico(db: Session = Depends(get_db), current_user=Depends(get_usuario_logado)):
    return service.listar_por_usuario(db, current_user.id)