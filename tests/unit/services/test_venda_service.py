import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from app.services.venda import VendaService
from app.schemas.venda import VendaCreate, VendaUpdate
from app.core.exceptions import VendaNotFoundError, TurnoNotFoundError
from app.models.venda import VendaStatus

@pytest.fixture
def service_setup():
    mock_repo_venda = MagicMock()
    mock_repo_produto = MagicMock()
    mock_repo_movimentacao = MagicMock()
    mock_repo_turno = MagicMock()
    
    service = VendaService(
        repository_venda=mock_repo_venda,
        repository_produto=mock_repo_produto,
        repository_movimentacao=mock_repo_movimentacao,
        repository_turno=mock_repo_turno
    )
    # Mockando o TurnoService interno para evitar comportamentos inesperados nos testes da Venda
    service.turno_service = MagicMock()
    
    mock_db = MagicMock()
    return service, mock_repo_venda, mock_repo_turno, mock_db

def test_create_venda_sucesso(service_setup):
    service, mock_repo_venda, mock_repo_turno, mock_db = service_setup
    
    turno_mock = MagicMock()
    turno_mock.id = 1
    mock_repo_turno.get_turno_ativo.return_value = turno_mock
    
    venda_input = VendaCreate() # assumindo que não tem campos obrigatórios extras
    mock_repo_venda.create.return_value = {"id": 10, "total": 0.0, "usuario_id": 1, "turno_id": 1}
    
    resultado = service.create(mock_db, venda_input, usuario_id=1)
    
    assert resultado["id"] == 10
    mock_repo_turno.get_turno_ativo.assert_called_once_with(mock_db, 1)
    mock_repo_venda.create.assert_called_once()
    
def test_create_venda_turno_nao_encontrado(service_setup):
    service, mock_repo_venda, mock_repo_turno, mock_db = service_setup
    
    mock_repo_turno.get_turno_ativo.return_value = None
    venda_input = VendaCreate()
    
    with pytest.raises(TurnoNotFoundError):
        service.create(mock_db, venda_input, usuario_id=1)

def test_get_venda_sucesso(service_setup):
    service, mock_repo_venda, _, mock_db = service_setup
    mock_repo_venda.get.return_value = {"id": 1, "status": VendaStatus.ABERTA}
    
    resultado = service.get(mock_db, 1)
    assert resultado["id"] == 1

def test_finalizar_venda_sucesso(service_setup):
    service, mock_repo_venda, _, mock_db = service_setup
    
    venda_mock = MagicMock()
    venda_mock.id = 1
    venda_mock.status = VendaStatus.ABERTA
    venda_mock.forma_pagamento = True # tem forma de pagamento
    
    item_mock = MagicMock()
    item_mock.produto_id = 99
    item_mock.quantidade = 2
    item_mock.subtotal = 20.0
    venda_mock.itens = [item_mock]
    venda_mock.acrescimo = 0
    venda_mock.desconto = 0
    
    mock_repo_venda.get.return_value = venda_mock
    
    resultado = service.finalizar(mock_db, 1)
    
    assert resultado.status == VendaStatus.CONCLUIDA
    assert resultado.total == 20.0
    service.movimentacao_repository.create.assert_called_once()
    service.turno_service.atualizar_totais.assert_called_once()

def test_finalizar_venda_sem_itens(service_setup):
    service, mock_repo_venda, _, mock_db = service_setup
    venda_mock = MagicMock()
    venda_mock.status = VendaStatus.ABERTA
    venda_mock.itens = []
    
    mock_repo_venda.get.return_value = venda_mock
    
    with pytest.raises(ValueError, match="Venda não pode ser finalizada sem itens"):
        service.finalizar(mock_db, 1)

def test_cancelar_venda_sucesso(service_setup):
    service, mock_repo_venda, _, mock_db = service_setup
    
    venda_mock = MagicMock()
    venda_mock.id = 1
    venda_mock.status = VendaStatus.ABERTA
    venda_mock.itens = []
    
    mock_repo_venda.get.return_value = venda_mock
    
    resultado = service.cancelar(mock_db, 1)
    
    assert resultado.status == VendaStatus.CANCELADA
    service.turno_service.atualizar_totais.assert_called_once()
