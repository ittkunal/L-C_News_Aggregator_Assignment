import pytest
from unittest.mock import patch

import client.services.user_service as user_service

@patch("client.services.user_service.requests.post")
@patch("client.services.user_service.get_session")
def test_save_article(mock_get_session, mock_post):
    mock_get_session.return_value = {"user_id": 1}
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "Article saved successfully."}
    with patch("builtins.input", side_effect=["3", "1", "1"]):
        user_service.display_articles([{
            "id": 1,
            "title": "Test Article",
            "content": "Test content",
            "source": "Test Source",
            "url": "http://example.com",
            "category": "business"
        }], user_id=1)

@patch("client.services.user_service.requests.delete")
@patch("client.services.user_service.get_session")
def test_delete_saved_article(mock_get_session, mock_delete):
    mock_get_session.return_value = {"user_id": 1}
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"message": "Article deleted successfully."}
    with patch("builtins.input", side_effect=["1", "1"]):
        user_service.show_saved_articles_menu()