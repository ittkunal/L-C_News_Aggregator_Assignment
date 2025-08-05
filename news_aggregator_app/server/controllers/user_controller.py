from fastapi import HTTPException
from server.repositories.user_repo import (
    get_user_by_id, update_user, get_saved_articles_db, save_article_db, delete_saved_article_db
)
from server.repositories.notification_repo import get_notifications_by_user, update_notification
from server.repositories.article_repo import report_article_db, get_articles_by_category_and_keywords

def get_profile(user_id):
    return get_user_by_id(user_id)

def update_profile(user_id, username=None, email=None):
    return update_user(user_id, username, email)

def get_saved_articles(user_id):
    return get_saved_articles_db(user_id)

def save_article(user_id, article_id):
    result = save_article_db(user_id, article_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

def delete_saved_article(user_id, article_id):
    result = delete_saved_article_db(user_id, article_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

def get_notifications(user_id):
    return get_notifications_by_user(user_id)

def update_notifications(user_id, type, enabled=None, keywords=None):
    from server.repositories.notification_repo import update_notification
    return update_notification(user_id, type, enabled, keywords)

def report_article_controller(article_id, user_id, reason=None):
    # Validate article exists
    from server.repositories.article_repo import article_exists
    if not article_exists(article_id):
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Validate user exists
    from server.repositories.user_repo import get_user_by_id
    if not get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    result = report_article_db(article_id, user_id, reason)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

def get_notification_articles(user_id):
    notifications = get_notifications_by_user(user_id)
    articles = []
    for notif in notifications:
        if notif["enabled"]:
            # Fetch recent articles for this category and keywords
            category = notif["type"]
            keywords = notif.get("keywords", "")
            matched = get_articles_by_category_and_keywords(category, keywords)
            articles.extend(matched)
    # Remove duplicates (by article id)
    unique_articles = {a["id"]: a for a in articles}.values()
    return list(unique_articles)