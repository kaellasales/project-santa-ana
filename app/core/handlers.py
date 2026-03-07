from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.exceptions import NotFoundError, EstoqueInsuficienteError
from fastapi import Request

async def handler_geral_404(request, exc: NotFoundError):
    return JSONResponse(
        status_code=404, 
        content={"detail": str(exc) or "Recurso não encontrado"}
    )

async def estoque_insuficiente_handler(request: Request, exc: EstoqueInsuficienteError):
    return JSONResponse(
        status_code=409, 
        content={"message": exc.message, "tipo_erro": "estoque_insuficiente"},
    )
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

def setup_exception_handlers(app: FastAPI):
    """Registra todos os handlers na aplicação FastAPI"""
    app.add_exception_handler(NotFoundError, handler_geral_404)
    app.add_exception_handler(EstoqueInsuficienteError, estoque_insuficiente_handler)
    app.add_exception_handler(ValueError, value_error_handler)