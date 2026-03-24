import pytest
from unittest.mock import MagicMock
from app.services.movimentacao import MovimentacaoEstoqueService
from app.schemas.movimentacao import MovimentacaoEstoqueCreate
from app.models.movimentacao import TipoMovimentacao, MotivoMovimentacao
from app.core.exceptions import ProdutoNotFoundError

@pytest.fixture
def service_setup():
    mock_repo = MagicMock()
    mock_repo_produto = MagicMock()
    service = MovimentacaoEstoqueService(repository=mock_repo, produto_repository=mock_repo_produto)
    mock_db = MagicMock()
    return service, mock_repo, mock_repo_produto, mock_db

def test_registrar_entrada_sucesso(service_setup):
    service, mock_repo, mock_repo_produto, mock_db = service_setup
    
    produto_mock = MagicMock()
    produto_mock.estoque = 10
    mock_repo_produto.get.return_value = produto_mock
    
    dados = MovimentacaoEstoqueCreate(
        produto_id=1,
        tipo=TipoMovimentacao.ENTRADA,
        motivo=MotivoMovimentacao.COMPRA,
        quantidade=5
    )
    
    mock_repo.create.return_value = {"id": 1, "quantidade": 5}
    resultado = service.registrar(mock_db, dados)
    
    assert produto_mock.estoque == 15
    assert resultado["id"] == 1
    mock_repo.create.assert_called_once()

def test_registrar_saida_sucesso(service_setup):
    service, mock_repo, mock_repo_produto, mock_db = service_setup
    
    produto_mock = MagicMock()
    produto_mock.estoque = 10
    mock_repo_produto.get.return_value = produto_mock
    
    dados = MovimentacaoEstoqueCreate(
        produto_id=1,
        tipo=TipoMovimentacao.SAIDA,
        motivo=MotivoMovimentacao.VENDA,
        quantidade=3
    )
    
    mock_repo.create.return_value = {"id": 2}
    service.registrar(mock_db, dados)
    
    assert produto_mock.estoque == 7

def test_registrar_saida_estoque_insuficiente(service_setup):
    service, mock_repo, mock_repo_produto, mock_db = service_setup
    
    produto_mock = MagicMock()
    produto_mock.estoque = 2
    mock_repo_produto.get.return_value = produto_mock
    
    dados = MovimentacaoEstoqueCreate(
        produto_id=1,
        tipo=TipoMovimentacao.SAIDA,
        motivo=MotivoMovimentacao.VENDA,
        quantidade=5
    )
    
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        service.registrar(mock_db, dados)

def test_registrar_produto_nao_encontrado(service_setup):
    service, mock_repo, mock_repo_produto, mock_db = service_setup
    mock_repo_produto.get.return_value = None
    
    dados = MovimentacaoEstoqueCreate(
        produto_id=99,
        tipo=TipoMovimentacao.ENTRADA,
        motivo=MotivoMovimentacao.COMPRA,
        quantidade=5
    )
    
    with pytest.raises(ProdutoNotFoundError):
        service.registrar(mock_db, dados)
