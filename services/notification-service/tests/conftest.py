import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set testing mode before importing main
os.environ["TESTING"] = "true"

from main import app
from models import Base


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test_notifications.db"


@pytest.fixture(scope="function")
def test_db():
    """Create a test database"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestSessionLocal()
    
    # Override the get_db dependency to use test database
    from routes import get_db
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        yield db
    finally:
        db.close()
        app.dependency_overrides.clear()
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client():
    """Create a test client"""
    with TestClient(app) as client:
        yield client
