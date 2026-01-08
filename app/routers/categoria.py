from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.repositories.categoria import CategoriaRepository
from app.services.categoria import CategoriaService
from app.models.categoria import Categoria

router = APIRouter()
repo = CategoriaRepository()
service = CategoriaService(repo)

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(nome: str | None = None, db:Session=Depends(get_db)):
    if nome:
        return service.buscar_por_nome(db, nome)
    return service.list(db)

@router.post("/", response_model=CategoriaResponse)
def criar_categoria(categoria: CategoriaCreate, db:Session=Depends(get_db)):
    return service.create(db, categoria)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, db:Session=Depends(get_db)):
    return service.get(db, categoria_id)

