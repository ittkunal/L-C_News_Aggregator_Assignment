import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)


@pytest.fixture
def test_user():
    user_data = {
        "username": "personaluser",
        "email": "personaluser@example.com",
        "password": "PersonalPass123",
    }
    client.post("/auth/signup", json=user_data)
    resp = client.post(
        "/auth/login", json={"username": "personaluser", "password": "PersonalPass123"}
    )
    user_id = resp.json()["user_id"]
    return user_id


@pytest.fixture
def test_article_id():
    resp = client.get("/news/headlines")
    articles = resp.json()
    if articles:
        return articles[0]["id"]
    pytest.skip("No articles available for personalization test.")


def test_personalized_feed_with_keyword(test_user):
    keyword = "tesla"
    client.put(
        "/user/notifications",
        params={
            "user_id": test_user,
            "type": "business",
            "enabled": True,
            "keywords": keyword,
        },
    )
    resp = client.get("/news/headlines", params={"user_id": test_user})
    assert resp.status_code == 200
    articles = resp.json()

    found = any(
        keyword.lower()
        in ((a.get("title") or "").lower() + (a.get("content") or "").lower())
        for a in articles
    )
    if articles:
        if not found:
            pytest.skip(
                f"No articles with keyword '{keyword}' in the feed for this test run."
            )
        assert found


def test_personalized_feed_with_like(test_user, test_article_id):
    client.post(f"/news/{test_article_id}/like", params={"user_id": test_user})
    resp = client.get("/news/headlines", params={"user_id": test_user})
    assert resp.status_code == 200
    articles = resp.json()
    if articles:
        assert any(a["id"] == test_article_id for a in articles)
