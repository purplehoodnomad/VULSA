import pytest

from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    return TestClient(app)

def test_health_live_endpoint(client):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200