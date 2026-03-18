from sqlalchemy.orm import Session
from app.models.turno import Turno as TurnoModel, TurnoStatus
from .base import BaseRepository


class TurnoRepository(BaseRepository[TurnoModel]):
    def __init__(self):
        super().__init__(TurnoModel)

    def get_turno_ativo(self, db: Session, usuario_id: int) -> TurnoModel | None:
        return (
            db.query(TurnoModel)
            .filter(
                TurnoModel.usuario_id == usuario_id,
                TurnoModel.status == TurnoStatus.ABERTO
            )
            .first()
        )

    def listar_por_usuario(self, db: Session, usuario_id: int) -> list[TurnoModel]:
        return (
            db.query(TurnoModel)
            .filter(TurnoModel.usuario_id == usuario_id)
            .order_by(TurnoModel.data_abertura.desc())
            .all()
        )