from fastapi import APIRouter, Body
from server.controllers.news_controller import (
    get_headlines, get_article, search_articles, get_categories,
    like_article, dislike_article, report_article
)
from server.controllers.user_controller import save_article, delete_saved_article

router = APIRouter()

@router.get("/headlines")
def headlines(date: str = None, start: str = None, end: str = None, category: str = None):
    return get_headlines(date, start, end, category)

@router.get("/categories")
def categories():
    return get_categories()

@router.get("/search")
def search(q: str, start: str = None, end: str = None, sort_by: str = None):
    return search_articles(q, start, end, sort_by)

@router.get("/{article_id}")
def article(article_id: int):
    return get_article(article_id)

@router.post("/{article_id}/like")
def like(article_id: int, user_id: int):
    return like_article(article_id, user_id)

@router.post("/{article_id}/dislike")
def dislike(article_id: int, user_id: int):
    return dislike_article(article_id, user_id)

@router.post("/{article_id}/report")
def report(article_id: int, user_id: int):
    return report_article(article_id, user_id)


# RESTful endpoints to save/delete articles

@router.post("/{article_id}/save")
def save_article_endpoint(article_id: int, user_id: int = Body(...)):
    """
    Save the specified article for the user.
    """
    return save_article(user_id, article_id)

@router.delete("/{article_id}/save")
def delete_article_save(article_id: int, user_id: int):
    """
    Remove the saved article for the user.
    """
    return delete_saved_article(user_id, article_id)
