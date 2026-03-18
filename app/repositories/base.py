from typing import TypeVar, Generic, Type, List
from sqlalchemy.orm import Session, DeclarativeBase

class Base(DeclarativeBase):
    pass

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> T | None:
        query = db.query(self.model).filter(self.model.id == id)
        if hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo)
        return query.first()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        query = db.query(self.model)
        if hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: T, obj_in: dict) -> T | None:
        for field, value in obj_in.items():
            setattr(obj, field, value)
        db.flush()
        db.refresh(obj)
        return obj
        
    def delete(self, db: Session, id: int) -> T | None:
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.flush()
        return obj

    def deactivate(self, db: Session, id: int) -> T | None:
        obj = self.get(db, id)
        if obj:
            obj.ativo = False
            db.flush()
        return obj

    def get_inactive(self, db: Session, id: int) -> T | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def reativar(self, db: Session, id: int) -> T | None:
        obj = self.get_inactive(db, id)
        if obj:
            obj.ativo = True
            db.flush()
        return obj

    def list_inactive(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        query = db.query(self.model)
        if hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo.is_(False))
        return query.offset(skip).limit(limit).all()
