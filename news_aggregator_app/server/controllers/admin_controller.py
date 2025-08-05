from fastapi import HTTPException
from server.repositories.admin_repo import (
    list_sources_db,
    get_source_db,
    update_source_db,
    add_source_db,
    add_category_db,
)

from server.repositories.article_repo import (
    get_reported_articles_db,
    set_article_hidden,
    set_category_hidden,
    add_filtered_keyword,
    remove_filtered_keyword,
    get_filtered_keywords,
    get_article_report_details,
    get_hidden_articles,
)

def list_sources():
    return list_sources_db()

def get_source(source_id):
    return get_source_db(source_id)

def update_source(source_id, api_key):
    if not api_key or not api_key.strip():
        raise HTTPException(status_code=400, detail="API key cannot be empty or blank")
    return update_source_db(source_id, api_key.strip())

def add_source(name, api_key):
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Source name cannot be empty or blank")
    if not api_key or not api_key.strip():
        raise HTTPException(status_code=400, detail="API key cannot be empty or blank")
    return add_source_db(name.strip(), api_key.strip())

def add_category(name, description=None):
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Category name cannot be empty or blank")
    return add_category_db(name.strip(), description)

def get_reported_articles():
    articles = get_reported_articles_db()
    if not articles:
        return []
    return articles

def hide_article(article_id, hide):
    return set_article_hidden(article_id, hide)

def hide_category(category, hide):
    return set_category_hidden(category, hide)

def add_filtered_keyword_controller(keyword):
    return add_filtered_keyword(keyword)

def remove_filtered_keyword_controller(keyword):
    return remove_filtered_keyword(keyword)

def get_filtered_keywords_controller():
    return get_filtered_keywords()

def get_article_report_details_controller(article_id):
    return get_article_report_details(article_id)

def get_hidden_articles_controller():
    return get_hidden_articles()