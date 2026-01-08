import pytest

def test_criar_categoria(client):
    """Testa criar uma categoria com sucesso"""
    response = client.post(
        "/categorias/",
        json={"nome": "Eletrônicos"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Eletrônicos"
    assert "id" in data
    print(f"Categoria criada com ID: {data['id']}")

def test_criar_categoria_nome_vazio(client):
    """Testa criar categoria com nome vazio (deve falhar)"""
    response = client.post(
        "/categorias/",
        json={"nome": ""}
    )
    
    assert response.status_code == 422

def test_listar_categorias_vazio(client):
    """Testa listar categorias quando não há nenhuma"""
    response = client.get("/categorias/")
    
    assert response.status_code == 200
    assert response.json() == []

def test_listar_categorias_com_dados(client):
    """Testa listar categorias depois de criar algumas"""
    # Arrange - cria dados de teste
    client.post("/categorias/", json={"nome": "Livros"})
    client.post("/categorias/", json={"nome": "Filmes"})
    client.post("/categorias/", json={"nome": "Música"})
    
    # Act - faz a requisição
    response = client.get("/categorias/")
    
    # Assert - verifica
    assert response.status_code == 200
    categorias = response.json()
    assert len(categorias) == 3
    nomes = [c["nome"] for c in categorias]
    assert "Livros" in nomes
    assert "Filmes" in nomes
    assert "Música" in nomes

def test_buscar_categoria_por_id(client):
    """Testa buscar uma categoria específica pelo ID"""
    # Arrange - cria a categoria
    create_response = client.post("/categorias/", json={"nome": "Eletrônicos"})
    categoria_id = create_response.json()["id"]
    
    # Act - busca ela
    response = client.get(f"/categorias/{categoria_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == categoria_id
    assert data["nome"] == "Eletrônicos"

def test_buscar_categoria_inexistente(client):
    """Testa buscar uma categoria que não existe"""
    response = client.get("/categorias/9999")
    
    assert response.status_code == 404
    assert "Recurso não encontrado" in response.json()["detail"]

def test_buscar_categoria_por_nome(client):
    """Testa filtrar categorias pelo nome"""
    # Arrange - cria várias categorias
    client.post("/categorias/", json={"nome": "Eletrônicos"})
    client.post("/categorias/", json={"nome": "Eletrodomésticos"})
    client.post("/categorias/", json={"nome": "Livros"})
    
    # Act - busca por nome parcial
    response = client.get("/categorias/?nome=Eletr")
    
    # Assert
    assert response.status_code == 200
    categorias = response.json()
    assert len(categorias) == 2
    nomes = [c["nome"] for c in categorias]
    assert "Eletrônicos" in nomes
    assert "Eletrodomésticos" in nomes
