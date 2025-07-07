import pytest
from server.repositories.notification_repo import (
    get_notifications_by_user,
    update_notification,
    get_users_for_notification,
)

@pytest.fixture
def test_user_id():
    return 1

def test_update_and_get_notifications(test_user_id):
    result = update_notification(test_user_id, "business", enabled=True, keywords="stock,market")
    assert "message" in result
    notifications = get_notifications_by_user(test_user_id)
    assert isinstance(notifications, list)
    found = any(n["type"] == "business" and n["enabled"] in [True, 1] for n in notifications)
    assert found

def test_disable_notification(test_user_id):
    result = update_notification(test_user_id, "business", enabled=False)
    assert "message" in result
    notifications = get_notifications_by_user(test_user_id)
    found = any(n["type"] == "business" and n["enabled"] in [False, 0] for n in notifications)
    assert found

def test_get_users_for_notification():
    users = get_users_for_notification()
    assert isinstance(users, list)
    if users:
        assert "type" in users[0]
        assert "keywords" in users[0]