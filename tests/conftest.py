import pytest
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.core.models import Categoria  
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db():
    engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session
    
    session.close()
    engine.dispose()

@pytest.fixture
def client(test_db):
    from app.core.database import get_db
    
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)
    
    yield client
    
    app.dependency_overrides.clear()
