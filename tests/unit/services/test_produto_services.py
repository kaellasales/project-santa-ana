import pytest
from unittest.mock import MagicMock
from app.services.produto import ProdutoService
from app.schemas.produto import ProdutoCreate
from app.core.exceptions import ProdutoNotFoundError

@pytest.fixture
def service_setup():
    mock_repository = MagicMock()
    service = ProdutoService(repository=mock_repository)
    mock_db = MagicMock()
    
    return service, mock_repository, mock_db

def test_create_produto_chama_repository_corretamente(service_setup):
    # Arrange 
    service, mock_repo, mock_db = service_setup
    
    # Dados de entrada (Schema Pydantic)
    produto_input = ProdutoCreate(nome="Coca Cola", preco_venda=10.0, estoque=100, categoria_id=1)
    
    # Ensinamos o Mock: "Quando chamarem o create, devolva esse dicionário"
    mock_repo.create.return_value = {"id": 1, "nome": "Coca Cola", "estoque":100, "preco_venda":10.0}
    
    # Act (Agir)
    resultado = service.create(mock_db, produto_input)
    
    # Assert (Verificar)
    # 1. O resultado é o que esperamos?
    assert resultado["id"] == 1
    assert resultado["nome"] == "Coca Cola"
    
    # 2. O service chamou o método certo no repository?
    # Note que aqui verificamos se ele converteu o Pydantic para dict (.model_dump())
    mock_repo.create.assert_called_once_with(mock_db, produto_input.model_dump())

def test_get_produto_levanta_erro_se_nao_existir(service_setup):
    # Arrange
    service, mock_repo, mock_db = service_setup
    
    # Ensinamos o Mock: "Quando buscarem o ID 999, retorne None (não achou)"
    mock_repo.get.return_value = None
    
    # Act & Assert (Agir e Verificar Exceção)
    # O pytest.raises funciona como um "try/except" invertido. 
    # O teste SÓ PASSAR se o erro acontecer.
    with pytest.raises(ProdutoNotFoundError):
        service.get(mock_db, produto_id=999)
    
    # Verifica se o repository foi chamado com o ID certo
    mock_repo.get.assert_called_once_with(mock_db, 999)

def test_get_produto_pelo_nome(service_setup):
    service, mock_repo, mock_db = service_setup

    dado_esperado = {"id": 1, "nome": "Coca Cola", "estoque": 100, "preco_venda": 10.0}
    
    mock_repo.buscar_por_nome.return_value = dado_esperado

    resultado = service.buscar_por_nome(mock_db, "Coca Cola")

    assert resultado == dado_esperado

    mock_repo.buscar_por_nome.assert_called_once_with(mock_db, "Coca Cola")

