import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_get_headlines_today():
    response = client.get("/news/headlines")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_headlines_with_date_range():
    params = {"start": "2025-06-19", "end": "2025-06-19"}
    response = client.get("/news/headlines", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_headlines_with_category():
    params = {"category": "business"}
    response = client.get("/news/headlines", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_categories():
    response = client.get("/news/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert any("name" in cat for cat in categories)

def test_search_articles():
    response = client.get("/news/search", params={"q": "Tesla"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)