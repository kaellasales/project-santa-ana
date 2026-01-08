from sqlalchemy.orm import Session
from app.core.models import Categoria as CategoriaModel
from app.schemas.categoria import CategoriaCreate
from .base import BaseRepository


class CategoriaRepository(BaseRepository[CategoriaModel]):
    def __init__(self):
        super().__init__(CategoriaModel)

    def buscar_por_nome(self, db:Session, nome: str):
        return db.query(CategoriaModel).filter(CategoriaModel.nome.ilike(f"%{nome}%")).all()
