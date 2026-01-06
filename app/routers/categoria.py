from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.repositories.categoria import CategoriaRepository
from app.services.categoria import CategoriaService
from app.core.models import Categoria

router = APIRouter()

def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
    repo = CategoriaRepository(db, Categoria) 
    return CategoriaService(repo)

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(nome: str | None = None, service: CategoriaService = Depends(get_categoria_service)):
    if nome:
        return service.buscar_por_nome(nome)
    return service.list()

@router.post("/", response_model=CategoriaResponse)
def criar_categoria(categoria: CategoriaCreate, service: CategoriaService = Depends(get_categoria_service)):
    return service.create(categoria)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, service: CategoriaService = Depends(get_categoria_service)):
    return service.get(categoria_id)

