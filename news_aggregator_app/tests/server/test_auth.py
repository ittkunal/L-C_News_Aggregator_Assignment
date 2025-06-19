def test_signup_and_login(client):
    resp = client.post("/auth/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert resp.status_code == 200

    resp = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert resp.status_code == 200
    assert "user_id" in resp.json()