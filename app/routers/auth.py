from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import criar_token
from app.repositories.usuario import UsuarioRepository
from app.services.usuario import UsuarioService
from app.schemas.token import TokenResponse

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
    token = criar_token({"sub": usuario.username, "role": usuario.role.value})
    return {"access_token": token, "token_type": "bearer"}