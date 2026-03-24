import pytest
from unittest.mock import MagicMock
from app.services.categoria import CategoriaService
from app.schemas.categoria import CategoriaCreate
from app.core.exceptions import CategoriaNotFoundError

@pytest.fixture
def service_setup():
    mock_repository = MagicMock()
    service = CategoriaService(repository=mock_repository)
    mock_db = MagicMock()
    return service, mock_repository, mock_db

def test_create_categoria_chama_repository_corretamente(service_setup):
    service, mock_repo, mock_db = service_setup
    
    categoria_input = CategoriaCreate(nome="Eletrônicos")
    mock_repo.create.return_value = {"id": 1, "nome": "Eletrônicos"}
    
    resultado = service.create(mock_db, categoria_input)
    
    assert resultado["id"] == 1
    assert resultado["nome"] == "Eletrônicos"
    mock_repo.create.assert_called_once_with(mock_db, categoria_input.model_dump())

def test_list_categorias(service_setup):
    service, mock_repo, mock_db = service_setup
    dado_esperado = [{"id": 1, "nome": "Categoria A"}, {"id": 2, "nome": "Categoria B"}]
    mock_repo.list.return_value = dado_esperado
    
    resultado = service.list(mock_db)
    
    assert resultado == dado_esperado
    mock_repo.list.assert_called_once_with(mock_db)

def test_get_categoria_sucesso(service_setup):
    service, mock_repo, mock_db = service_setup
    dado_esperado = {"id": 1, "nome": "Eletrônicos"}
    mock_repo.get.return_value = dado_esperado
    
    resultado = service.get(mock_db, categoria_id=1)
    
    assert resultado == dado_esperado
    mock_repo.get.assert_called_once_with(mock_db, 1)

def test_get_categoria_levanta_erro_se_nao_existir(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.get.return_value = None
    
    with pytest.raises(CategoriaNotFoundError):
        service.get(mock_db, categoria_id=999)
    
    mock_repo.get.assert_called_once_with(mock_db, 999)

def test_buscar_por_nome(service_setup):
    service, mock_repo, mock_db = service_setup
    dado_esperado = {"id": 1, "nome": "Eletrônicos"}
    mock_repo.buscar_por_nome.return_value = dado_esperado
    
    resultado = service.buscar_por_nome(mock_db, "Eletrônicos")
    
    assert resultado == dado_esperado
    mock_repo.buscar_por_nome.assert_called_once_with(mock_db, "Eletrônicos")

def test_delete_categoria_sucesso(service_setup):
    service, mock_repo, mock_db = service_setup
    dado_esperado = {"id": 1, "nome": "Para Deletar"}
    mock_repo.get.return_value = dado_esperado
    
    service.delete(mock_db, categoria_id=1)
    
    mock_repo.get.assert_called_once_with(mock_db, 1)
    mock_repo.deactivate.assert_called_once_with(mock_db, 1)
    mock_db.commit.assert_called_once()

def test_delete_categoria_levanta_erro_se_nao_existir(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.get.return_value = None
    
    with pytest.raises(CategoriaNotFoundError):
        service.delete(mock_db, categoria_id=999)
    
    mock_repo.get.assert_called_once_with(mock_db, 999)
    mock_repo.deactivate.assert_not_called()
