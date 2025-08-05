from server.repositories.article_repo import (
    get_articles, get_article_by_id, search_articles_db, get_categories_db,
    like_article_db, dislike_article_db, report_article_db
)

def get_headlines(date=None, start=None, end=None, category=None, limit=None):
    return get_articles(date, start, end, category, limit)

def get_article(article_id):
    return get_article_by_id(article_id)

def search_articles(q, start=None, end=None, sort_by=None):
    return search_articles_db(q, start, end, sort_by)

def get_categories():
    return get_categories_db()

def like_article(article_id, user_id):
    return like_article_db(article_id, user_id)

def dislike_article(article_id, user_id):
    return dislike_article_db(article_id, user_id)

def report_article(article_id, user_id, reason=None):
    return report_article_db(article_id, user_id, reason)