from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import criar_access_token, criar_refresh_token, verificar_token
from app.repositories.usuario import UsuarioRepository
from app.services.usuario import UsuarioService
from app.schemas.token import TokenResponse, RefreshTokenRequest

router = APIRouter()

repository = UsuarioRepository()
service = UsuarioService(repository)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = service.autenticar(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = criar_access_token({"sub": usuario.username, "role": usuario.role.value})
    refresh_token = criar_refresh_token({"sub": usuario.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = verificar_token(data.refresh_token, "refresh")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido ou expirado")
    
    usuario = repository.get_by_username(db, payload.get("sub"))
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    
    access_token = criar_access_token({"sub": usuario.username, "role": usuario.role.value})
    refresh_token = criar_refresh_token({"sub": usuario.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}