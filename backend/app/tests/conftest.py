import pytest
from fastapi.testclient import TestClient
from app.services.fastapi_client import app  # FastAPI

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
