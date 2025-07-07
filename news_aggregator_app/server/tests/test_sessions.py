import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    user_data = {
        "username": "sessionuser",
        "email": "sessionuser@example.com",
        "password": "SessionPass123"
    }
    client.post("/auth/signup", json=user_data)
    resp = client.post("/auth/login", json={
        "username": "sessionuser",
        "password": "SessionPass123"
    })
    user_id = resp.json()["user_id"]
    return user_id

def test_login_session(test_user):
    resp = client.get("/user/saved-articles", params={"user_id": test_user})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_invalid_session():
    resp = client.get("/user/saved-articles", params={"user_id": 999999})
    assert resp.status_code in [200, 404, 401]

def test_logout(test_user):
    pass