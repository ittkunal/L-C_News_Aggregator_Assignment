import pytest
from server.repositories.article_repo import (
    get_articles,
    get_article_by_id,
    search_articles_db,
    like_article_db,
    dislike_article_db,
)

def test_get_articles():
    articles = get_articles()
    assert isinstance(articles, list)

def test_search_articles():
    articles = search_articles_db("news")
    assert isinstance(articles, list)

def test_like_and_dislike_article():
    articles = get_articles()
    if not articles:
        pytest.skip("No articles in DB to like/dislike.")
    article_id = articles[0]["id"]
    user_id = 1 
    like_result = like_article_db(article_id, user_id)
    assert "success" in str(like_result).lower() or "liked" in str(like_result).lower()
    dislike_result = dislike_article_db(article_id, user_id)
    assert "success" in str(dislike_result).lower() or "disliked" in str(dislike_result).lower()

def test_get_article_by_id():
    articles = get_articles()
    if not articles:
        pytest.skip("No articles in DB to fetch by ID.")
    article_id = articles[0]["id"]
    article = get_article_by_id(article_id)
    assert article is not None
    assert article["id"] == article_id