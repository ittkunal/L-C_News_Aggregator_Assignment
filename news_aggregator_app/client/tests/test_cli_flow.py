import pytest
from unittest.mock import patch

import client.main as client_main

@patch("client.menus.main_menu.login")
@patch("builtins.input", side_effect=["1", "testuser", "TestPass123", "3"])
def test_main_menu_login(mock_input, mock_login):
    with patch("client.menus.main_menu.show_main_menu", side_effect=SystemExit):
        try:
            client_main.main()
        except SystemExit:
            pass
    mock_login.assert_called_once()

@patch("client.menus.main_menu.signup")
@patch("builtins.input", side_effect=["2", "testuser", "testuser@example.com", "TestPass123", "3"])
def test_main_menu_signup(mock_input, mock_signup):
    with patch("client.menus.main_menu.show_main_menu", side_effect=SystemExit):
        try:
            client_main.main()
        except SystemExit:
            pass
    mock_signup.assert_called_once()