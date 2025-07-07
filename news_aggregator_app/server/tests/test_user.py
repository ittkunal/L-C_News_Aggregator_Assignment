import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    user_data = {
        "username": "saveuser",
        "email": "saveuser@example.com",
        "password": "SavePass123"
    }
    client.post("/auth/signup", json=user_data)
    resp = client.post("/auth/login", json={
        "username": "saveuser",
        "password": "SavePass123"
    })
    user_id = resp.json()["user_id"]
    return user_id

@pytest.fixture
def test_article_id():
    resp = client.get("/news/headlines")
    articles = resp.json()
    if articles:
        return articles[0]["id"]
    pytest.skip("No articles available to save.")

def test_save_article(test_user, test_article_id):
    resp = client.post("/user/saved-articles", params={"user_id": test_user, "article_id": test_article_id})
    assert resp.status_code == 200
    assert "save" in resp.json().get("message", "").lower()

def test_get_saved_articles(test_user, test_article_id):
    client.post("/user/saved-articles", params={"user_id": test_user, "article_id": test_article_id})
    resp = client.get("/user/saved-articles", params={"user_id": test_user})
    assert resp.status_code == 200
    articles = resp.json()
    assert any(a["id"] == test_article_id for a in articles)

def test_delete_saved_article(test_user, test_article_id):
    client.post("/user/saved-articles", params={"user_id": test_user, "article_id": test_article_id})
    resp = client.delete(f"/user/saved-articles/{test_article_id}", params={"user_id": test_user})
    assert resp.status_code == 200
    assert "delete" in resp.json().get("message", "").lower()