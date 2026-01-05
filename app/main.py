from fastapi import FastAPI
from app.routers import categoria

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

app.include_router(categoria.router, prefix="/categorias", tags=["Categorias"])

@app.get("/")
def root():
    return {"message":"Api running"}

@app.get("/health")
def health():
    return {"status": "ok"}