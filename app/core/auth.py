from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings

def criar_access_token(data: dict) -> str:
    payload = data.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expiracao, "type": "access"})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def criar_refresh_token(data: dict) -> str:
    payload = data.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload.update({"exp": expiracao, "type": "refresh"})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verificar_token(token: str, type: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != type:
            return None
        return payload
    except JWTError:
        return None