from sqlalchemy.orm import Session
from app.core.models import Categoria as CategoriaModel
from app.schemas.categoria import CategoriaCreate
from .base import BaseRepository


class CategoriaRepository(BaseRepository):

    def buscar_por_nome(self, nome: str):
        return self.db.query(CategoriaModel).filter(CategoriaModel.nome.ilike(f"%{nome}%")).all()
