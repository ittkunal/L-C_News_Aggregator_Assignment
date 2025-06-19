def test_session_creation(client):
    resp = client.post("/auth/signup", json={
        "username": "sessionuser",
        "email": "sessionuser@example.com",
        "password": "testpass123"
    })
    assert resp.status_code == 200 or resp.status_code == 400

    resp = client.post("/auth/login", json={
        "email": "sessionuser@example.com",
        "password": "testpass123"
    })
    assert resp.status_code == 200
    assert "user_id" in resp.json()