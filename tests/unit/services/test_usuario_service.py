import pytest
from unittest.mock import MagicMock, patch
from app.services.usuario import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.exceptions import UsuarioNotFoundError

@pytest.fixture
def service_setup():
    mock_repository = MagicMock()
    service = UsuarioService(repository=mock_repository)
    mock_db = MagicMock()
    return service, mock_repository, mock_db

def test_create_usuario_sucesso(service_setup):
    service, mock_repo, mock_db = service_setup
    
    usuario_input = UsuarioCreate(username="admin", senha="123", email="admin@test.com", role="ADMIN")
    mock_repo.get_by_username.return_value = None
    mock_repo.create.return_value = {"id": 1, "username": "admin"}
    
    with patch.object(service, '_hash_senha', return_value="hashed_123"):
        resultado = service.create(mock_db, usuario_input)
    
    assert resultado["id"] == 1
    assert resultado["username"] == "admin"
    mock_repo.get_by_username.assert_called_once_with(mock_db, "admin")
    
    # Verifica que salvou com o hash
    dados_esperados = usuario_input.model_dump()
    dados_esperados["senha"] = "hashed_123"
    mock_repo.create.assert_called_once_with(mock_db, dados_esperados)

def test_create_usuario_username_existente(service_setup):
    service, mock_repo, mock_db = service_setup
    
    usuario_input = UsuarioCreate(username="admin", senha="123", email="admin@test.com", role="ADMIN")
    mock_repo.get_by_username.return_value = {"id": 1, "username": "admin"}
    
    with pytest.raises(ValueError, match="Username já cadastrado"):
        service.create(mock_db, usuario_input)

def test_get_usuario_sucesso(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.get.return_value = {"id": 1, "username": "admin"}
    
    resultado = service.get(mock_db, 1)
    
    assert resultado["id"] == 1
    mock_repo.get.assert_called_once_with(mock_db, 1)

def test_get_usuario_levanta_erro_se_nao_existir(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.get.return_value = None
    
    with pytest.raises(UsuarioNotFoundError):
        service.get(mock_db, 999)

def test_update_usuario(service_setup):
    service, mock_repo, mock_db = service_setup
    
    usuario_existente = {"id": 1, "username": "admin", "senha": "old_hash"}
    mock_repo.get.return_value = usuario_existente
    mock_repo.update.return_value = {"id": 1, "username": "admin_novo"}
    
    usuario_update = UsuarioUpdate(senha="new_pw")
    
    with patch.object(service, '_hash_senha', return_value="new_hash"):
        resultado = service.update(mock_db, 1, usuario_update)
        
    assert resultado["username"] == "admin_novo"
    mock_repo.update.assert_called_once_with(mock_db, usuario_existente, {"senha": "new_hash"})

def test_autenticar_sucesso(service_setup):
    service, mock_repo, mock_db = service_setup
    
    usuario_mock = MagicMock()
    usuario_mock.senha = "hashed_pw"
    mock_repo.get_by_username.return_value = usuario_mock
    
    with patch.object(service, '_verificar_senha', return_value=True):
        resultado = service.autenticar(mock_db, "admin", "senha_certa")
        
    assert resultado == usuario_mock

def test_autenticar_senha_errada(service_setup):
    service, mock_repo, mock_db = service_setup
    
    usuario_mock = MagicMock()
    usuario_mock.senha = "hashed_pw"
    mock_repo.get_by_username.return_value = usuario_mock
    
    with patch.object(service, '_verificar_senha', return_value=False):
        resultado = service.autenticar(mock_db, "admin", "senha_errada")
        
    assert resultado is None

def test_autenticar_usuario_nao_encontrado(service_setup):
    service, mock_repo, mock_db = service_setup
    
    mock_repo.get_by_username.return_value = None
    resultado = service.autenticar(mock_db, "missing", "pw")
    
    assert resultado is None

def test_deactivate_usuario(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.get.return_value = {"id": 1, "username": "admin"}
    
    service.deactivate(mock_db, 1)
    
    mock_repo.deactivate.assert_called_once_with(mock_db, 1)

def test_reativar_usuario_sucesso(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.reativar.return_value = {"id": 1, "is_active": True}
    
    resultado = service.reativar(mock_db, 1)
    
    assert resultado["is_active"] is True
    mock_repo.reativar.assert_called_once_with(mock_db, 1)

def test_reativar_usuario_erro(service_setup):
    service, mock_repo, mock_db = service_setup
    mock_repo.reativar.return_value = None
    
    with pytest.raises(UsuarioNotFoundError):
        service.reativar(mock_db, 999)
