import pytest
from app.main import app
from app.core.dependencies import get_usuario_logado

def override_get_usuario_logado():
    return type("User", (), {"id": 1, "username": "vendedor"})()

@pytest.fixture
def auth_client(client):
    app.dependency_overrides[get_usuario_logado] = override_get_usuario_logado
    yield client
    app.dependency_overrides.pop(get_usuario_logado, None)

def test_fluxo_venda(auth_client):
    # 1. Abrir turno (necessário para vender)
    turno_resp = auth_client.post(
        "/turnos/abrir",
        json={"valor_inicial": 50.0}
    )
    assert turno_resp.status_code == 201
    
    # 2. Criar venda vazia
    venda_resp = auth_client.post(
        "/vendas/",
        json={"observacoes": "Cliente VIP"}
    )
    assert venda_resp.status_code == 201
    venda_id = venda_resp.json()["id"]
    
    # 3. Listar vendas
    listar_resp = auth_client.get("/vendas/")
    assert listar_resp.status_code == 200
    assert len(listar_resp.json()) > 0
    
    # 4. Obter venda
    get_resp = auth_client.get(f"/vendas/{venda_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == venda_id
    
    # 5. Fechar turno no final
    auth_client.post( "/turnos/fechar", json={"valor_informado": 50.0, "observacoes": ""} )
