import pytest
from server.repositories.user_repo import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_user_by_username,
    update_user,
)

def test_create_and_get_user():
    import uuid
    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password_hash = "hashedpassword"
    user_id = create_user(username, email, password_hash)
    assert user_id is not None

    user = get_user_by_id(user_id)
    assert user is not None
    assert user["username"] == username

    user_by_email = get_user_by_email(email)
    assert user_by_email is not None
    assert user_by_email["id"] == user_id

    user_by_username = get_user_by_username(username)
    assert user_by_username is not None
    assert user_by_username["id"] == user_id

def test_update_user():
    import uuid
    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password_hash = "hashedpassword"
    user_id = create_user(username, email, password_hash)
    new_username = f"{username}_updated"
    new_email = f"{new_username}@example.com"
    update_user(user_id, new_username, new_email)
    user = get_user_by_id(user_id)
    assert user["username"] == new_username
    assert user["email"] == new_email