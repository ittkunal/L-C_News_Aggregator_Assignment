import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    user_data = {
        "username": "reportuser",
        "email": "reportuser@example.com",
        "password": "ReportPass123"
    }
    client.post("/auth/signup", json=user_data)
    resp = client.post("/auth/login", json={
        "username": "reportuser",
        "password": "ReportPass123"
    })
    user_id = resp.json()["user_id"]
    return user_id

@pytest.fixture
def test_article_id():
    resp = client.get("/news/headlines")
    articles = resp.json()
    if articles:
        return articles[0]["id"]
    pytest.skip("No articles available to report.")

def test_report_article(test_user, test_article_id):
    resp = client.post("/user/report-article", json={
        "article_id": test_article_id,
        "user_id": test_user,
        "reason": "Inappropriate content"
    })
    assert resp.status_code == 200
    assert "reported" in resp.json().get("message", "").lower()

def test_admin_view_reported_articles():
    resp = client.get("/admin/reported-articles")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)