from server.repositories.user_repo import (
    get_user_by_id, update_user, get_saved_articles_db, save_article_db, delete_saved_article_db,
    get_notifications_db, update_notifications_db
)

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
    return get_notifications_db(user_id)

def update_notifications(user_id, keywords=None, enabled=None):
    return update_notifications_db(user_id, keywords, enabled)