import openpyxl
from sqlalchemy.orm import Session
from io import BytesIO
from datetime import datetime
from fastapi.responses import StreamingResponse
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.repositories.produto import ProdutoRepository
from app.schemas.movimentacao import MovimentacaoEstoqueCreate
from app.models.movimentacao import TipoMovimentacao, MotivoMovimentacao
from app.core.exceptions import ProdutoNotFoundError


class MovimentacaoEstoqueService:
    def __init__(self, repository: MovimentacaoEstoqueRepository, produto_repository: ProdutoRepository):
        self.repository = repository
        self.produto_repository = produto_repository

    def registrar(self, db: Session, dados: MovimentacaoEstoqueCreate):
        produto = self.produto_repository.get(db, dados.produto_id)
        if not produto:
            raise ProdutoNotFoundError()

        if dados.tipo == TipoMovimentacao.SAIDA and produto.estoque < dados.quantidade:
            raise ValueError(f"Estoque insuficiente. Estoque atual: {produto.estoque}")

        if dados.tipo == TipoMovimentacao.ENTRADA:
            produto.estoque += dados.quantidade
        else:
            produto.estoque -= dados.quantidade

        obj = self.repository.create(db, dados.model_dump())
        db.commit()
        db.refresh(obj)
        return obj

    def listar_por_produto(self, db: Session, produto_id: int):
        return self.repository.listar_por_produto(db, produto_id)

    def listar_por_venda(self, db: Session, venda_id: int):
        return self.repository.listar_por_venda(db, venda_id)

    def exportar_excel(self, db: Session, data_inicio: datetime, data_fim: datetime, tipo=None):
        movimentacoes = self.repository.listar_por_periodo(db, data_inicio, data_fim, tipo)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Movimentações"

        ws.append(["ID", "Produto", "Tipo", "Motivo", "Quantidade", "Venda ID", "Data"])

        for m in movimentacoes:
            ws.append([
                m.id,
                m.produto.nome,
                m.tipo.value,
                m.motivo.value,
                m.quantidade,
                m.venda_id or "-",
                m.data.strftime("%d/%m/%Y %H:%M")
            ])

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=movimentacoes.xlsx"}
        )