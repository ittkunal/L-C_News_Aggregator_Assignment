from fastapi import APIRouter
from fastapi import Body
from server.controllers.user_controller import (
    get_profile,
    update_profile,
    get_saved_articles,
    save_article,
    delete_saved_article,
    get_notifications,
    update_notifications,
    report_article_controller,
)

router = APIRouter()


@router.get("/profile")
def profile(user_id: int):
    return get_profile(user_id)


@router.put("/profile")
def update(user_id: int, username: str = None, email: str = None):
    return update_profile(user_id, username, email)


@router.get("/saved-articles")
def saved_articles(user_id: int):
    return get_saved_articles(user_id)


@router.post("/saved-articles")
def save(user_id: int, article_id: int):
    return save_article(user_id, article_id)


@router.delete("/saved-articles/{article_id}")
def delete(user_id: int, article_id: int):
    return delete_saved_article(user_id, article_id)


@router.get("/notifications")
def notifications(user_id: int):
    return get_notifications(user_id)


@router.put("/notifications")
def update_notifications_route(user_id: int, type: str, keywords: str = None, enabled: bool = None):
    return update_notifications(user_id, type, enabled, keywords)


@router.post("/report-article")
def report_article_route(
    article_id: int = Body(...), user_id: int = Body(...), reason: str = Body(None)):
    return report_article_controller(article_id, user_id, reason)
