# app/core/handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import NotFoundError

async def handler_geral_404(request, exc: NaoEncontradoError):
    return JSONResponse(
        status_code=404, 
        content={"detail": str(exc) or "Recurso não encontrado"}
    )
def setup_exception_handlers(app: FastAPI):
    """Registra todos os handlers na aplicação FastAPI"""
    app.add_exception_handler(NotFoundError, handler_geral_404)

