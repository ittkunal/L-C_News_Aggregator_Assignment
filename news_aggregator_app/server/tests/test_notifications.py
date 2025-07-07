import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    user_data = {
        "username": "notifuser",
        "email": "notifuser@example.com",
        "password": "NotifPass123"
    }
    client.post("/auth/signup", json=user_data)
    resp = client.post("/auth/login", json={
        "username": "notifuser",
        "password": "NotifPass123"
    })
    user_id = resp.json()["user_id"]
    return user_id

def test_get_notifications_empty(test_user):
    resp = client.get("/user/notifications", params={"user_id": test_user})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_enable_notification_for_category(test_user):
    resp = client.put("/user/notifications", params={
        "user_id": test_user,
        "type": "business",
        "enabled": True,
        "keywords": "stock,market"
    })
    assert resp.status_code == 200
    assert "updated" in resp.json().get("message", "").lower()

def test_get_notifications_after_enabling(test_user):
    resp = client.get("/user/notifications", params={"user_id": test_user})
    assert resp.status_code == 200
    notifications = resp.json()
    assert any(n.get("type") == "business" and n.get("enabled") in [True, 1] for n in notifications)

def test_disable_notification_for_category(test_user):
    resp = client.put("/user/notifications", params={
        "user_id": test_user,
        "type": "business",
        "enabled": False
    })
    assert resp.status_code == 200
    assert "updated" in resp.json().get("message", "").lower()
    resp2 = client.get("/user/notifications", params={"user_id": test_user})
    notifications = resp2.json()
    assert any(n.get("type") == "business" and n.get("enabled") in [False, 0] for n in notifications)