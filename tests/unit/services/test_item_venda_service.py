import pytest
from unittest.mock import MagicMock
from app.services.itemVenda import ItemVendaService
from app.schemas.itemVenda import ItemVendaCreate, ItemVendaUpdate
from app.core.exceptions import ItemVendaNotFoundError, VendaNotFoundError, ProdutoNotFoundError

@pytest.fixture
def service_setup():
    mock_repo_item = MagicMock()
    mock_repo_produto = MagicMock()
    mock_repo_venda = MagicMock()
    
    service = ItemVendaService(
        repo_item_venda=mock_repo_item,
        repo_produto=mock_repo_produto,
        repo_venda=mock_repo_venda
    )
    mock_db = MagicMock()
    return service, mock_repo_item, mock_repo_produto, mock_repo_venda, mock_db

def test_create_item_venda_sucesso(service_setup):
    service, mock_repo_item, mock_repo_produto, mock_repo_venda, mock_db = service_setup
    
    venda_mock = MagicMock()
    venda_mock.itens = []
    mock_repo_venda.get.return_value = venda_mock
    
    produto_mock = MagicMock()
    produto_mock.estoque = 10
    produto_mock.preco_venda = 5.0
    mock_repo_produto.get.return_value = produto_mock
    
    item_input = ItemVendaCreate(produto_id=1, quantidade=2)
    mock_repo_item.create.return_value = {"id": 1, "subtotal": 10.0}
    
    resultado = service.create(mock_db, venda_id=1, item=item_input)
    
    assert produto_mock.estoque == 8
    assert resultado["id"] == 1
    mock_repo_item.create.assert_called_once()

def test_create_item_estoque_insuficiente(service_setup):
    service, mock_repo_item, mock_repo_produto, mock_repo_venda, mock_db = service_setup
    
    mock_repo_venda.get.return_value = MagicMock()
    
    produto_mock = MagicMock()
    produto_mock.estoque = 1
    mock_repo_produto.get.return_value = produto_mock
    
    item_input = ItemVendaCreate(produto_id=1, quantidade=5)
    
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        service.create(mock_db, venda_id=1, item=item_input)

def test_delete_item_sucesso(service_setup):
    service, mock_repo_item, mock_repo_produto, mock_repo_venda, mock_db = service_setup
    
    item_mock = MagicMock()
    item_mock.produto_id = 1
    item_mock.venda_id = 1
    item_mock.quantidade = 2
    item_mock.subtotal = 10.0
    mock_repo_item.get.return_value = item_mock
    
    produto_mock = MagicMock()
    produto_mock.estoque = 10
    mock_repo_produto.get.return_value = produto_mock
    
    venda_mock = MagicMock()
    venda_mock.itens = []
    mock_repo_venda.get.return_value = venda_mock
    
    service.delete(mock_db, item_id=1)
    
    assert produto_mock.estoque == 12
    mock_repo_item.delete.assert_called_once_with(mock_db, 1)
