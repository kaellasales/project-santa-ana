from sqlalchemy.orm import Session
from app.schemas.sincronizacao import SyncPayload, SyncResponse
from app.models.turno import Turno, TurnoStatus
from app.models.venda import Venda, VendaStatus
from app.models.itemVenda import ItemVenda
from app.models.pagamento import FormaPagamento
from app.models.movimentacao import TipoMovimentacao, MotivoMovimentacao
from app.repositories.turno import TurnoRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.movimentacao import MovimentacaoEstoqueRepository
from app.services.turno import TurnoService
from app.repositories.venda import VendaRepository
from datetime import datetime, timezone
from fastapi import HTTPException


class SincronizacaoService:
    def __init__(
        self,
        turno_repository: TurnoRepository,
        produto_repository: ProdutoRepository,
        movimentacao_repository: MovimentacaoEstoqueRepository,
        venda_repository: VendaRepository,
    ):
        self.turno_repository = turno_repository
        self.produto_repository = produto_repository
        self.movimentacao_repository = movimentacao_repository
        self.turno_service = TurnoService(turno_repository, venda_repository)

    def sincronizar(self, db: Session, payload: SyncPayload, usuario_id: int) -> SyncResponse:
        conflitos = []

        # ── 1. TURNO ──────────────────────────────────────────────────────────

        turno = db.query(Turno).filter(
            Turno.id_offline == payload.turno.id_offline
        ).first()

        if not turno:
            # Verifica se já existe turno ativo para o usuário
            # Se sim, reutiliza — pode ser que o turno foi aberto online
            turno_ativo = self.turno_repository.get_turno_ativo(db, usuario_id)
            if turno_ativo:
                turno = turno_ativo
                turno.id_offline = payload.turno.id_offline
            else:
                turno = Turno(
                    id_offline=payload.turno.id_offline,
                    usuario_id=usuario_id,
                    valor_inicial=payload.turno.valor_inicial,
                    data_abertura=payload.turno.data_abertura,
                    status=TurnoStatus.ABERTO,
                    total_vendas=0.0,
                    quantidade_vendas=0,
                )
                db.add(turno)

            db.flush()  # gera turno.id sem commitar

        # ── 2. VENDAS ─────────────────────────────────────────────────────────

        for venda_data in payload.vendas:

            venda = db.query(Venda).filter(
                Venda.id_offline == venda_data.id_offline
            ).first()

            if not venda:
                venda = Venda(
                    id_offline=venda_data.id_offline,
                    turno_id=turno.id,        # ID real resolvido pelo flush acima
                    usuario_id=usuario_id,
                    data_venda=venda_data.data_venda,
                    desconto=venda_data.desconto,
                    acrescimo=venda_data.acrescimo,
                    total=0.0,
                    status=VendaStatus.ABERTA,
                )
                db.add(venda)
                db.flush()  # gera venda.id

            # ── 3. ITENS ──────────────────────────────────────────────────────

            for item_data in venda_data.itens:

                item = db.query(ItemVenda).filter(
                    ItemVenda.id_offline == item_data.id_offline
                ).first()

                if item:
                    continue  # já sincronizado, pula

                produto = self.produto_repository.get(db, item_data.produto_id)

                if not produto:
                    conflitos.append({
                        "tipo": "PRODUTO_NAO_ENCONTRADO",
                        "produto_id": item_data.produto_id,
                        "venda_id_offline": str(venda_data.id_offline),
                    })
                    continue

                if produto.estoque < item_data.quantidade:
                    conflitos.append({
                        "tipo": "ESTOQUE_INSUFICIENTE",
                        "produto_id": item_data.produto_id,
                        "nome_produto": produto.nome,
                        "estoque_atual": produto.estoque,
                        "solicitado": item_data.quantidade,
                        "venda_id_offline": str(venda_data.id_offline),
                    })
                    continue

                subtotal = produto.preco_venda * item_data.quantidade

                db.add(ItemVenda(
                    id_offline=item_data.id_offline,
                    venda_id=venda.id,
                    produto_id=item_data.produto_id,
                    quantidade=item_data.quantidade,
                    preco_unitario=produto.preco_venda,
                    subtotal=subtotal,
                ))

                # Delta — nunca valor absoluto
                produto.estoque -= item_data.quantidade
                db.add(produto)

                # Movimentação — mesma lógica do VendaService.finalizar
                self.movimentacao_repository.create(db, {
                    "produto_id": item_data.produto_id,
                    "venda_id": venda.id,
                    "tipo": TipoMovimentacao.SAIDA,
                    "motivo": MotivoMovimentacao.VENDA,
                    "quantidade": item_data.quantidade,
                })

            db.flush()

            # ── 4. PAGAMENTO ──────────────────────────────────────────────────

            if venda_data.pagamento:
                pag_existe = db.query(FormaPagamento).filter(
                    FormaPagamento.id_offline == venda_data.pagamento.id_offline
                ).first()

                if not pag_existe:
                    total_venda = sum(
                        i.subtotal for i in db.query(ItemVenda)
                        .filter(ItemVenda.venda_id == venda.id).all()
                    )
                    total_venda += venda.acrescimo or 0
                    total_venda -= venda.desconto or 0

                    troco = max(
                        venda_data.pagamento.valor_recebido - total_venda, 0
                    )

                    db.add(FormaPagamento(
                        id_offline=venda_data.pagamento.id_offline,
                        venda_id=venda.id,
                        tipo=venda_data.pagamento.tipo,
                        valor_recebido=venda_data.pagamento.valor_recebido,
                        troco=troco,
                    ))
                    db.flush()

            # ── 5. FINALIZA VENDA ─────────────────────────────────────────────

            # Só finaliza se não teve conflitos nessa venda e tem itens
            itens_da_venda = db.query(ItemVenda).filter(
                ItemVenda.venda_id == venda.id
            ).all()

            venda_tem_conflito = any(
                c["venda_id_offline"] == str(venda_data.id_offline)
                for c in conflitos
            )

            if not venda_tem_conflito and itens_da_venda and venda_data.pagamento:
                venda.total = sum(i.subtotal for i in itens_da_venda)
                venda.total += venda.acrescimo or 0
                venda.total -= venda.desconto or 0
                venda.status = VendaStatus.CONCLUIDA
                venda.data_venda = venda_data.data_venda
                db.flush()

        # ── 6. FECHA TURNO ────────────────────────────────────────────────────

        # Atualiza totais do turno com as vendas que acabaram de entrar
        # Reutiliza lógica existente do TurnoService
        self.turno_service.atualizar_totais(db, turno.id)
        db.flush()

        if payload.turno.data_fechamento and turno.status == TurnoStatus.ABERTO:
            db.refresh(turno)  # pega total_vendas atualizado
            valor_esperado = turno.valor_inicial + turno.total_vendas
            diferenca = round(
                valor_esperado - (payload.turno.valor_informado or 0), 2
            )
            turno.status = TurnoStatus.FECHADO
            turno.data_fechamento = payload.turno.data_fechamento
            turno.valor_informado = payload.turno.valor_informado
            turno.valor_esperado = valor_esperado
            turno.diferenca = diferenca
            turno.observacoes = payload.turno.observacoes
            db.flush()

        db.commit()
        db.refresh(turno)

        return SyncResponse(
            status="ok" if not conflitos else "parcial",
            turno_id=turno.id,
            vendas_sincronizadas=len(payload.vendas) - len(set(
                c["venda_id_offline"] for c in conflitos
            )),
            conflitos=conflitos,
        )