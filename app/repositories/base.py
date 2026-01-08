from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session, DeclarativeBase

class Base(DeclarativeBase):
    pass

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> T | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[T]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: T, obj_in: dict) -> T | None:
        for field, value in obj_in.items():
            setattr(obj, field, value)

        db.commit()
        db.refresh(obj)
        return obj
        
    def delete(self, db: Session, id: int) -> T | None:
        obj = self.get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
