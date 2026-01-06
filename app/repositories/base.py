from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session, DeclarativeBase

class Base(DeclarativeBase):
    pass

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get(self, id: int) -> T | None:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def list(self, skip: int = 0, limit: int = 100) -> list[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> T | None:
        obj = self.get(self.db, id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
