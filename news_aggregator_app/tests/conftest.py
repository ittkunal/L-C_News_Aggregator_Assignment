import pytest

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from server.main import app
    return TestClient(app)