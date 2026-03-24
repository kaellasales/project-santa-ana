import pytest
from unittest.mock import MagicMock
from app.services.turno import TurnoService
from app.schemas.turno import TurnoAbrir, TurnoFechar
from app.models.turno import TurnoStatus

@pytest.fixture
def service_setup():
    mock_repo_turno = MagicMock()
    mock_repo_venda = MagicMock()
    service = TurnoService(repository=mock_repo_turno, venda_repository=mock_repo_venda)
    mock_db = MagicMock()
    return service, mock_repo_turno, mock_repo_venda, mock_db

def test_abrir_turno_sucesso(service_setup):
    service, mock_repo, _, mock_db = service_setup
    mock_repo.get_turno_ativo.return_value = None
    
    dados = TurnoAbrir(valor_inicial=100.0)
    mock_repo.create.return_value = {"id": 1, "status": TurnoStatus.ABERTO}
    
    resultado = service.abrir(mock_db, dados, usuario_id=1)
    
    assert resultado["id"] == 1
    mock_repo.create.assert_called_once()

def test_abrir_turno_existente(service_setup):
    service, mock_repo, _, mock_db = service_setup
    mock_repo.get_turno_ativo.return_value = {"id": 1}
    
    dados = TurnoAbrir(valor_inicial=100.0)
    with pytest.raises(ValueError, match="Usuário já possui um turno aberto"):
        service.abrir(mock_db, dados, usuario_id=1)

def test_fechar_turno_sucesso(service_setup):
    service, mock_repo, _, mock_db = service_setup
    
    turno_mock = MagicMock()
    turno_mock.valor_inicial = 100.0
    turno_mock.vendas = [] # Sem vendas para simplificar
    
    mock_repo.get_turno_ativo.return_value = turno_mock
    
    dados = TurnoFechar(valor_informado=100.0, observacoes="")
    
    resultado = service.fechar(mock_db, dados, usuario_id=1)
    mock_repo.update.assert_called_once()
