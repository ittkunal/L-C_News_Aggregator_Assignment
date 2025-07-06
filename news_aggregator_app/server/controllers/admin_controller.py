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
)

def list_sources():
    return list_sources_db()

def get_source(source_id):
    return get_source_db(source_id)

def update_source(source_id, api_key):
    return update_source_db(source_id, api_key)

def add_source(name, api_key):
    return add_source_db(name, api_key)

def add_category(name, description=None):
    return add_category_db(name, description)

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