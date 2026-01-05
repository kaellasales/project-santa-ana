# app/repositories/categoria.py
from sqlalchemy.orm import Session
from app.core.models import Categoria as CategoriaModel
from app.schemas.categoria import CategoriaCreate

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, categoria: CategoriaCreate) -> CategoriaModel:
        db_categoria = CategoriaModel(nome=categoria.nome)
        self.db.add(db_categoria)
        self.db.commit()
        self.db.refresh(db_categoria)
        return db_categoria

    def listar_todas(self):
        return self.db.query(CategoriaModel).all()

    def buscar_por_id(self, categoria_id: int):
        return self.db.query(CategoriaModel).filter(CategoriaModel.id == categoria_id).first()

    def buscar_por_nome(self, nome: str):
        return self.db.query(CategoriaModel).filter(CategoriaModel.nome.ilike(f"%{nome}%")).all()

    def atualizar(self, categoria_id: int, novo_nome: str):
        categoria = self.buscar_por_id(categoria_id)
        if not categoria:
            return None
        categoria.nome = novo_nome
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def deletar(self, categoria_id: int):
        categoria = self.buscar_por_id(categoria_id)
        if not categoria:
            return False
        self.db.delete(categoria)
        self.db.commit()
        return True
