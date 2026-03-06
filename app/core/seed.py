from sqlalchemy.orm import Session
from app.models.categoria import Categoria

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