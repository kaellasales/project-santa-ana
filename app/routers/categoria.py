from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.repositories.categoria import CategoriaRepository
from app.services.categoria import CategoriaService

router = APIRouter()

def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
    repo = CategoriaRepository(db)
    return CategoriaService(repo)

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(nome: str | None = None, service: CategoriaService = Depends(get_categoria_service)):
    if nome:
        return service.buscar_por_nome(nome)
    return service.listar_todas()

@router.post("/", response_model=CategoriaResponse)
def criar_categoria(categoria: CategoriaCreate, service: CategoriaService = Depends(get_categoria_service)):
    return service.criar(categoria)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, service: CategoriaService = Depends(get_categoria_service)):
    return service.buscar_por_id(categoria_id)

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, categoria: CategoriaCreate, service: CategoriaService = Depends(get_categoria_service)):
    return service.atualizar(categoria_id, categoria.nome)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, service: CategoriaService = Depends(get_categoria_service)):
    service.deletar(categoria_id)