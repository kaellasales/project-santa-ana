from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario import UsuarioService
from app.repositories.usuario import UsuarioRepository

router = APIRouter()

repository = UsuarioRepository()
service = UsuarioService(repository)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return service.create(db, usuario)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    return service.list(db, skip=skip, limit=limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.get(db, usuario_id)


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int = Path(gt=0), usuario: UsuarioUpdate = None, db: Session = Depends(get_db)):
    return service.update(db, usuario_id, usuario)


@router.patch("/{usuario_id}/desativar", response_model=UsuarioResponse)
def desativar_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.deactivate(db, usuario_id)


@router.patch("/{usuario_id}/reativar", response_model=UsuarioResponse)
def reativar_usuario(usuario_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return service.reativar(db, usuario_id)