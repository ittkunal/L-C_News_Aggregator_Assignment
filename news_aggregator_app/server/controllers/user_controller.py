from server.repositories.user_repo import (
    get_user_by_id, update_user, get_saved_articles_db, save_article_db, delete_saved_article_db
)
from server.repositories.notification_repo import get_notifications_by_user, update_notification
from server.repositories.article_repo import report_article_db

def get_profile(user_id):
    return get_user_by_id(user_id)

def update_profile(user_id, username=None, email=None):
    return update_user(user_id, username, email)

def get_saved_articles(user_id):
    return get_saved_articles_db(user_id)

def save_article(user_id, article_id):
    return save_article_db(user_id, article_id)

def delete_saved_article(user_id, article_id):
    return delete_saved_article_db(user_id, article_id)

def get_notifications(user_id):
    return get_notifications_by_user(user_id)

def update_notifications(user_id, type, keywords=None, enabled=None):
    from server.repositories.notification_repo import update_notification
    return update_notification(user_id, type, enabled, keywords)

def report_article_controller(article_id, user_id, reason=None):
    return report_article_db(article_id, user_id)