import pytest
from unittest.mock import MagicMock
from app.services.pagamento import FormaPagamentoService
from app.schemas.pagamento import FormaPagamentoCreate
from app.models.pagamento import TipoPagamento
from app.core.exceptions import VendaNotFoundError

@pytest.fixture
def service_setup():
    mock_repo_forma = MagicMock()
    mock_repo_venda = MagicMock()
    
    service = FormaPagamentoService(
        repo_forma_pagamento=mock_repo_forma,
        repo_venda=mock_repo_venda
    )
    mock_db = MagicMock()
    return service, mock_repo_forma, mock_repo_venda, mock_db

def test_calcular_troco_dinheiro(service_setup):
    service, _, _, _ = service_setup
    forma = FormaPagamentoCreate(tipo=TipoPagamento.DINHEIRO, valor_recebido=50.0)
    troco = service._calcular_troco(forma, 40.0)
    assert troco == 10.0

def test_calcular_troco_dinheiro_insuficiente(service_setup):
    service, _, _, _ = service_setup
    forma = FormaPagamentoCreate(tipo=TipoPagamento.DINHEIRO, valor_recebido=30.0)
    with pytest.raises(ValueError, match="Valor recebido insuficiente"):
        service._calcular_troco(forma, 40.0)

def test_calcular_troco_cartao_exato(service_setup):
    service, _, _, _ = service_setup
    forma = FormaPagamentoCreate(tipo=TipoPagamento.CARTAO_CREDITO, valor_recebido=40.0)
    troco = service._calcular_troco(forma, 40.0)
    assert troco == 0.0

def test_calcular_troco_cartao_diferente(service_setup):
    service, _, _, _ = service_setup
    forma = FormaPagamentoCreate(tipo=TipoPagamento.CARTAO_CREDITO, valor_recebido=50.0)
    with pytest.raises(ValueError, match="deve ser o valor exato"):
        service._calcular_troco(forma, 40.0)

def test_create_forma_pagamento_sucesso(service_setup):
    service, mock_repo_forma, mock_repo_venda, mock_db = service_setup
    
    venda_mock = MagicMock()
    venda_mock.forma_pagamento = None
    venda_mock.total = 100.0
    mock_repo_venda.get.return_value = venda_mock
    
    forma_input = FormaPagamentoCreate(tipo=TipoPagamento.DINHEIRO, valor_recebido=100.0)
    mock_repo_forma.create.return_value = {"id": 1, "venda_id": 1, "tipo": TipoPagamento.DINHEIRO}
    
    resultado = service.create(mock_db, 1, forma_input)
    assert resultado["id"] == 1
    mock_repo_forma.create.assert_called_once()

def test_create_forma_pagamento_venda_nao_encontrada(service_setup):
    service, _, mock_repo_venda, mock_db = service_setup
    mock_repo_venda.get.return_value = None
    
    forma_input = FormaPagamentoCreate(tipo=TipoPagamento.DINHEIRO, valor_recebido=100.0)
    with pytest.raises(VendaNotFoundError):
        service.create(mock_db, 1, forma_input)

def test_create_forma_pagamento_venda_com_pagamento(service_setup):
    service, _, mock_repo_venda, mock_db = service_setup
    
    venda_mock = MagicMock()
    venda_mock.forma_pagamento = MagicMock() # Já possui pagamento
    mock_repo_venda.get.return_value = venda_mock
    
    forma_input = FormaPagamentoCreate(tipo=TipoPagamento.DINHEIRO, valor_recebido=100.0)
    with pytest.raises(ValueError, match="Venda já possui forma de pagamento registrada"):
        service.create(mock_db, 1, forma_input)
