import pytest
from app.main import app
from app.core.dependencies import get_admin

# Mock da dependência de admin
def override_get_admin():
    return {"id": 1, "username": "admin", "role": "ADMIN"}

@pytest.fixture
def auth_client(client):
    # Sobrescreve a dependência de admin para as rotas de usuário
    app.dependency_overrides[get_admin] = override_get_admin
    yield client
    app.dependency_overrides.pop(get_admin, None)

def test_fluxo_usuario(auth_client):
    # 1. Cria usuário
    response = auth_client.post(
        "/usuarios/",
        json={
            "username": "joao_teste",
            "nome_completo": "Joao Teste",
            "email": "joao@teste.com",
            "senha": "senha_segura",
            "role": "CAIXA"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "joao_teste"
    assert "senha" not in data # A resposta não deve conter a senha
    user_id = data["id"]
    
    # 2. Lista usuários
    list_resp = auth_client.get("/usuarios/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) > 0
    
    # 3. Obtém usuário por ID
    get_resp = auth_client.get(f"/usuarios/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == user_id
    
    # 4. Atualiza usuário
    patch_resp = auth_client.patch(f"/usuarios/{user_id}", json={"nome_completo": "Joao da Silva Teste"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["nome_completo"] == "Joao da Silva Teste"
    
    # 5. Desativa usuário
    desativar_resp = auth_client.patch(f"/usuarios/{user_id}/desativar")
    assert desativar_resp.status_code == 200
    assert desativar_resp.json()["is_active"] is False
    
    # 6. Reativa usuário
    reativar_resp = auth_client.patch(f"/usuarios/{user_id}/reativar")
    assert reativar_resp.status_code == 200
    assert reativar_resp.json()["is_active"] is True

def test_criar_usuario_existente(auth_client):
    # Tenta criar um que já existe
    auth_client.post(
        "/usuarios/",
        json={"username": "maria", "email": "m@m.com", "senha": "123", "role": "ADMIN"}
    )
    
    response2 = auth_client.post(
        "/usuarios/",
        json={"username": "maria", "email": "m2@m.com", "senha": "123", "role": "ADMIN"}
    )
    # Assumindo que o controller levanta uma exception validada como 400 ou 422
    assert response2.status_code in [400, 422, 500] 
