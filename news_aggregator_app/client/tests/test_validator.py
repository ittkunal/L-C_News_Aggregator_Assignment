import pytest
from client.services.auth_service import is_valid_email

def test_valid_email():
    assert is_valid_email("user@example.com")
    assert is_valid_email("user.name+tag@domain.co.in")
    assert is_valid_email("user_name@domain.com")

def test_invalid_email():
    assert not is_valid_email("userexample.com")
    assert not is_valid_email("user@.com")
    assert not is_valid_email("user@com")
    assert not is_valid_email("@example.com")
    assert not is_valid_email("user@")
    assert not is_valid_email("user@domain,com")