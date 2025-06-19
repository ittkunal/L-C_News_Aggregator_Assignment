def test_cli_login(monkeypatch):
    from client.services.auth_service import login
    inputs = iter(["testuser@example.com", "testpass123"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    login()  # Should print login result

def test_cli_signup(monkeypatch):
    from client.services.auth_service import signup
    inputs = iter(["testuser", "testuser@example.com", "testpass123"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    signup()  # Should print signup result