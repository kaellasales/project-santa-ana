from fastapi import FastAPI, Depends
from app.routers import (
    categoria, produto, venda, itemVenda, pagamento, 
    usuario, auth, movimentacao, turno, sincronizacao
)
from app.core.handlers import setup_exception_handlers
from app.core.seed import seed_categorias, seed_usuario_admin
from app.core.database import SessionLocal
from app.core.dependencies import get_usuario_logado
from app.routers import relatorio

app = FastAPI(
    title="API Farmácia Santa Ana",
    description="API para gerenciamento de farmácia.",
    version="1.0.0",
    contact={"name": "Kaella Sales", "email": "kaellasales09@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

protected = {"dependencies": [Depends(get_usuario_logado)]}

app.include_router(categoria.router, prefix="/categorias", tags=["Categorias"], **protected)
app.include_router(produto.router, prefix="/produtos", tags=["Produtos"], **protected)
app.include_router(venda.router, prefix="/vendas", tags=["vendas"], **protected)
app.include_router(itemVenda.router, prefix="/itens-venda", tags=["itens-venda"], **protected)
app.include_router(pagamento.router, prefix="/vendas", tags=["Pagamentos"], **protected)
app.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])  
app.include_router(auth.router, prefix="/auth", tags=["Auth"]) 
app.include_router(movimentacao.router, prefix="/movimentacoes", tags=["Movimentacoes"], **protected)
app.include_router(turno.router, prefix="/turnos", tags=["Turnos"], **protected)
app.include_router(relatorio.router, prefix="/relatorios", tags=["Relatorios"], **protected)
app.include_router(sincronizacao.router, prefix="/sincronizar", tags=["Sincronizacao"], **protected)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        seed_categorias(db)
        seed_usuario_admin(db)
    finally:
        db.close()

@app.get("/")
def root():
    return {"message":"Api running"}

@app.get("/health")
def health():
    return {"status": "ok"}

setup_exception_handlers(app)
