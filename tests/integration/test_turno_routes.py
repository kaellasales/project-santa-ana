import pytest
from app.main import app
from app.core.dependencies import get_usuario_logado

def override_get_usuario_logado():
    return type("User", (), {"id": 2, "username": "operador_turno"})()

@pytest.fixture
def auth_client_turno(client):
    app.dependency_overrides[get_usuario_logado] = override_get_usuario_logado
    yield client
    app.dependency_overrides.pop(get_usuario_logado, None)

def test_fluxo_turno(auth_client_turno):
    # 1. Abrir turno
    resp_abrir = auth_client_turno.post(
        "/turnos/abrir",
        json={"valor_inicial": 100.50}
    )
    assert resp_abrir.status_code == 201
    assert resp_abrir.json()["status"] == "Aberto"
    
    # 2. Get turno ativo
    resp_ativo = auth_client_turno.get("/turnos/ativo")
    assert resp_ativo.status_code == 200
    assert resp_ativo.json()["valor_inicial"] == 100.50
    
    # 3. Fechar turno
    resp_fechar = auth_client_turno.post(
        "/turnos/fechar",
        json={"valor_informado": 100.50, "observacoes": "Tudo certo"}
    )
    assert resp_fechar.status_code == 200
    assert resp_fechar.json()["status"] == "Fechado"
    
    # 4. Listar histórico
    resp_historico = auth_client_turno.get("/turnos/historico")
    assert resp_historico.status_code == 200
    assert len(resp_historico.json()) > 0
