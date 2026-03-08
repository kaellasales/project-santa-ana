from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.auth import verificar_token
from app.core.database import get_db
from app.repositories.usuario import UsuarioRepository
from app.models.usuario import RoleUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
repository = UsuarioRepository()


def get_usuario_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    
    usuario = repository.get_by_username(db, payload.get("sub"))
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    
    return usuario


def get_admin(usuario=Depends(get_usuario_logado)):
    if usuario.role != RoleUsuario.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito ao administrador")
    return usuario