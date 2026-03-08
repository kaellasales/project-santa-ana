from app.repositories.base import BaseRepository
from app.models.usuario import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    def get_by_username(self, db, username: str) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.username == username, Usuario.ativo).first()