import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)


def test_signup_success():

    user_data = {
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "TestPass123",
    }
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 200
    assert "Signup successful" in response.json().get("message", "")


def test_signup_invalid_email():
    user_data = {
        "username": "testuser2",
        "email": "notanemail",
        "password": "TestPass123",
    }
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 422


def test_signup_duplicate_email():
    user_data = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "password": "TestPass123",
    }

    response1 = client.post("/auth/signup", json=user_data)

    response2 = client.post("/auth/signup", json=user_data)
    assert response2.status_code == 400 or response2.status_code == 409


def test_login_success():
    user_data = {
        "username": "testuser4",
        "email": "testuser4@example.com",
        "password": "TestPass123",
    }

    client.post("/auth/signup", json=user_data)
    response = client.post(
        "/auth/login", json={"username": "testuser4", "password": "TestPass123"}
    )
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_login_wrong_password():
    user_data = {
        "username": "testuser5",
        "email": "testuser5@example.com",
        "password": "TestPass123",
    }
    client.post("/auth/signup", json=user_data)
    response = client.post(
        "/auth/login", json={"username": "testuser5", "password": "WrongPass"}
    )
    assert response.status_code == 401


def test_login_nonexistent_user():
    response = client.post(
        "/auth/login", json={"username": "idontexist", "password": "whatever"}
    )
    assert response.status_code == 401
