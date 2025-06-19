from fastapi import APIRouter, Query
from server.controllers.news_controller import (
    get_headlines, get_article, search_articles, get_categories, like_article, dislike_article
)

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