from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from passlib.context import CryptContext
from app.models.usuario import Usuario, RoleUsuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
CATEGORIAS_PADRAO = [
    "Medicamentos & Saúde",
    "Vitaminas & Suplementos",
    "Beleza & Skincare",
    "Higiene Pessoal",
    "Bebê & Infantil",
    "Nutrição & Esporte",
    "Alimentação Saudável",
    "Casa & Limpeza",
    "Pet Care",
    "Aparelhos & Dispositivos",
    "Outros"
]

def seed_categorias(db: Session):
    for nome in CATEGORIAS_PADRAO:
        existe = db.query(Categoria).filter(Categoria.nome == nome).first()
        if not existe:
            db.add(Categoria(nome=nome, ativo=True))
    db.commit()


def seed_usuario_admin(db: Session):
    existe = db.query(Usuario).filter(Usuario.username == "admin").first()
    if not existe:
        db.add(Usuario(
            nome="Administrador",
            username="admin",
            senha=pwd_context.hash("admin123"),
            role=RoleUsuario.ADMIN,
            ativo=True
        ))
        db.commit()